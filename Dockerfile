# Use the official Python image as the base image
FROM python:3.11-slim

# Set environment variables
ENV APP_HOME /app

# Set the working directory in the container
WORKDIR $APP_HOME

# Copy the current directory contents into the container at /app
COPY . $APP_HOME

# Install any dependencies
RUN pip install uv
RUN uv venv
RUN uv pip sync requirements.txt

# Command to run the Python application
CMD ["./gradiusbot.py"]
