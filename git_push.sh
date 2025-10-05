#!/bin/bash
# Usage:
# ./git_push.sh <remote_url> [--tag v1.0.0] [--push-ghcr]
# Example:
# ./git_push.sh https://github.com/yourusername/ai-companion.git --tag v1.0.0 --push-ghcr

set -e
if [ -z "$1" ]; then
  echo "Please provide remote repo URL as first argument."
  exit 1
fi
remote=$1
shift

tag=""
push_ghcr=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --tag) tag="$2"; shift 2 ;;
    --push-ghcr) push_ghcr=true; shift ;;
    *) echo "Unknown option $1"; exit 1 ;;
  esac
done

git init
git add .
git commit -m "Final submission: AI Companion complete"
git branch -M main
git remote add origin "$remote"
if [ -n "$tag" ]; then
  git tag "$tag"
fi
echo "Repository initialized. Push with:"
echo "  git push -u origin main"
if [ -n "$tag" ]; then
  echo "  git push origin $tag"
fi
if [ "$push_ghcr" = true ]; then
  echo "To push Docker images to GHCR, create a personal access token with write:packages scope and set it as GHCR_TOKEN secret in GitHub."
  echo "The CI workflow will build & push images to ghcr.io when you push to GitHub."
fi
