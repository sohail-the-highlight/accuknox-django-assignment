# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements.txt file first to leverage Docker cache
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to /app
COPY . /app/

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable for Django settings module
ENV DJANGO_SETTINGS_MODULE=social_network.settings

# Run the Django server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "social_network.wsgi:application"]
