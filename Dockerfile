# Use the official Python image as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that the Flask app will run on
EXPOSE 5000

# Use Gunicorn to serve the app, binding it to port 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]

