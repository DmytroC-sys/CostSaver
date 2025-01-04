# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables to avoid interactive prompts during package installations
ENV PYTHONUNBUFFERED 1
ENV AWS_ACCESS_KEY_ID=<your_aws_access_key_id>
ENV AWS_SECRET_ACCESS_KEY=<your_aws_secret_access_key>
ENV AWS_REGION=us-west-1  # You can change this to your preferred AWS region

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 to be able to access the Flask app
EXPOSE 5000

# Define the command to run the app
CMD ["python", "app.py"]

