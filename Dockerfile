# Use an official Node.js 14 Alpine image as a parent image
FROM node:14-alpine

# Set the working directory
WORKDIR /usr/src/app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install production dependencies.
RUN npm install
RUN npm ci --only=production
RUN apk add --no-cache bash
RUN apk add --no-cache python3

# Copy the local code to the container's work directory
COPY . .

# Copy wait-for-it.sh from your local directory to the container
COPY wait-for-it-script/wait-for-it.sh .

# Make wait-for-it.sh executable
RUN chmod +x wait-for-it.sh

# Inform Docker that the container listens on port 5000 at runtime.
EXPOSE 5000

# Define the command to run the app
CMD [ "node", "src/index.js" ]
