# Dockerfile

# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.9
# Allows docker to cache installed dependencies between builds
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy .env file
COPY .env /dap/.env
# Mounts the application code to the image
COPY . code
WORKDIR /code

EXPOSE 8000

# runs the production server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
