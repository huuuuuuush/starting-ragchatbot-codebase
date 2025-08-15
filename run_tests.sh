#!/bin/bash

# Test runner script for RAG system tests

echo "🧪 Running RAG System Tests"
echo "========================"

# Install test dependencies if needed
if ! command -v pytest &> /dev/null; then
    echo "Installing pytest..."
    pip install pytest pytest-asyncio httpx
fi

# Run all tests
echo "Running all tests..."
cd backend
python -m pytest tests/ -v

# Run specific test categories
echo ""
echo "Running API tests..."
python -m pytest tests/test_app.py -v

echo ""
echo "Running model tests..."
python -m pytest tests/test_models.py -v

echo ""
echo "✅ All tests completed!"

# Optional: Run with coverage (if coverage is available)
if command -v coverage &> /dev/null; then
    echo ""
    echo "📊 Running with coverage..."
    coverage run -m pytest tests/
    coverage report -m
fi