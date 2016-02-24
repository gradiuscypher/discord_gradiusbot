import os
import json
from importlib import import_module


class PluginLoader:

    def __init__(self):
        self.public_plugins = []
        self.private_plugins = []
        self.event_plugins = []
        self.public_plugin_dir = 'public_plugins'
        self.private_plugin_dir = 'private_plugins'
        self.event_plugin_dir = 'event_plugins'
        self.config = None
        self.public_plugin_config = None
        self.private_plugin_config = None
        self.event_plugin_config = None

    def load_plugins(self, config):
        self.config = config
        self.public_plugin_config = json.loads(self.config.get('BotSettings', 'public_plugins'))
        self.private_plugin_config = json.loads(self.config.get('BotSettings', 'private_plugins'))
        self.event_plugin_config = json.loads(self.config.get('BotSettings', 'event_plugins'))

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

        # Load event plugins
        count = 0

        for plugin in self.event_plugin_config:
            location = os.path.join(self.event_plugin_dir, plugin)

            if not os.path.isdir(location):
                plugin_name = plugin.replace('.py', '')
                self.event_plugins.append(import_module(self.event_plugin_dir + "." + plugin_name))
                count += 1

        print("Loaded " + str(count) + " event plugins.")
