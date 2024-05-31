# Dockerize a python app
FROM python:3.11.8-slim

# Create app directory
WORKDIR /app

# Install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

#Copy app
COPY app .

# Run app
ENTRYPOINT ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
