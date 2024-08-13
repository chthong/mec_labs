#!/bin/bash

# Prompt for the base URL
read -p "Enter the base URL API: " BASE_URL

# Save the base URL to a file (optional)
echo $BASE_URL > base_url.txt

# Define the endpoint (you can change this as needed)
ENDPOINT="/queries/users?address=10.100.0.3"

# Execute the curl command and format the JSON output
curl -s "${BASE_URL}${ENDPOINT}" | jq .
