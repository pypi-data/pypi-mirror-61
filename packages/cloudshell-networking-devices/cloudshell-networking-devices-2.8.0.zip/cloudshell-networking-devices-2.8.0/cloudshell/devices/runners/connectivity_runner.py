#!/usr/bin/python
# -*- coding: utf-8 -*-

import traceback

import jsonpickle

from abc import abstractproperty
from collections import defaultdict
from threading import Thread, current_thread

from cloudshell.core.driver_response import DriverResponse
from cloudshell.core.driver_response_root import DriverResponseRoot
from cloudshell.networking.apply_connectivity.models.connectivity_result import ConnectivityErrorResponse, \
    ConnectivitySuccessResponse
from cloudshell.devices.json_request_helper import JsonRequestDeserializer
from cloudshell.devices.networking_utils import serialize_to_json, validate_vlan_range, \
    validate_vlan_number, command_logging
from cloudshell.devices.runners.interfaces.connectivity_runner_interface import ConnectivityOperationsInterface


class ConnectivityRunner(ConnectivityOperationsInterface):
    IS_VLAN_RANGE_SUPPORTED = True
    APPLY_CONNECTIVITY_CHANGES_ACTION_REQUIRED_ATTRIBUTE_LIST = ["type", "actionId",
                                                                 ("connectionParams", "mode"),
                                                                 ("actionTarget", "fullAddress")]

    def __init__(self, logger, cli_handler):
        self._logger = logger
        self.result = defaultdict(list)
        self._cli_handler = cli_handler

    @property
    def cli_handler(self):
        """ CLI Handler property
        :return: CLI handler
        """

        return self._cli_handler

    @abstractproperty
    def add_vlan_flow(self):
        """ Get Add VLAN flow property
        :return: AddVLANFlow object
        """

        pass

    @abstractproperty
    def remove_vlan_flow(self):
        """ Remove VLAN flow property
        :return: RemoveVLANFlow object
        """

        pass

    @command_logging
    def apply_connectivity_changes(self, request):
        """ Handle apply connectivity changes request json, trigger add or remove vlan methods,
        get responce from them and create json response

        :param request: json with all required action to configure or remove vlans from certain port
        :return Serialized DriverResponseRoot to json
        :rtype json
        """

        if request is None or request == "":
            raise Exception(self.__class__.__name__, "request is None or empty")

        holder = JsonRequestDeserializer(jsonpickle.decode(request))

        if not holder or not hasattr(holder, "driverRequest"):
            raise Exception(self.__class__.__name__, "Deserialized request is None or empty")

        driver_response = DriverResponse()
        add_vlan_thread_list = []
        remove_vlan_thread_list = []
        driver_response_root = DriverResponseRoot()

        for action in holder.driverRequest.actions:
            self._logger.info("Action: ", action.__dict__)
            self._validate_request_action(action)

            action_id = action.actionId
            full_name = action.actionTarget.fullName
            port_mode = action.connectionParams.mode.lower()

            if action.type == "setVlan":
                qnq = False
                ctag = ""
                for attribute in action.connectionParams.vlanServiceAttributes:
                    if attribute.attributeName.lower() == "qnq" and attribute.attributeValue.lower() == "true":
                        qnq = True
                    if attribute.attributeName.lower() == "ctag":
                        ctag = attribute.attributeValue

                for vlan_id in self._get_vlan_list(action.connectionParams.vlanId):
                    add_vlan_thread = Thread(target=self.add_vlan,
                                             name=action_id,
                                             args=(vlan_id, full_name, port_mode, qnq, ctag))
                    add_vlan_thread_list.append(add_vlan_thread)
            elif action.type == "removeVlan":
                for vlan_id in self._get_vlan_list(action.connectionParams.vlanId):
                    remove_vlan_thread = Thread(target=self.remove_vlan,
                                                name=action_id,
                                                args=(vlan_id, full_name, port_mode,))
                    remove_vlan_thread_list.append(remove_vlan_thread)
            else:
                self._logger.warning("Undefined action type determined '{}': {}".format(action.type, action.__dict__))
                continue

        # Start all created remove_vlan_threads
        for thread in remove_vlan_thread_list:
            thread.start()

        # Join all remove_vlan_threads. Main thread will wait completion of all remove_vlan_thread
        for thread in remove_vlan_thread_list:
            thread.join()

        # Start all created add_vlan_threads
        for thread in add_vlan_thread_list:
            thread.start()

        # Join all add_vlan_threads. Main thread will wait completion of all add_vlan_thread
        for thread in add_vlan_thread_list:
            thread.join()

        request_result = []
        for action in holder.driverRequest.actions:
            result_statuses, message = zip(*self.result.get(action.actionId))
            if all(result_statuses):
                action_result = ConnectivitySuccessResponse(action,
                                                            "Add Vlan {vlan} configuration successfully completed"
                                                            .format(vlan=action.connectionParams.vlanId))
            else:
                message_details = "\n\t".join(message)
                action_result = ConnectivityErrorResponse(action, "Add Vlan {vlan} configuration failed."
                                                                  "\nAdd Vlan configuration details:\n{message_details}"
                                                          .format(vlan=action.connectionParams.vlanId,
                                                                  message_details=message_details))
            request_result.append(action_result)

        driver_response.actionResults = request_result
        driver_response_root.driverResponse = driver_response
        return serialize_to_json(driver_response_root)  # .replace("[true]", "true")

    def _validate_request_action(self, action):
        """ Validate action from the request json,
            according to APPLY_CONNECTIVITY_CHANGES_ACTION_REQUIRED_ATTRIBUTE_LIST
        """
        is_fail = False
        fail_attribute = ""
        for class_attribute in self.APPLY_CONNECTIVITY_CHANGES_ACTION_REQUIRED_ATTRIBUTE_LIST:
            if type(class_attribute) is tuple:
                if not hasattr(action, class_attribute[0]):
                    is_fail = True
                    fail_attribute = class_attribute[0]
                if not hasattr(getattr(action, class_attribute[0]), class_attribute[1]):
                    is_fail = True
                    fail_attribute = class_attribute[1]
            else:
                if not hasattr(action, class_attribute):
                    is_fail = True
                    fail_attribute = class_attribute

        if is_fail:
            raise Exception(self.__class__.__name__,
                            "Mandatory field {0} is missing in ApplyConnectivityChanges request json".format(
                                fail_attribute))

    def _get_vlan_list(self, vlan_str):
        """ Get VLAN list from input string

        :param vlan_str:
        :return list of VLANs or Exception
        """

        result = set()
        for splitted_vlan in vlan_str.split(","):
            if "-" not in splitted_vlan:
                if validate_vlan_number(splitted_vlan):
                    result.add(int(splitted_vlan))
                else:
                    raise Exception(self.__class__.__name__, "Wrong VLAN number detected {}".format(splitted_vlan))
            else:
                if self.IS_VLAN_RANGE_SUPPORTED:
                    if validate_vlan_range(splitted_vlan):
                        result.add(splitted_vlan)
                    else:
                        raise Exception(self.__class__.__name__, "Wrong VLANs range detected {}".format(vlan_str))
                else:
                    start, end = map(int, splitted_vlan.split("-"))
                    if validate_vlan_number(start) and validate_vlan_number(end):
                        if start > end:
                            start, end = end, start
                        for vlan in range(start, end + 1):
                            result.add(vlan)
                    else:
                        raise Exception(self.__class__.__name__, "Wrong VLANs range detected {}".format(vlan_str))

        return map(str, list(result))

    def add_vlan(self, vlan_id, full_name, port_mode, qnq, c_tag):
        """ Run flow to add VLAN(s) to interface

        :param vlan_id: Already validated number of VLAN(s)
        :param full_name: Full interface name. Example: 2950/Chassis 0/FastEthernet0-23
        :param port_mode: port mode type. Should be trunk or access
        :param qnq:
        :param c_tag:
        """

        try:
            action_result = self.add_vlan_flow.execute_flow(vlan_range=vlan_id,
                                                            port_mode=port_mode,
                                                            port_name=full_name,
                                                            qnq=qnq,
                                                            c_tag=c_tag)
            self.result[current_thread().name].append((True, action_result))
        except Exception as e:
            self._logger.error(traceback.format_exc())
            self.result[current_thread().name].append((False, e.message))

    def remove_vlan(self, vlan_id, full_name, port_mode):
        """
        Run flow to remove VLAN(s) from interface
        :param vlan_id: Already validated number of VLAN(s)
        :param full_name: Full interface name. Example: 2950/Chassis 0/FastEthernet0-23
        :param port_mode: port mode type. Should be trunk or access
        """

        try:

            action_result = self.remove_vlan_flow.execute_flow(vlan_range=vlan_id,
                                                               port_name=full_name,
                                                               port_mode=port_mode)
            self.result[current_thread().name].append((True, action_result))
        except Exception as e:
            self._logger.error(traceback.format_exc())
            self.result[current_thread().name].append((False, e.message))
