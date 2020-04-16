# Dockerfile to build a discord_gradiusbot container
# TODO:
# install the bot from target git branch
# install prereqs
# start the bot
# load a config
# log to central logging using an environment variable

# Set the base image to Python3 
FROM python:3

# File author
MAINTAINER gradiuscypher

# Install Git
RUN apt update && apt install -y git

# Git clone the target branch of discord_gradiusbot from Github
# TODO: remove this so that we build off main later
RUN git clone --single-branch --branch dockerdeploy https://github.com/gradiuscypher/discord_gradiusbot.git --depth=1

# Set the working directory
WORKDIR discord_gradiusbot

# install the requirements
RUN pip install --no-cache-dir -r requirements.txt

# Run gradiusbot.py with the config file passed as a volume
CMD ["python", "gradiusbot.py", "botconfig.conf"]
