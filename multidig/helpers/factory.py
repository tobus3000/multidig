"""
A multi purpose Object Factory Class.

Classes:
    ObjectFactory
    QueryPluginProvider
    ResponsePluginProvider
"""
class ObjectFactory:
    """
    The ObjectFactory object is a basic object factory class.
    Child classes can inherit this class and extend it's functionality.
    :ivar _plugins: A dictionary that keeps track of the registered plugins.
    :vartype _plugins: dict
    """
    def __init__(self):
        self._plugins = {}

    def register_plugin(self, key, plugin):
        """
        Register a new plugin by providing a name as `key` and Plugin object as `plugin`.

        :param key: The name reference to the plugin.
        :type key: str
        :param plugin: An object instance of a Plugin class.
        :type plugin: obj
        """
        self._plugins[key] = plugin

    def create(self, key, **kwargs):
        """
        Used to create and return a requested plugin object instance.

        :param key: The name reference of the plugin.
        :type key: str
        :param **kwargs: The keyword arguments used to setup the plugin.
        :type **kwargs: dict
        :return: The object instance of the requested plugin.
        :rtype: obj
        :raises: :class:`ValueError`: Not a registered plugin.
        """
        plugin = self._plugins.get(key)
        if not plugin:
            raise ValueError(f"Not a registered plugin: {key}")
        return plugin(**kwargs)

    def list(self):
        """
        Returns a list of plugin keys.

        :return: A list of available plugins.
        :rtype: list
        """
        return self._plugins.keys()

class QueryPluginProvider(ObjectFactory):
    """
    The :class:`QueryPluginProvider` returns the available plugins
    that can be used to query for a DNS record. Eg. DNS, DOH, DOT
    """
    def get(self, plugin_ref, **kwargs):
        """
        Used to `get` a new or an existing plugin object.
        Eg. ```get('dns', **kwargs)``` will return a :class:`Query` object
        instance of the DNS plugin.

        :param plugin_ref: The name of the plugin to be called.
        :type plugin_ref: str
        :param **kwargs: The keyword arguments used to setup the required plugin.
        :type **kwargs: dict
        :return: The object instance of the requested plugin.
        :rtype: obj
        """
        return self.create(plugin_ref, **kwargs)

class ResponsePluginProvider(ObjectFactory):
    """
    The :class:`ResponsePluginProvider` returns the available plugins
    that can be used to render the query response into various outputs.
    """
    def get(self, plugin_ref, **kwargs):
        """
        Used to `get` a new or an existing plugin object.
        Eg. ```get('dig', **kwargs)``` will return a :class:`Response` object 
        instance of the dig output plugin.

        :param plugin_ref: The name of the plugin to be called.
        :type plugin_ref: str
        :param **kwargs: The keyword arguments used to setup the required plugin.
        :type **kwargs: dict
        :return: The object instance of the requested plugin.
        :rtype: obj
        """
        return self.create(plugin_ref, **kwargs)
