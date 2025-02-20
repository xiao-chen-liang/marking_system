# Use the official MySQL 8.0 image from Docker Hub
FROM mysql:8.4.0

# Set the environment variables
ENV MYSQL_ROOT_PASSWORD=rootpassword
ENV MYSQL_DATABASE=postgraduate

# Copy the SQL file into the Docker container
COPY postgraduate_data.sql /docker-entrypoint-initdb.d/

# Expose the default MySQL port to the host
EXPOSE 3306
