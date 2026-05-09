#!/bin/bash
# Deploy script for Blog Publisher
# Builds the package and pushes to GitHub

set -e

echo "Building Blog Publisher..."

# Install build tools
pip install --upgrade build twine

# Clean previous builds
rm -rf build/ dist/ *.egg-info

# Build package
python -m build

echo "Build complete: dist/"

# Check if we should publish to PyPI
if [ "$1" == "--pypi" ]; then
    echo "Publishing to PyPI..."
    twine upload dist/*
else
    echo "To publish to PyPI, run: $0 --pypi"
fi

echo "Done!"
