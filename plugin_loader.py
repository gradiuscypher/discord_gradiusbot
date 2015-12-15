import os
import configparser
import json
from importlib import import_module


class PluginLoader:

    def __init__(self):
        self.public_plugins = []
        self.private_plugins = []
        self.methods = []
        self.public_plugin_dir = 'public_plugins'
        self.private_plugin_dir = 'private_plugins'

        config = configparser.RawConfigParser()
        config.read('config.conf')
        self.public_plugin_config = json.loads(config.get('Settings', 'public_plugins'))
        self.private_plugin_config = json.loads(config.get('Settings', 'private_plugins'))

    def load_plugins(self):
        # Load public plugins
        count = 0

        for plugin in self.public_plugin_config:
            location = os.path.join(self.public_plugin_dir, plugin)

            if not os.path.isdir(location):
                plugin_name = plugin.replace('.py', '')
                self.public_plugins.append(import_module(self.public_plugin_dir + "." + plugin_name))
                count += 1

        print("Loaded " + str(count) + " public plugins.")

        # Load private plugins
        count = 0

        for plugin in self.private_plugin_config:
            location = os.path.join(self.private_plugin_dir, plugin)

            if not os.path.isdir(location):
                plugin_name = plugin.replace('.py', '')
                self.private_plugins.append(import_module(self.private_plugin_dir + "." + plugin_name))
                count += 1

        print("Loaded " + str(count) + " private plugins.")
