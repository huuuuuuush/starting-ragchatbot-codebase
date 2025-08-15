#!/bin/bash
set -e

echo "🔍 Running code quality checks..."

# Run black to check formatting
echo "🎨 Checking code formatting with Black..."
uv run black backend/ --check

# Check import sorting
echo "📦 Checking import sorting with isort..."
uv run isort backend/ --check-only

# Run flake8 for linting
echo "🔍 Running linting with flake8..."
uv run flake8 backend/

# Run type checking
echo "🎯 Running type checking with mypy..."
uv run mypy backend/

echo "✅ All quality checks passed!"