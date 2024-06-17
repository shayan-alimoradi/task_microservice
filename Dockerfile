# Use the official Python image from the Alpine variant
FROM python:3.10-alpine

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /src/ 

# Install Python dependencies
COPY requirements.txt /src/
RUN pip install -U pip
RUN pip install -r requirements.txt

# Copy the application code
COPY . /src/

# Expose the application port
EXPOSE 8000
