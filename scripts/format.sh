#!/bin/bash
set -e

echo "🔧 Running code formatting..."

# Format Python code with black
echo "🎨 Formatting Python code with Black..."
uv run black backend/

# Sort imports with isort
echo "📦 Sorting imports with isort..."
uv run isort backend/

echo "✅ Code formatting complete!"