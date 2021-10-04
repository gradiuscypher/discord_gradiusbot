import os
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
        self.relationships = []
        self.group = []


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
        self.relationships_event_plugin_config = None
        self.group_event_plugin_config = None

    def load_plugins(self, config):
        self.config = config
        self.public_plugin_config = config['public_plugins']
        self.private_plugin_config = config['private_plugins']
        self.scheduled_tasks_config = config['scheduled_tasks']

        # Event Plugin Config
        self.message_event_plugin_config = config['event_plugins']['messages']
        self.reaction_event_plugin_config = config['event_plugins']['reactions']
        self.private_event_plugin_config = config['event_plugins']['private']
        self.guild_event_plugin_config = config['event_plugins']['guild']
        self.member_event_plugin_config = config['event_plugins']['member']
        self.client_event_plugin_config = config['event_plugins']['client']
        self.relationships_event_plugin_config = config['event_plugins']['relationships']
        self.group_event_plugin_config = config['event_plugins']['group']

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

        # Load client event plugins
        count = 0
        for plugin in self.client_event_plugin_config:
            plugin_file = plugin + '.py'
            location = os.path.join(self.event_plugin_dir, 'client', plugin, plugin_file)

            if not os.path.isdir(location):
                self.event_plugins.member.append(import_module(self.event_plugin_dir + '.client.' + plugin + '.' + plugin))
                count += 1
        self.logger.info("Loaded " + str(count) + " client event plugins.")

        # Load relationship event plugins
        count = 0
        for plugin in self.relationships_event_plugin_config:
            plugin_file = plugin + '.py'
            location = os.path.join(self.event_plugin_dir, 'relationships', plugin, plugin_file)

            if not os.path.isdir(location):
                self.event_plugins.relationships.append(import_module(self.event_plugin_dir + '.relationships.' + plugin + '.' + plugin))
                count += 1
        self.logger.info("Loaded " + str(count) + " relationship event plugins.")

        # Load group event plugins
        count = 0
        for plugin in self.group_event_plugin_config:
            plugin_file = plugin + '.py'
            location = os.path.join(self.event_plugin_dir, 'group', plugin, plugin_file)

            if not os.path.isdir(location):
                self.event_plugins.group.append(import_module(self.event_plugin_dir + '.group.' + plugin + '.' + plugin))
                count += 1
        self.logger.info("Loaded " + str(count) + " group event plugins.")

        # Load scheduled tasks
        count = 0
        for plugin in self.scheduled_tasks_config:
            plugin_file = plugin + '.py'
            location = os.path.join(self.scheduled_tasks_dir, plugin, plugin_file)

            if not os.path.isdir(location):
                self.scheduled_tasks.append(import_module(self.scheduled_tasks_dir + '.' + plugin + '.' + plugin))
                count += 1
        self.logger.info("Loaded " + str(count) + " scheduled tasks.")
