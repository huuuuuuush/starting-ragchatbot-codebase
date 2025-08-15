"""
Test configuration and shared fixtures for RAG system tests.
"""

import os
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any, List
import pytest
from unittest.mock import MagicMock, AsyncMock

from fastapi.testclient import TestClient
from sentence_transformers import SentenceTransformer

# Import backend modules
from backend.models import Course, Lesson, CourseChunk
from backend.rag_system import RAGSystem
from backend.vector_store import VectorStore
from backend.ai_generator import AIGenerator
from backend.document_processor import DocumentProcessor
from backend.session_manager import SessionManager


@pytest.fixture(scope="session")
def test_data_dir():
    """Create a temporary directory for test data."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture(scope="session")
def chroma_db_path(test_data_dir):
    """Create a temporary ChromaDB path."""
    return os.path.join(test_data_dir, "test_chroma_db")


@pytest.fixture(scope="session")
def mock_sentence_transformer():
    """Mock sentence transformer for testing."""
    mock_model = MagicMock(spec=SentenceTransformer)
    
    def mock_encode(texts, **kwargs):
        if isinstance(texts, str):
            texts = [texts]
        # Return fixed-size embeddings
        return [[0.1] * 384 for _ in texts]
    
    mock_model.encode.side_effect = mock_encode
    return mock_model


@pytest.fixture
def sample_course():
    """Create a sample course for testing."""
    return Course(
        title="Introduction to Python Programming",
        instructor="Dr. Jane Smith",
        course_link="https://example.com/python-course",
        lessons=[
            Lesson(
                lesson_number=1,
                title="Python Basics",
                lesson_link="https://example.com/python-basics"
            ),
            Lesson(
                lesson_number=2,
                title="Data Structures",
                lesson_link="https://example.com/data-structures"
            ),
            Lesson(
                lesson_number=3,
                title="Object-Oriented Programming",
                lesson_link="https://example.com/oop"
            )
        ]
    )


@pytest.fixture
def sample_course_chunks(sample_course):
    """Create sample course chunks for testing."""
    course = sample_course
    chunks = []
    
    chunk_content = [
        "Python is a high-level programming language known for its simplicity and readability.",
        "It supports multiple programming paradigms including procedural, object-oriented, and functional programming.",
        "Python's syntax emphasizes code readability with its notable use of significant whitespace.",
        "Lists in Python are ordered, mutable collections of items. They can contain different data types.",
        "Dictionaries are unordered collections of key-value pairs, providing fast lookups by key.",
        "Classes in Python are blueprints for creating objects with shared attributes and methods.",
        "Inheritance allows classes to inherit attributes and methods from parent classes.",
    ]
    
    for i, content in enumerate(chunk_content):
        chunk = CourseChunk(
            content=content,
            course_title=course.title,
            lesson_number=(i // 3) + 1,
            chunk_index=i
        )
        chunks.append(chunk)
    
    return chunks


@pytest.fixture
def mock_ai_generator():
    """Create a mock AI generator for testing."""
    mock = MagicMock(spec=AIGenerator)
    
    # Mock generate_response method
    mock.generate_response = AsyncMock(return_value={
        "response": "This is a mock AI response for testing purposes.",
        "sources": [
            {
                "course_title": "Introduction to Python Programming",
                "lesson_number": 1,
                "chunk_index": 0,
                "content": "Python is a high-level programming language..."
            }
        ]
    })
    
    return mock


@pytest.fixture
def mock_vector_store():
    """Create a mock vector store for testing."""
    mock_store = MagicMock(spec=VectorStore)
    
    # Mock search methods
    mock_store.search_courses = AsyncMock(return_value=[
        {
            "course": {
                "title": "Introduction to Python Programming",
                "instructor": "Dr. Jane Smith",
                "course_link": "https://example.com/python-course"
            },
            "score": 0.95
        }
    ])
    
    mock_store.search_content = AsyncMock(return_value=[
        {
            "chunk": {
                "content": "Python is a high-level programming language...",
                "course_title": "Introduction to Python Programming",
                "lesson_number": 1,
                "chunk_index": 0
            },
            "score": 0.92
        }
    ])
    
    mock_store.get_course_stats = AsyncMock(return_value={
        "total_courses": 5,
        "total_lessons": 15,
        "total_chunks": 350
    })
    
    return mock_store


@pytest.fixture
def mock_document_processor():
    """Create a mock document processor for testing."""
    mock = MagicMock(spec=DocumentProcessor)
    mock.process_document = AsyncMock(return_value=sample_course())
    return mock


@pytest.fixture
def mock_session_manager():
    """Create a mock session manager for testing."""
    mock = MagicMock(spec=SessionManager)
    
    # Mock session methods
    mock.create_session = MagicMock(return_value="test-session-123")
    mock.get_session = MagicMock(return_value={
        "session_id": "test-session-123",
        "history": [
            {"role": "user", "content": "What is Python?"},
            {"role": "assistant", "content": "Python is a programming language..."}
        ]
    })
    mock.update_session = MagicMock()
    
    return mock


@pytest.fixture
def test_rag_system(mock_vector_store, mock_ai_generator, mock_session_manager):
    """Create a test RAG system with mocked dependencies."""
    rag_system = RAGSystem(
        vector_store=mock_vector_store,
        ai_generator=mock_ai_generator,
        session_manager=mock_session_manager
    )
    return rag_system


@pytest.fixture
def test_client():
    """Create a test client for the FastAPI app."""
    from backend.tests.test_app import test_app
    return TestClient(test_app)


@pytest.fixture
def sample_query_data():
    """Sample query data for API testing."""
    return {
        "query": "What is Python and how does it work?",
        "session_id": None
    }


@pytest.fixture
def sample_query_with_session():
    """Sample query data with session ID."""
    return {
        "query": "Tell me more about Python lists",
        "session_id": "test-session-123"
    }