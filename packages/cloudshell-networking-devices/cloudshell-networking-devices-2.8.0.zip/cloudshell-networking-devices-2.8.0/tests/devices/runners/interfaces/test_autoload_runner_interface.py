import unittest

from cloudshell.devices.runners.interfaces.autoload_runner_interface import AutoloadOperationsInterface


class TestCliCliHandlerInterface(unittest.TestCase):
    def setUp(self):
        class TestedClass(AutoloadOperationsInterface):
            pass
        self.tested_class = TestedClass

    def test_discover(self):
        """Check that instance can't be instantiated without implementation of the "discover" method"""
        with self.assertRaisesRegexp(TypeError, "Can't instantiate abstract class TestedClass with "
                                                "abstract methods discover"):
            self.tested_class()

    def test_discover_does_nothing(self):
        class TestedClass(AutoloadOperationsInterface):
            def discover(self):
                return super(TestedClass, self).discover()

        tested_class = TestedClass()

        self.assertIsNone(tested_class.discover())
