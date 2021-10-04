# Dockerfile to build a discord_gradiusbot container
# docker build --tag gradiusbot . --no-cache
# docker run -d -it --name gradiusbot -v "$(pwd)"/config.conf:/discord_gradiusbot/botconfig.conf gradiusbot

# Set the base image to Python3 
FROM python:latest

# File author
MAINTAINER gradiuscypher

# Install Git
RUN apt update && apt install -y git

# Git clone the target branch of discord_gradiusbot from Github
# RUN git clone --branch master --single-branch https://github.com/gradiuscypher/discord_gradiusbot.git --depth=1

# Copy the local files to the app directory
COPY event_plugins/ /discord_gradiusbot/private_plugins
COPY libs/ /discord_gradiusbot/libs
COPY private_plugins/ /discord_gradiusbot/private_plugins
COPY public_plugins/ /discord_gradiusbot/public_plugins
COPY scheduled_tasks/ /discord_gradiusbot/scheduled_tasks
COPY gradiusbot.py /discord_gradiusbot/gradiusbot.py
COPY requirements.txt /discord_gradiusbot/requirements.txt

# Set the working directory
WORKDIR /discord_gradiusbot

# touch the logfile so we can mount it
RUN touch /discord_gradiusbot/gradiusbot.json

# install the requirements
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run gradiusbot.py with the config file passed as a volume
CMD ["python", "gradiusbot.py", "botconfig.conf"]
