# discord_gradiusbot
Currently in the process of being re-written. More documentation coming soon!

## Running gradiusbot with Docker
To run discord_gradiusbot and it's plugins in Docker, we'll need to build the container and launch it with a few configuration flags. Theses flags depend on what plugins you want to run.

### Setting up a Discord bot account
* Head over to the [Discord Developers](https://discord.com/developers/applications) page to create yourself a Discord application
* Click the "New Application" button in the top right
* Give the Application a name, usually the name of your bot is a fine name. Read the ToS.
* Click the "Bot" subsection on the left side of the webpage (it's a puzzle icon)
* Click the "Add Bot" button to create your bot credentials
* Edit your bot name to something fitting for its duties
* Under "Click to Reveal Token" click the "Copy" button to copy your bot's authentication token to your clipboard.
* Disable the "Public Bot" switch unless you want other people to be able to invite your bot.

### Inviting your bot to your Discord server
* Open the [Discord API Permissions Calculator](https://discordapi.com/permissions.html)
* Check any of the checkboxes related to the permission you want your bot to have. Some plugins require more permissions than others. For example, the `url_checker` plugin will require at least "Manage Messages"
* On the Discord Developers page, click the "General Information" section for your bot and click the "Copy" button next to the "CLIENT ID" section
* Paste this CLIENT ID into the "Client ID" section of the Permissions Calculator
* Click the link at the bottom of the page to be redirected to Discord's site, where it'll ask you which server you want to invite your bot
* Chose the server you want to invite it to, and click Continue

### Getting the discord_gradiusbot code and building the Docker container
This is how you get the code responsible for running gradiusbot. These instructions are only tested in Ubuntu, but should work for any Linux system with `git` and `docker` installed.

```
git clone https://github.com/gradiuscypher/discord_gradiusbot.git
cd discord_gradiusbot
docker build -t gradiusbot . --no-cache
```

### Editing the gradiusbot configuration
* Copy the example config file to a new config file: `cp config.conf.example config.conf`
* **Note**: you can run more than one instance of the `discord_gradiusbot` container if you create uniquely named config files
* Edit the config file:
  * Paste the Bot Token value that was copied from the Discord Developer site during the instructions above. Do not wrap the value in quotes.
  * Add the names of any plugins that you'd like to run to their respective section, include the name in DOUBLE QUOTES only. Separate values by comma.
    * For example, if you'd like to run the `url_checker` plugin, your `public_plugins` section would look like this:
    ```
    # Plugins
    public_plugins = ["url_checker"]
    ```

### Launching an instance of the discord_gradiusbot container
* Ensure that your container has been built by following the instructions above
* Run this `docker` command to launch a container. Any time you make configuration changes to either config.conf or plugin configs, you will need to restart the container
```
docker run -d -it --name BOT_NAME -v /PATH/TO/config.conf:/discord_gradiusbot/botconfig.conf --restart always gradiusbot
```
* Include any edited plugin files as volumes by adding `-v` switches. For example, if you wanted to include your JSON file for the `url_checker` plugin, you'd run this docker command:
```
docker run -d -it --name BOT_NAME -v /PATH/TO/config.conf:/discord_gradiusbot/botconfig.conf -v /PATH/TO/DISCORD_GRADIUSBOT_GIT/public_plugins/url_checker/url_checker.json:/discord_gradiusbot/public_plugins/url_checker/url_checker.json --restart always gradiusbot
```
