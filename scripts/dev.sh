#!/bin/bash
set -e

echo "🚀 Starting development workflow..."

# Run formatting first
echo "🎨 Running code formatting..."
./scripts/format.sh

# Then run quality checks
echo "🔍 Running quality checks..."
./scripts/lint.sh

echo "✅ Development checks complete! Starting server..."

# Start the backend server
cd backend && uv run uvicorn app:app --reload --port 8000