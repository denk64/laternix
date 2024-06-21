#!/bin/bash

# Set variables
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
REPO="denk64/EVG-G_Label" # Replace with your GitHub username/repo
ARTIFACT_NAME="EVG-G-Converted"

# Authenticate GitHub CLI (uncomment if not authenticated)
# gh auth login

# Get the latest run ID
RUN_ID=$(gh run list --repo "$REPO" --limit 1 --json databaseId --jq '.[0].databaseId')
DOWNLOAD_DIR="artifacts/$ARTIFACT_NAME/$RUN_ID"

if [ -z "$RUN_ID" ]; then
  echo "Failed to get the latest run ID."
  exit 1
fi

echo "Latest Run ID: $RUN_ID"

# Download the latest artifact
gh run download "$RUN_ID" --repo "$REPO" --name "$ARTIFACT_NAME" --dir "$DOWNLOAD_DIR"

if [ $? -eq 0 ]; then
  echo "Artifact downloaded successfully to $DOWNLOAD_DIR"
else
  echo "Failed to download the artifact."
  exit 1
fi
