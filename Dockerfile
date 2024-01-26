# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Install necessary packages
RUN apt-get update && apt-get install -y redis-server

# Copy the current directory contents into the container
COPY ./src /app

COPY ./requirements.txt requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the ports for Dash and Redis
EXPOSE 8080 6379

# Run the Cisco AnyConnect VPN client and Redis server
CMD ["bash", "-c", "redis-server & python app.py"]