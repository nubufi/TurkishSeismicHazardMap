FROM python:3.10-slim

WORKDIR /app

# Install other dependencies
COPY requirements.txt ./
RUN apt-get update
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the source code
COPY src .

# Expose the port for the app
EXPOSE 8000
