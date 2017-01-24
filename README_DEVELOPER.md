# Developer Readme

This readme will be for anyone interested in developing for the gradiusbot program. This includes plugins or core code changes.

## Previous Pasting

### Plugins

Every file in the private_plugins and public_plugins folder are loaded as a module and is imported.

After every message, each public message is sent to every public_plugin, and each private message is sent to every private_plugin.

### Design

The plugin file should contain an action method that takes a [Discord Message](https://github.com/Rapptz/discord.py/blob/master/discord/message.py) and send message callback function.

The plugin will process the message and use the callback function to send messages if needed.
