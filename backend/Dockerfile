# Use the official Python 3.9 image from Docker Hub
FROM python:3.9

# Set the working directory in the container
WORKDIR /backend

# Copy the requirements file into the container at /app
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY app ./

# Expose the Flask port
EXPOSE 5000

# Run the Flask application
CMD ["python", "./app/app.py"]