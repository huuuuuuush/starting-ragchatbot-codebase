#!/bin/bash

# Test runner script for the RAG system

echo "Setting up test environment..."

# Install test dependencies
echo "Installing test dependencies..."
uv sync --extra dev

# Run tests
echo "Running tests..."
uv run pytest backend/tests/ -v --tb=short

# Run tests with coverage
echo "Running tests with coverage..."
uv run pytest backend/tests/ --cov=backend --cov-report=term-missing --cov-report=html --cov-report=xml

echo "Test run complete!"