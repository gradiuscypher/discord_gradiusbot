# Developer Readme

This readme will be for anyone interested in developing for the gradiusbot program. This includes plugins or core code changes.

# 10,000 Foot Overview

Gradiusbot is a python program that connects to Discord and waits for messages and events to come through. Each message or event is then run through various processing modules imported at runtime.

The core event tracking logic is all contained in [gradiusbot.py](gradiusbot.py). When a Discord event fires and we have logic for interacting with it, that event is run through the list of processing modules related to its type that have been enabled in the configuration file. Each module has an `action` function that takes various arguments depending on the event type.

There are 3 different event types: public, private, and event. Each of those then is sent to different lists of modules.

# Plugins

Every module can do many things. It can interact with the Discord services using the `client` object. For example, when a message/event matches a string, you can send a message to a specific channel. You can also do anything else that a normal Discord client can do, within its permissions on that server.

## Example Plugins
* [Event Plugin](event_plugins/example_event_plugin.py)
* [Public Plugin](public_plugins/echo.py)
* [Private Plugin](private_plugins/example_private_plugin.py)

## Event Plugins

These plugins interact with Discord events (eg: member joins/parts, message deletes).  These plugins take the arguments:
* `event_object` - The [discord.py](http://discordpy.readthedocs.io/en/latest/index.html) event object.
* `client` - The discord.py Discord [client](http://discordpy.readthedocs.io/en/latest/api.html#client) object.
* `config` - The config object. Used for global configuration
* `event_type` - A string that defines which event is being triggered. Is used in the plugin to determine when to process an event.
* `object_after` - Used in some events, for example a message edit or namechange

## Public Plugins

These plugins interact with the messages that people send to a channel. They take these arguments:
* `message` - The discord.py [message](http://discordpy.readthedocs.io/en/latest/api.html#message) object.
* `client` - The discord.py Discord [client](http://discordpy.readthedocs.io/en/latest/api.html#client) object.
* `config` - The config object. Used for global configuration.

## Private Plugins

These plugins interact with PMs sent to the bot. It's arguments are the same as the public plugins.
