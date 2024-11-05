# Dockerfile for Python script
FROM python:3.9-slim

# Install psycopg2 dependencies
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*
# Install psycopg2
RUN pip install psycopg2 django pandas

RUN pip freeze  
# Set the working directory
WORKDIR /app

# Copy the Python script into the container
COPY main.py .

# Run the Python script
CMD ["python", "main.py"]
