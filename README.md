# Course Materials RAG System

A Retrieval-Augmented Generation (RAG) system designed to answer questions about course materials using semantic search and AI-powered responses.

## Overview

This application is a full-stack web application that enables users to query course materials and receive intelligent, context-aware responses. It uses ChromaDB for vector storage, Anthropic's Claude for AI generation, and provides a web interface for interaction.


## Prerequisites

- Python 3.13 or higher
- uv (Python package manager)
- An Anthropic API key (for Claude AI)
- **For Windows**: Use Git Bash to run the application commands - [Download Git for Windows](https://git-scm.com/downloads/win)

## Installation

1. **Install uv** (if not already installed)
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Install Python dependencies**
   ```bash
   uv sync
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```bash
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```

## Development Workflow

### Code Quality Tools

This project includes comprehensive code quality tools:
- **Black**: Automatic code formatting
- **isort**: Import sorting
- **flake8**: Code linting
- **mypy**: Type checking

### Running the Application

#### With Quality Checks (Recommended)
```bash
chmod +x scripts/*.sh
./scripts/dev.sh
```
This runs formatting, linting, and type checking before starting the server.

#### Quick Start (Standard)
```bash
chmod +x run.sh
./run.sh
```

#### Manual Start
```bash
cd backend
uv run uvicorn app:app --reload --port 8000
```

### Code Quality Commands

#### Format Code
```bash
./scripts/format.sh
```

#### Run Quality Checks
```bash
./scripts/lint.sh
```

#### Manual Commands
```bash
# Format with black
uv run black backend/

# Sort imports
uv run isort backend/

# Lint with flake8
uv run flake8 backend/

# Type checking
uv run mypy backend/
```

The application will be available at:
- Web Interface: `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`

