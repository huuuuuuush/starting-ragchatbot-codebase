# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Retrieval-Augmented Generation (RAG) system for querying course materials using semantic search and AI-powered responses. Built with FastAPI backend and vanilla JavaScript frontend.

## Architecture

### Core Components
- **RAGSystem** (`backend/rag_system.py`): Main orchestrator coordinating document processing, vector storage, AI generation, and session management
- **VectorStore** (`backend/vector_store.py`): ChromaDB-based vector storage with separate collections for course metadata and content
- **DocumentProcessor** (`backend/document_processor.py`): Processes course documents into structured chunks
- **AIGenerator** (`backend/ai_generator.py`): Claude AI integration for generating responses
- **SessionManager** (`backend/session_manager.py`): Manages conversation history and sessions
- **SearchTools** (`backend/search_tools.py`): Tool-based search functionality for AI queries

### Data Flow
1. Documents processed into Course objects with Lessons and CourseChunks
2. Course metadata stored in `course_catalog` collection (semantic search for course discovery)
3. Course content chunks stored in `course_content` collection (semantic search for answers)
4. AI queries use tool-based search to retrieve relevant content, then generate contextual responses

## Key Commands

### Development
```bash
# Quick start - runs backend server
chmod +x run.sh
./run.sh

# Manual start
uv sync  # Install dependencies
cd backend && uv run uvicorn app:app --reload --port 8000
```

### Environment Setup
```bash
# Create .env file
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### Testing
- Web interface: http://localhost:8000
- API docs: http://localhost:8000/docs

## File Structure

```
├── backend/                 # FastAPI backend
│   ├── app.py              # Main FastAPI application
│   ├── rag_system.py       # Core RAG orchestrator
│   ├── vector_store.py     # ChromaDB vector storage
│   ├── document_processor.py
│   ├── ai_generator.py
│   ├── session_manager.py
│   ├── search_tools.py
│   ├── models.py           # Data models
│   └── config.py           # Configuration
├── frontend/               # Vanilla JS frontend
│   ├── index.html
│   ├── script.js
│   └── style.css
├── docs/                   # Course materials (PDF, DOCX, TXT)
├── main.py                 # Entry point (minimal)
├── run.sh                  # Quick start script
└── pyproject.toml          # Dependencies (uv)
```

## Key Configuration

- **Vector Storage**: ChromaDB with persistent storage at `./chroma_db`
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2
- **AI Model**: Claude via Anthropic API
- **Chunking**: 1000 tokens with 200 token overlap
- **Max Results**: 5 results per semantic search

## API Endpoints

- `POST /api/query` - Query course materials
- `GET /api/courses` - Get course statistics
- `GET /docs` - Swagger API documentation

## Dependencies

Managed via `uv` (Python package manager):
- chromadb==1.0.15
- anthropic==0.58.2
- sentence-transformers==5.0.0
- fastapi==0.116.1
- uvicorn==0.35.0

## Data Model

- **Course**: Title, instructor, course_link, lessons[]
- **Lesson**: lesson_number, title, lesson_link
- **CourseChunk**: content, course_title, lesson_number, chunk_index
- 在所有可以使用中文的地方都尽量使用中文回复
Application/chrome.exe