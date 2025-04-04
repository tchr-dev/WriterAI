#!/bin/zsh

# Set the name of your remote repository
REMOTE_REPO="git@github.com:tchr-dev/WriterAI.git"

# Initialize the local repository
git init

# Add all files in the current directory to the repository
git add .

# Commit the files
git commit -m "Initial commit"

# Add your remote repository URL
git remote add origin $REMOTE_REPO

# Ensure the branch is named 'main'
git branch -M main

# Push the changes to the remote repository
git push -u origin main
