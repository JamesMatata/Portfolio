# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install system dependencies (you don't need MySQL dependencies anymore)
RUN apt-get update && apt-get install -y \
    build-essential \
    && apt-get clean

# Copy the requirements file
COPY requirements.txt /app/

# Install Python packages from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Django project
COPY . /app/

# Copy the .env file (if you're using environment variables, optional)
COPY .env /app/

# Copy the script to handle migrations and superuser creation
COPY ./docker-entrypoint.sh /app/docker-entrypoint.sh

# Make the script executable
RUN chmod +x /app/docker-entrypoint.sh

# Expose the port the app runs on
EXPOSE 8000

# Override CMD to run the entrypoint script
CMD ["/app/docker-entrypoint.sh"]
