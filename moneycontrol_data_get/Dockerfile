# Use an official Python runtime as a base image
FROM python:3.11.9-slim

# Set the working directory in the container to /app
WORKDIR /app

# Install virtualenv
RUN pip install --upgrade pip
RUN pip install virtualenv

# Create a virtual environment named "venv" in /app
RUN virtualenv venv

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the Python dependencies into the virtual environment
RUN . venv/bin/activate && pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Command to activate virtual environment and run your Python script
CMD . venv/bin/activate && python scraper.py 
