# Dockerfile to build a gradiusbot docker container

# Set the base image to Python3
FROM python:3

# Set the working directory
WORKDIR /usr/src/app

# File Author
MAINTAINER gradiuscypher

# Copy the requirements.txt and install them
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the installed libraries to the Docker container
COPY . .

# Execute the the command
CMD ["python", "gradiusbot.py", "config.conf"]
