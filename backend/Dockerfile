# Use the official Python 3.9 image from Docker Hub
FROM python:3.9

# Set the working directory in the container
WORKDIR /backend

# Copy the requirements file into the container at /backend
COPY ./requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY ./app ./app

# Expose the Flask port
EXPOSE 5000

# Health check to ensure the container is healthy
HEALTHCHECK --interval=30s --timeout=10s --retries=3 CMD curl --fail http://localhost:5000/health || exit 1

# Run the Flask application
CMD ["python", "./app/app.py"]
