# Dockerfile to build a discord_gradiusbot container
# docker build --tag gradiusbot . --no-cache
# docker run -d -it --name gradiusbot -v "$(pwd)"/config.conf:/discord_gradiusbot/botconfig.conf gradiusbot

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

# touch the logfile so we can mount it
RUN touch /discord_gradiusbot/gradiusbot.log

# install the requirements
RUN pip install --no-cache-dir -r requirements.txt

# Run gradiusbot.py with the config file passed as a volume
CMD ["python", "gradiusbot.py", "botconfig.conf"]
