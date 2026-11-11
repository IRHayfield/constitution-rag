#!/bin/bash

# Install script for Constitution RAG project

echo "Setting up Constitution RAG project..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "uv not found. Please install using a package manager."
    exit 1
fi

echo "Creating virtual environment with uv..."
uv venv

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing dependencies with uv..."
uv sync

echo "Setup complete!"
echo "To use the system, activate the environment with:"
echo "  source .venv/bin/activate"
echo "Then run demos with:"
echo "  python demo.py --setup-only"