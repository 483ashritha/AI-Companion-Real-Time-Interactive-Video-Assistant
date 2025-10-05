#!/bin/bash
# Initialize git repo with basic commits for submission
git init
git add .
git commit -m "Initial commit: AI Companion final submission"
git branch -M main
echo "Repository initialized. Add remote and push:"
echo "  git remote add origin <your-repo-url>"
echo "  git push -u origin main"
