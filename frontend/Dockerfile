# Use the official Node.js image from the Docker Hub
FROM node:14

# Create and change to the app directory
WORKDIR /usr/src/app

# Copy package.json and package-lock.json files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code, except node_modules
COPY . .

# Expose the port that the application will run on
EXPOSE 8080

# Define the command to run the application
CMD ["npm", "run", "serve"]
