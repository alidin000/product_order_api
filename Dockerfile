# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Install netcat (netcat-openbsd)
RUN apt-get update && apt-get install -y netcat-openbsd && apt-get clean

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port on which the app will run
EXPOSE 8000

# Copy the migration script
COPY ./docker-entrypoint.sh /usr/local/bin/

# Make the migration script executable
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Command to run the application with the entrypoint
ENTRYPOINT ["docker-entrypoint.sh"]
