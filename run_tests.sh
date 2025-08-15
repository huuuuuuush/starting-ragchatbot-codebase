#!/bin/bash

# Test runner script for RAG system tests

echo "🧪 Running RAG System Tests"
echo "========================"

# Ensure script is executable
chmod +x "$0"

# Install test dependencies
echo "📦 Installing test dependencies..."
uv sync --group dev

# Run all tests
echo "🔍 Running all tests..."
uv run pytest backend/tests/ -v --tb=short

# Run tests with coverage
echo "📊 Running tests with coverage..."
uv run pytest backend/tests/ --cov=backend --cov-report=term-missing --cov-report=html --cov-report=xml

# Run specific test categories
echo ""
echo "🔍 Running API tests..."
uv run pytest backend/tests/test_app.py -v

echo ""
echo "🔍 Running model tests..."
uv run pytest backend/tests/test_models.py -v

# Check if tests passed
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ All tests passed successfully!"
    echo "📈 Coverage report available at: htmlcov/index.html"
else
    echo ""
    echo "❌ Some tests failed. Please check the output above."
    exit 1
fi

# Optional: Run linting
echo ""
echo "🔍 Running code quality checks..."
uv run black --check backend/
uv run isort --check-only backend/
uv run flake8 backend/

echo ""
echo "🎉 Test suite completed!"