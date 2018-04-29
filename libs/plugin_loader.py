import os
import json
import logging
from importlib import import_module


class EventPlugin:
    def __init__(self):
        self.messages = []
        self.reactions = []
        self.guild = []
        self.member = []
        self.private_channels = []
        self.client = []


class PluginLoader:

    def __init__(self):
        # Setup Logging
        self.logger = logging.getLogger('gradiusbot')

        self.public_plugins = []
        self.private_plugins = []
        self.scheduled_tasks = []
        self.public_plugin_dir = 'public_plugins'
        self.private_plugin_dir = 'private_plugins'
        self.scheduled_tasks_dir = 'scheduled_tasks'
        self.config = None
        self.public_plugin_config = None
        self.private_plugin_config = None
        self.scheduled_tasks_config = None

        # Event Plugin Config
        self.event_plugins = EventPlugin()
        self.event_plugin_dir = 'event_plugins'
        self.message_event_plugin_config = None
        self.reaction_event_plugin_config = None
        self.private_event_plugin_config = None
        self.guild_event_plugin_config = None
        self.member_event_plugin_config = None
        self.client_event_plugin_config = None

    def load_plugins(self, config):
        self.config = config
        self.public_plugin_config = json.loads(self.config.get('gradiusbot', 'public_plugins'))
        self.private_plugin_config = json.loads(self.config.get('gradiusbot', 'private_plugins'))
        self.scheduled_tasks_config = json.loads(self.config.get('gradiusbot', 'scheduled_tasks'))

        # Event Plugin Config
        self.message_event_plugin_config = json.loads(self.config.get('gradiusbot', 'event_plugins.messages'))
        self.reaction_event_plugin_config = json.loads(self.config.get('gradiusbot', 'event_plugins.reactions'))
        self.private_event_plugin_config = json.loads(self.config.get('gradiusbot', 'event_plugins.private'))
        self.guild_event_plugin_config = json.loads(self.config.get('gradiusbot', 'event_plugins.guild'))
        self.member_event_plugin_config = json.loads(self.config.get('gradiusbot', 'event_plugins.member'))
        self.client_event_plugin_config = json.loads(self.config.get('gradiusbot', 'event_plugins.client'))

        # Load public plugins
        count = 0
        for plugin in self.public_plugin_config:
            plugin_file = plugin + '.py'
            location = os.path.join(self.public_plugin_dir, plugin, plugin_file)

            if not os.path.isdir(location):
                self.public_plugins.append(import_module(self.public_plugin_dir + '.' + plugin + '.' + plugin))
                count += 1
        self.logger.info("Loaded " + str(count) + " public plugins.")

        # Load private plugins
        count = 0
        for plugin in self.private_plugin_config:
            plugin_file = plugin + '.py'
            location = os.path.join(self.private_plugin_dir, plugin, plugin_file)

            if not os.path.isdir(location):
                self.private_plugins.append(import_module(self.private_plugin_dir + '.' + plugin + '.' + plugin))
                count += 1
        self.logger.info("Loaded " + str(count) + " private plugins.")

        # Load message event plugins
        count = 0
        for plugin in self.message_event_plugin_config:
            plugin_file = plugin + '.py'
            location = os.path.join(self.event_plugin_dir, 'messages', plugin, plugin_file)

            if not os.path.isdir(location):
                self.event_plugins.messages.append(import_module(self.event_plugin_dir + '.messages.' + plugin + '.' + plugin))
                count += 1
        self.logger.info("Loaded " + str(count) + " message event plugins.")

        # Load reaction event plugins
        count = 0
        for plugin in self.reaction_event_plugin_config:
            plugin_file = plugin + '.py'
            location = os.path.join(self.event_plugin_dir, 'reactions', plugin, plugin_file)

            if not os.path.isdir(location):
                self.event_plugins.reactions.append(import_module(self.event_plugin_dir + '.reactions.' + plugin + '.' + plugin))
                count += 1
        self.logger.info("Loaded " + str(count) + " reaction event plugins.")

        # Load private event plugins
        count = 0
        for plugin in self.private_event_plugin_config:
            plugin_file = plugin + '.py'
            location = os.path.join(self.event_plugin_dir, 'private', plugin, plugin_file)

            if not os.path.isdir(location):
                self.event_plugins.private_channels.append(import_module(self.event_plugin_dir + '.private.' + plugin + '.' + plugin))
                count += 1
        self.logger.info("Loaded " + str(count) + " private channel event plugins.")

        # Load guild event plugins
        count = 0
        for plugin in self.guild_event_plugin_config:
            plugin_file = plugin + '.py'
            location = os.path.join(self.event_plugin_dir, 'guild', plugin, plugin_file)

            if not os.path.isdir(location):
                self.event_plugins.guild.append(import_module(self.event_plugin_dir + '.guild.' + plugin + '.' + plugin))
                count += 1
        self.logger.info("Loaded " + str(count) + " guild event plugins.")

        # Load member event plugins
        count = 0
        for plugin in self.member_event_plugin_config:
            plugin_file = plugin + '.py'
            location = os.path.join(self.event_plugin_dir, 'member', plugin, plugin_file)

            if not os.path.isdir(location):
                self.event_plugins.member.append(import_module(self.event_plugin_dir + '.member.' + plugin + '.' + plugin))
                count += 1
        self.logger.info("Loaded " + str(count) + " member event plugins.")

        # Load member event plugins
        count = 0
        for plugin in self.client_event_plugin_config:
            plugin_file = plugin + '.py'
            location = os.path.join(self.event_plugin_dir, 'client', plugin, plugin_file)

            if not os.path.isdir(location):
                self.event_plugins.member.append(import_module(self.event_plugin_dir + '.client.' + plugin + '.' + plugin))
                count += 1
        self.logger.info("Loaded " + str(count) + " client event plugins.")

        # Load scheduled tasks
        count = 0
        for plugin in self.scheduled_tasks_config:
            plugin_file = plugin + '.py'
            location = os.path.join(self.scheduled_tasks_dir, plugin, plugin_file)

            if not os.path.isdir(location):
                self.scheduled_tasks.append(import_module(self.scheduled_tasks_dir + '.' + plugin + '.' + plugin))
                count += 1
        self.logger.info("Loaded " + str(count) + " scheduled tasks.")
