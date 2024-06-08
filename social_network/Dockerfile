
### Dockerfile

Create a `Dockerfile` in the root directory of your project:

    ```Dockerfile
    # Use an official Python runtime as a base image
    FROM python:3.8
    
    # Set environment variables
    ENV PYTHONDONTWRITEBYTECODE 1
    ENV PYTHONUNBUFFERED 1
    
    # Set the working directory in the container
    WORKDIR /app
    
    # Copy the requirements file into the container
    COPY requirements.txt /app/
    
    # Install dependencies
    RUN pip install --no-cache-dir -r requirements.txt
    
    # Copy the rest of the application code into the container
    COPY . /app/
    
    # Expose the port the app runs on
    EXPOSE 8000
    
    # Set environment variable for Django settings
    ENV DJANGO_SETTINGS_MODULE=social_network.settings
    
    # Run the development server
    CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
    