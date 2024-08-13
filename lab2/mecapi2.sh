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

# Define the endpoint and query parameters (you can change these as needed)
ENDPOINT="/queries/distance"
QUERY_PARAMS="?address=10.100.0.2&address=10.100.0.1"

# Full URL
FULL_URL="${BASE_URL}${ENDPOINT}${QUERY_PARAMS}"

# Execute the curl command with the necessary headers and format the JSON output
curl -s -X GET "${FULL_URL}" -H "accept: application/json" | jq .
