#!/bin/bash

# Function to prompt for the base URL and save it to .env
save_base_url() {
    read -p "Enter the base URL API: " BASE_URL
    echo "BASE_URL=${BASE_URL}" > .env
}

# Check if .env file exists
if [ -f ".env" ]; then
    # Load the base URL from the .env file
    source .env
    echo "Using base URL from .env: $BASE_URL"
else
    # Prompt for the base URL and save it to .env if not found
    save_base_url
fi

# Define the endpoint (you can change this as needed)
ENDPOINT="/queries/users?address=10.100.0.3"

# Execute the curl command and format the JSON output
curl -s "${BASE_URL}${ENDPOINT}" | jq .
