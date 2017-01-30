# discord_gradiusbot
A gradiusbot for the Discord chat service. Both in-line documentation and these files are a work in progress. Gradiusbot is a Python bot that runs on a plugin system. The plugins are also written in Python.

## Developer Documentation

A link to the developer documentation can be found [HERE](README_DEVELOPER.md)

## User Documentation

### Installation and Setup

Note: This is a first pass at getting some setup instructions. These instructions may be incomplete.

```
pip install -r requirements.txt
```

### Configuration

The Discord bot token value. DO NOT SAVE THIS TO A PUBLIC CONFIGURATION.
```
[Account]
token =
```

#### Bot message control:

What is the bot's display name? This is required so that it doesn't reply to itself.
```
self_name =
```

Which channels is the bot allowed to read/write in?
```
permitted_channels = []
```


#### Various other settings:
```
[BotSettings]
server_id =
statuses = ["PM me !help for more info", "@RiotGradius on Twitter", "status1", "status2"]
```

* statuses: the statuses the bot displays where the active game would normally be.

#### Plugin Configuration
This is a list of strings. Each string is a filename found in the folders `private_plugins`, `public_plugins`, and `event_plugins`.

For example:
```
public_plugins = ["echo.py", "dice.py"]
```

All sections:
```
public_plugins = []
private_plugins = []
event_plugins = []
```

### Usage

`./gradiusbot.py config.conf`
