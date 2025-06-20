#!/bin/bash

# Define the image name and tag
IMAGE_NAME="webvoyager-webbench-env"
IMAGE_TAG="latest"

echo "Building Docker image: ${IMAGE_NAME}:${IMAGE_TAG}"

# Build the Docker image using the Dockerfile.webbench
# The -f flag specifies the Dockerfile to use
# The . at the end specifies the build context (current directory)
docker build -f Dockerfile.webbench -t ${IMAGE_NAME}:${IMAGE_TAG} .

if [ $? -eq 0 ]; then
    echo "Docker image built successfully: ${IMAGE_NAME}:${IMAGE_TAG}"
else
    echo "Error: Docker image build failed."
    exit 1
fi