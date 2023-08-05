import unittest
from collections import defaultdict

import mock

from cloudshell.devices.runners.connectivity_runner import ConnectivityRunner


class TestConnectivityRunner(unittest.TestCase):
    def setUp(self):
        self.logger = mock.MagicMock()
        self.cli_handler = mock.MagicMock()

        class TestedConnectivityRunner(ConnectivityRunner):
            def cli_handler(self):
                pass

            def add_vlan_flow(self):
                pass

            def remove_vlan_flow(self):
                pass

        self.connectivity_runner = TestedConnectivityRunner(logger=self.logger, cli_handler=self.cli_handler)

    def test_abstract_methods(self):
        """Check that instance can't be instantiated without implementation of the all abstract methods"""
        class TestedClass(ConnectivityRunner):
            pass

        with self.assertRaisesRegexp(TypeError, "Can't instantiate abstract class TestedClass with abstract methods "
                                                "add_vlan_flow, remove_vlan_flow"):
            TestedClass(logger=self.logger, cli_handler=self.cli_handler)

    def test_get_vlan_list(self):
        """Check that method will return list of valid VLANs if all od them are valid"""
        vlan_str = "10-15,19,21-23"
        # act
        result = self.connectivity_runner._get_vlan_list(vlan_str=vlan_str)
        # verify
        self.assertEqual(result, ["21-23", "19", "10-15"])

    def test_get_vlan_list_vlan_range_range_is_not_supported(self):
        """Check that method will return list with VLANs between the given range and change start/end if needed"""
        self.connectivity_runner.IS_VLAN_RANGE_SUPPORTED = False
        vlan_str = "12-10"
        # act
        result = self.connectivity_runner._get_vlan_list(vlan_str=vlan_str)
        # verify
        self.assertEqual(result, ["10", "11", "12"])

    @mock.patch("cloudshell.devices.runners.connectivity_runner.validate_vlan_number")
    def test_get_vlan_list_invalid_vlan_number(self, validate_vlan_number):
        """Check that method will raise Exception if VLAN number is not valid"""
        validate_vlan_number.return_value = False
        vlan_str = "5000"
        # act
        with self.assertRaisesRegexp(Exception, "Wrong VLAN number detected 5000"):
            self.connectivity_runner._get_vlan_list(vlan_str=vlan_str)

    @mock.patch("cloudshell.devices.runners.connectivity_runner.validate_vlan_range")
    def test_get_vlan_list_invalid_vlan_range(self, validate_vlan_range):
        """Check that method will raise Exception if VLAN range is not valid"""
        self.connectivity_runner.IS_VLAN_RANGE_SUPPORTED = True
        validate_vlan_range.return_value = False
        vlan_str = "5000-5005"
        # act
        with self.assertRaisesRegexp(Exception, "Wrong VLANs range detected 5000-5005"):
            self.connectivity_runner._get_vlan_list(vlan_str=vlan_str)

    @mock.patch("cloudshell.devices.runners.connectivity_runner.validate_vlan_number")
    def test_get_vlan_list_invalid_vlan_range_range_is_not_supported(self, validate_vlan_number):
        """Check that method will raise Exception if VLAN range is not valid and IS_VLAN_RANGE_SUPPORTED is False"""
        self.connectivity_runner.IS_VLAN_RANGE_SUPPORTED = False
        validate_vlan_number.return_value = False
        vlan_str = "5000-5005"
        # act
        with self.assertRaisesRegexp(Exception, "Wrong VLANs range detected 5000-5005"):
            self.connectivity_runner._get_vlan_list(vlan_str=vlan_str)

    @mock.patch("cloudshell.devices.runners.connectivity_runner.current_thread")
    def test_add_vlan(self, current_thread):
        """Check that method will execute add_vlan_flow and add it to the result"""
        vlan_id = "some vlan id"
        full_name = "some full name"
        port_mode = "port mode"
        qnq = mock.MagicMock()
        c_tag = mock.MagicMock()
        expected_res = defaultdict(list)
        action_result = mock.MagicMock()
        expected_res[current_thread().name] = [(True, action_result)]
        self.connectivity_runner.add_vlan_flow = mock.MagicMock(
            execute_flow=mock.MagicMock(
                return_value=action_result))
        # act
        self.connectivity_runner.add_vlan(vlan_id=vlan_id,
                                          full_name=full_name,
                                          port_mode=port_mode,
                                          qnq=qnq,
                                          c_tag=c_tag)
        # verify
        self.connectivity_runner.add_vlan_flow.execute_flow.assert_called_once_with(
            vlan_range=vlan_id,
            port_mode=port_mode,
            port_name=full_name,
            qnq=qnq,
            c_tag=c_tag)

        self.assertEqual(self.connectivity_runner.result, expected_res)

    @mock.patch("cloudshell.devices.runners.connectivity_runner.current_thread")
    def test_add_vlan_failed(self, current_thread):
        """Check that method will execute add_vlan_flow and add error message to the result"""
        vlan_id = "some vlan id"
        full_name = "some full name"
        port_mode = "port mode"
        qnq = mock.MagicMock()
        c_tag = mock.MagicMock()
        expected_res = defaultdict(list)
        error_msg = "some exception message"
        expected_res[current_thread().name] = [(False, error_msg)]
        self.connectivity_runner.add_vlan_flow = mock.MagicMock(
            execute_flow=mock.MagicMock(
                side_effect=Exception(error_msg)))
        # act
        self.connectivity_runner.add_vlan(vlan_id=vlan_id,
                                          full_name=full_name,
                                          port_mode=port_mode,
                                          qnq=qnq,
                                          c_tag=c_tag)
        # verify
        self.connectivity_runner.add_vlan_flow.execute_flow.assert_called_once_with(
            vlan_range=vlan_id,
            port_mode=port_mode,
            port_name=full_name,
            qnq=qnq,
            c_tag=c_tag)

        self.assertEqual(self.connectivity_runner.result, expected_res)

    @mock.patch("cloudshell.devices.runners.connectivity_runner.current_thread")
    def test_remove_vlan(self, current_thread):
        """Check that method will execute remove_vlan_flow and add it to the result"""
        vlan_id = "some vlan id"
        full_name = "some full name"
        port_mode = "port mode"
        expected_res = defaultdict(list)
        action_result = mock.MagicMock()
        expected_res[current_thread().name] = [(True, action_result)]
        self.connectivity_runner.remove_vlan_flow = mock.MagicMock(
            execute_flow=mock.MagicMock(
                return_value=action_result))
        # act
        self.connectivity_runner.remove_vlan(vlan_id=vlan_id,
                                             full_name=full_name,
                                             port_mode=port_mode)
        # verify
        self.connectivity_runner.remove_vlan_flow.execute_flow.assert_called_once_with(
            vlan_range=vlan_id,
            port_mode=port_mode,
            port_name=full_name)

        self.assertEqual(self.connectivity_runner.result, expected_res)

    @mock.patch("cloudshell.devices.runners.connectivity_runner.current_thread")
    def test_remove_vlan_failed(self, current_thread):
        """Check that method will execute remove_vlan_flow and add error message to the result"""
        vlan_id = "some vlan id"
        full_name = "some full name"
        port_mode = "port mode"
        expected_res = defaultdict(list)
        error_msg = "some exception message"
        expected_res[current_thread().name] = [(False, error_msg)]
        self.connectivity_runner.remove_vlan_flow = mock.MagicMock(
            execute_flow=mock.MagicMock(
                side_effect=Exception(error_msg)))
        # act
        self.connectivity_runner.remove_vlan(vlan_id=vlan_id,
                                             full_name=full_name,
                                             port_mode=port_mode)
        # verify
        self.connectivity_runner.remove_vlan_flow.execute_flow.assert_called_once_with(
            vlan_range=vlan_id,
            port_mode=port_mode,
            port_name=full_name)

        self.assertEqual(self.connectivity_runner.result, expected_res)

    def test_validate_request_action_no_attr(self):
        """Check that method will raise exception if action object doesn't contain required attr"""
        class Action(object):
            type = ""

            class connectionParams(object):
                mode = ""

            class actionTarget(object):
                fullAddress = ""

        with self.assertRaisesRegexp(Exception, "Mandatory field actionId is missing in ApplyConnectivityChanges "
                                                "request json"):
            self.connectivity_runner._validate_request_action(action=Action())

    def test_validate_request_action_no_nested_obj(self):
        """Check that method will raise exception if action object doesn't contain required nested object"""
        class Action(object):
            type = ""
            actionId = ""

            class actionTarget(object):
                fullAddress = ""

        with self.assertRaisesRegexp(Exception, "'Action' object has no attribute 'connectionParams'"):
            self.connectivity_runner._validate_request_action(action=Action())

    def test_validate_request_action_no_attr_on_nested_obj(self):
        """Check that method will raise exception if nested object on the action one doesn't contain required attr"""
        class Action(object):
            type = ""
            actionId = ""

            class connectionParams(object):
                pass

            class actionTarget(object):
                fullAddress = ""

        with self.assertRaisesRegexp(Exception, "Mandatory field mode is missing in ApplyConnectivityChanges "
                                                "request json"):
            self.connectivity_runner._validate_request_action(action=Action())

    def test_apply_connectivity_changes_no_requests(self):
        """Check that method will raise exception if request is None"""
        with self.assertRaisesRegexp(Exception, "request is None or empty"):
            self.connectivity_runner.apply_connectivity_changes(request=None)

    @mock.patch("cloudshell.devices.runners.connectivity_runner.jsonpickle")
    @mock.patch("cloudshell.devices.runners.connectivity_runner.JsonRequestDeserializer")
    def test_apply_connectivity_changes_no_json_req_holder(self, json_request_deserializer_class, jsonpickle):
        """Check that method will raise exception if json request was not correctly parsed"""
        json_request_deserializer_class.return_value = None
        request = mock.MagicMock()

        with self.assertRaisesRegexp(Exception, "Deserialized request is None or empty"):
            self.connectivity_runner.apply_connectivity_changes(request=request)

    @mock.patch("cloudshell.devices.runners.connectivity_runner.DriverResponseRoot")
    @mock.patch("cloudshell.devices.runners.connectivity_runner.serialize_to_json")
    @mock.patch("cloudshell.devices.runners.connectivity_runner.jsonpickle")
    @mock.patch("cloudshell.devices.runners.connectivity_runner.JsonRequestDeserializer")
    def test_apply_connectivity_changes(self, json_request_deserializer_class, jsonpickle, serialize_to_json,
                                        driver_response_root_class):
        """Check that method will return serialized response"""
        response = mock.MagicMock()
        driver_response_root = mock.MagicMock()
        driver_response_root_class.return_value = driver_response_root
        serialize_to_json.return_value = response
        json_request_deserializer = mock.MagicMock(
            driverRequest=mock.MagicMock(actions=[]))

        json_request_deserializer_class.return_value = json_request_deserializer
        request = mock.MagicMock()
        # act
        result = self.connectivity_runner.apply_connectivity_changes(request=request)
        # verify
        self.assertEqual(result, response)
        serialize_to_json.assert_called_once_with(driver_response_root)

    @mock.patch("cloudshell.devices.runners.connectivity_runner.Thread")
    @mock.patch("cloudshell.devices.runners.connectivity_runner.ConnectivitySuccessResponse")
    @mock.patch("cloudshell.devices.runners.connectivity_runner.serialize_to_json")
    @mock.patch("cloudshell.devices.runners.connectivity_runner.jsonpickle")
    @mock.patch("cloudshell.devices.runners.connectivity_runner.JsonRequestDeserializer")
    def test_apply_connectivity_changes_set_vlan_action_success(self, json_request_deserializer_class,
                                                                jsonpickle, serialize_to_json,
                                                                connectivity_success_response_class, thread_class):
        """Check that method will add success response for the set_vlan action"""
        action_id = "some action id"
        vlan_id = "test vlan id"
        qnq = True
        ctag = "ctag value"
        self.connectivity_runner.result[action_id] = [(True, "success action message")]
        self.connectivity_runner._get_vlan_list = mock.MagicMock(return_value=[vlan_id])
        action = mock.MagicMock(type="setVlan",
                                actionId=action_id,
                                connectionParams=mock.MagicMock(vlanServiceAttributes=[
                                    mock.MagicMock(attributeName="QNQ",
                                                   attributeValue=str(qnq)),
                                    mock.MagicMock(attributeName="CTAG",
                                                   attributeValue=ctag)
                                ]))

        json_request_deserializer = mock.MagicMock(
            driverRequest=mock.MagicMock(actions=[action]))

        json_request_deserializer_class.return_value = json_request_deserializer
        request = mock.MagicMock()

        # act
        self.connectivity_runner.apply_connectivity_changes(request=request)

        # verify
        thread_class.assert_any_call(target=self.connectivity_runner.add_vlan,
                                     name=action_id,
                                     args=(vlan_id, action.actionTarget.fullName, action.connectionParams.mode.lower(),
                                           qnq, ctag))

        connectivity_success_response_class.assert_called_once_with(
            action, "Add Vlan {} configuration successfully completed".format(action.connectionParams.vlanId))

    @mock.patch("cloudshell.devices.runners.connectivity_runner.ConnectivityErrorResponse")
    @mock.patch("cloudshell.devices.runners.connectivity_runner.serialize_to_json")
    @mock.patch("cloudshell.devices.runners.connectivity_runner.jsonpickle")
    @mock.patch("cloudshell.devices.runners.connectivity_runner.JsonRequestDeserializer")
    def test_apply_connectivity_changes_set_vlan_action_error(self, json_request_deserializer_class,
                                                                jsonpickle, serialize_to_json,
                                                                connectivity_error_response_class):
        """Check that method will add error response for the failed set_vlan action"""
        action_id = "some action id"
        self.connectivity_runner.result[action_id] = [(False, "failed action message")]
        action = mock.MagicMock(type="setVlan", actionId=action_id)
        json_request_deserializer = mock.MagicMock(
            driverRequest=mock.MagicMock(actions=[action]))

        json_request_deserializer_class.return_value = json_request_deserializer
        request = mock.MagicMock()

        # act
        self.connectivity_runner.apply_connectivity_changes(request=request)

        # verify
        connectivity_error_response_class.assert_called_once_with(
            action, "Add Vlan {} configuration failed.\n"
                    "Add Vlan configuration details:\n"
                    "failed action message".format(action.connectionParams.vlanId))

    @mock.patch("cloudshell.devices.runners.connectivity_runner.Thread")
    @mock.patch("cloudshell.devices.runners.connectivity_runner.ConnectivitySuccessResponse")
    @mock.patch("cloudshell.devices.runners.connectivity_runner.serialize_to_json")
    @mock.patch("cloudshell.devices.runners.connectivity_runner.jsonpickle")
    @mock.patch("cloudshell.devices.runners.connectivity_runner.JsonRequestDeserializer")
    def test_apply_connectivity_changes_remove_vlan_action_success(self, json_request_deserializer_class,
                                                                jsonpickle, serialize_to_json,
                                                                connectivity_success_response_class, thread_class):
        """Check that method will add success response for the remove_vlan action"""
        action_id = "some action id"
        vlan_id = "test vlan id"
        self.connectivity_runner.result[action_id] = [(True, "success action message")]
        self.connectivity_runner._get_vlan_list = mock.MagicMock(return_value=[vlan_id])

        action = mock.MagicMock(type="removeVlan", actionId=action_id)

        json_request_deserializer = mock.MagicMock(
            driverRequest=mock.MagicMock(actions=[action]))

        json_request_deserializer_class.return_value = json_request_deserializer
        request = mock.MagicMock()

        # act
        self.connectivity_runner.apply_connectivity_changes(request=request)
        # verify
        thread_class.assert_any_call(target=self.connectivity_runner.remove_vlan,
                                     name=action_id,
                                     args=(vlan_id, action.actionTarget.fullName, action.connectionParams.mode.lower()))

        connectivity_success_response_class.assert_called_once_with(
            action, "Add Vlan {} configuration successfully completed".format(action.connectionParams.vlanId))

    @mock.patch("cloudshell.devices.runners.connectivity_runner.Thread")
    @mock.patch("cloudshell.devices.runners.connectivity_runner.ConnectivitySuccessResponse")
    @mock.patch("cloudshell.devices.runners.connectivity_runner.serialize_to_json")
    @mock.patch("cloudshell.devices.runners.connectivity_runner.jsonpickle")
    @mock.patch("cloudshell.devices.runners.connectivity_runner.JsonRequestDeserializer")
    def test_apply_connectivity_changes_unknown_action(self, json_request_deserializer_class,
                                                                jsonpickle, serialize_to_json,
                                                                connectivity_success_response_class, thread_class):
        """Check that method will skip unknown action"""
        action_id = "some action id"
        vlan_id = "test vlan id"
        self.connectivity_runner.result[action_id] = [(True, "success action message")]
        self.connectivity_runner._get_vlan_list = mock.MagicMock(return_value=[vlan_id])

        action = mock.MagicMock(type="UNKNOWN", actionId=action_id)

        json_request_deserializer = mock.MagicMock(
            driverRequest=mock.MagicMock(actions=[action]))

        json_request_deserializer_class.return_value = json_request_deserializer
        request = mock.MagicMock()

        # act
        self.connectivity_runner.apply_connectivity_changes(request=request)

        # verify
        connectivity_success_response_class.assert_called_once_with(
            action, "Add Vlan {} configuration successfully completed".format(action.connectionParams.vlanId))

    def test_prop_cli_handler(self):
        class TestedClass(ConnectivityRunner):
            def add_vlan_flow(self):
                pass

            def remove_vlan_flow(self):
                pass

        tested_class = TestedClass(self.logger, self.cli_handler)

        self.assertEqual(self.cli_handler, tested_class.cli_handler)

    def test_add_and_remove_vlan_flow_do_nothing(self):
        class TestedClass(ConnectivityRunner):
            @property
            def remove_vlan_flow(self):
                return super(TestedClass, self).remove_vlan_flow

            @property
            def add_vlan_flow(self):
                return super(TestedClass, self).add_vlan_flow

        tested_class = TestedClass(self.logger, self.cli_handler)

        self.assertIsNone(tested_class.add_vlan_flow)
        self.assertIsNone(tested_class.remove_vlan_flow)
