# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /code

# Install git


# Copy the rest of the working directory contents into the container at /code
COPY . /code/

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run manage.py to collect static files
RUN python manage.py collectstatic --noinput

# Define environment variable
ENV DJANGO_SETTINGS_MODULE=management_booklib.settings

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
