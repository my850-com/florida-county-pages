#!/bin/bash
# Deploy to GitHub Pages
# Run this after GitHub repo is set up

REPO_URL="https://github.com/my850-com/florida-county-pages.git"

echo "Setting up Florida County Pages deployment..."

# Configure git
git remote add origin $REPO_URL 2>/dev/null || echo "Remote already exists"

# Add all files
git add -A

# Commit
git commit -m "Initial: 67 county SEO pages generated $(date)"

echo ""
echo "To complete deployment:"
echo "  1. Create repo: https://github.com/my850-com/florida-county-pages"
echo "  2. Make it public"
echo "  3. Run: git push -u origin main"
echo "  4. Enable GitHub Pages in Settings > Pages"
echo ""
echo "Then site will be at: https://my850-com.github.io/florida-county-pages/"
