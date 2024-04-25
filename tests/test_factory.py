"""Tests for the ObjectFactory class in factory.py"""
from unittest import TestCase
from multidig.helpers import factory

class TestObjectFactory(TestCase):
    """Testing the ObjectFactory class."""
    def setUp(self):
        self.test_args = {
            "foo": "bar"
        }

    def test_factory_instance(self):
        """Check that class can be instantiated."""
        test_obj = factory.ObjectFactory()
        self.assertIsInstance(
            test_obj,
            factory.ObjectFactory,
            msg="ObjectFactory can be instantiated."
        )

    def test_register_plugin(self):
        """Check that we can register new plugins in the object factory."""
        test_obj = factory.ObjectFactory()
        def test_builder():
            pass
        test_obj.register_plugin('ObjectFactoryTest', test_builder())
        self.assertIn(
            'ObjectFactoryTest',
            test_obj._plugins.keys(), # pylint: disable=W0212
            msg="Plugin has been correctly added to list of plugins."
        )

    def test_query_plugin_create(self):
        """Test if we can create a new Query plugin in the object factory."""
        test_obj = factory.ObjectFactory()

        class TestQueryPlugin:
            """A dummy Query plugin for testing."""
            def __init__(self, **kwargs):
                """Dummy concrete function."""

            def setup(self):
                """Dummy concrete function."""

            def query_dns(self):
                """Dummy concrete function."""
                return True

        def test_plugin(**kwargs):
            return TestQueryPlugin(**kwargs)

        test_obj.register_plugin('TestQueryPlugin', test_plugin)
        self.assertIsInstance(
            test_obj.create('TestQueryPlugin', **self.test_args),
            TestQueryPlugin,
            msg="Successfully created Query Plugin."
        )

    def test_output_plugin_create(self):
        """Test if we can create a new Output plugin in the object factory."""
        test_obj = factory.ObjectFactory()

        class TestOutputPlugin:
            """A dummy Query plugin for testing."""
            def __init__(self, **kwargs):
                """Dummy concrete function."""

            def parse_answers(self):
                """Dummy concrete function."""
                return True

        def test_plugin(**kwargs):
            return TestOutputPlugin(**kwargs)

        test_obj.register_plugin('TestOutputPlugin', test_plugin)
        self.assertIsInstance(
            test_obj.create('TestOutputPlugin', **self.test_args),
            TestOutputPlugin,
            msg="Successfully created Output Plugin."
        )

    def test_invalid_plugin_create(self):
        """Check that correct exception is raised when invalid
        plugin is selected."""
        test_obj = factory.ObjectFactory()
        with self.assertRaises(
            ValueError,
            msg="Raise exception if invalid plugin is selected."
        ) as current_exception:
            test_obj.create("NonExisting", **self.test_args)
        self.assertEqual(
            str(current_exception.exception),
            "Not a registered plugin: NonExisting"
        )
