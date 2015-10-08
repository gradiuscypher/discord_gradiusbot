from importlib import import_module
import os


class PluginLoader:

    def __init__(self):
        self.public_plugins = []
        self.private_plugins = []
        self.methods = []
        self.public_plugin_dir = 'public_plugins'
        self.private_plugin_dir = 'private_plugins'

    def load_plugins(self):
        # Load public plugins
        count = 0
        possible_plugins = os.listdir('public_plugins')

        for plugin in possible_plugins:
            location = os.path.join(self.public_plugin_dir, plugin)

            if not os.path.isdir(location):
                plugin_name = plugin.replace('.py', '')
                if "_" in plugin_name[0]:
                    print("ignoring this plugin: " + plugin_name)
                else:
                    self.public_plugins.append(import_module(self.public_plugin_dir + "." + plugin_name))
                    count += 1

        print("Loaded " + str(count) + " public plugins.")

        # Load private plugins
        count = 0
        possible_plugins = os.listdir('private_plugins')

        for plugin in possible_plugins:
            location = os.path.join(self.private_plugin_dir, plugin)

            if not os.path.isdir(location):
                plugin_name = plugin.replace('.py', '')
                if "_" in plugin_name[0]:
                    print("ignoring this plugin: " + plugin_name)
                else:
                    self.private_plugins.append(import_module(self.private_plugin_dir + "." + plugin_name))
                    count += 1

        print("Loaded " + str(count) + " private plugins.")
