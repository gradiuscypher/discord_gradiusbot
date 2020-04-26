# discord_gradiusbot with Docker

## Building the Docker image
```bash
cd REPO_DIRECTORY
docker build -t gradiusbot . --no-cache
```

## Running the Docker image
Use this command. Set up any additional files with `-v` to add volumes. The bot runs from `/discord_gradiusbot/`

```bash
touch /PATH/TO/LOCAL/LOGGING/BOTNAME.log
docker run -d -it --name BOT_NAME -v /PATH/TO/CONFIG.conf:/discord_gradiusbot/botconfig.conf -v /PATH/TO/LOCAL/LOGGING/botname.log:/discord_gradiusbot/gradiusbot.log --restart always gradiusbot-docker
```
