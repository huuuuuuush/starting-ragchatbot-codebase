"""
Test configuration and shared fixtures for RAG system tests.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any, List
import pytest
from unittest.mock import Mock, MagicMock, AsyncMock

# Add backend directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from fastapi.testclient import TestClient
from sentence_transformers import SentenceTransformer

# Import backend modules
from backend.models import Course, Lesson, CourseChunk
from backend.rag_system import RAGSystem
from backend.vector_store import VectorStore
from backend.ai_generator import AIGenerator
from backend.document_processor import DocumentProcessor
from backend.session_manager import SessionManager
from backend.config import Config


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


@pytest.fixture
def test_config():
    """Create test configuration with temporary directories."""
    with tempfile.TemporaryDirectory() as temp_dir:
        config = Config()
        config.chroma_db_path = os.path.join(temp_dir, "test_chroma_db")
        config.chunk_size = 100
        config.chunk_overlap = 20
        config.max_results = 3
        yield config


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
def mock_course():
    """Create a mock course for testing."""
    return Course(
        title="Test Course",
        instructor="Test Instructor",
        course_link="https://example.com/test-course",
        lessons=[
            Lesson(
                lesson_number=1,
                title="Introduction",
                lesson_link="https://example.com/test-course/lesson1"
            ),
            Lesson(
                lesson_number=2,
                title="Advanced Topics",
                lesson_link="https://example.com/test-course/lesson2"
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
def mock_course_chunks():
    """Create mock course chunks for testing."""
    return [
        CourseChunk(
            content="This is the first chunk of test content for lesson 1.",
            course_title="Test Course",
            lesson_number=1,
            chunk_index=0
        ),
        CourseChunk(
            content="This is the second chunk of test content for lesson 1.",
            course_title="Test Course",
            lesson_number=1,
            chunk_index=1
        ),
        CourseChunk(
            content="This is content for lesson 2 about advanced topics.",
            course_title="Test Course",
            lesson_number=2,
            chunk_index=0
        )
    ]


@pytest.fixture
def mock_ai_generator():
    """Create a mock AI generator for testing."""
    mock_ai = Mock()
    mock_ai.generate_response = AsyncMock(return_value="This is a generated test response")
    
    # Also create a MagicMock version for more detailed testing
    detailed_mock = MagicMock(spec=AIGenerator)
    detailed_mock.generate_response = AsyncMock(return_value={
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
    
    return detailed_mock


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
    
    # Also add newer mock methods
    mock_store.search_course_metadata = AsyncMock(return_value=[
        {"title": "Test Course 1", "score": 0.95},
        {"title": "Test Course 2", "score": 0.87}
    ])
    
    mock_store.search_course_content = AsyncMock(return_value=[
        {"content": "Test content", "metadata": {"course_title": "Test Course", "lesson_number": 1}, "score": 0.92}
    ])
    
    mock_store.add_course_metadata = AsyncMock(return_value=None)
    mock_store.add_course_chunks = AsyncMock(return_value=None)
    
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
    
    # Also add newer mock methods
    mock.create_session = AsyncMock(return_value="test-session-123")
    mock.get_session = AsyncMock(return_value={"messages": []})
    mock.add_message = AsyncMock(return_value=None)
    
    return mock


@pytest.fixture
def mock_rag_system():
    """Create a mock RAG system for testing."""
    mock_rag = Mock()
    
    mock_rag.query.return_value = (
        "This is a test answer",
        [
            {
                "content": "Test content 1",
                "course_title": "Test Course",
                "lesson_number": 1,
                "chunk_index": 0
            },
            {
                "content": "Test content 2",
                "course_title": "Test Course",
                "lesson_number": 2,
                "chunk_index": 0
            }
        ]
    )
    
    mock_rag.get_course_analytics.return_value = {
        "total_courses": 2,
        "course_titles": ["Test Course 1", "Test Course 2"]
    }
    
    mock_rag.add_course_folder.return_value = (1, 5)
    
    return mock_rag


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


@pytest.fixture
def sample_course_stats():
    """Create sample course statistics for testing."""
    return {
        "total_courses": 3,
        "course_titles": [
            "Introduction to Machine Learning",
            "Advanced Deep Learning",
            "Data Science Fundamentals"
        ]
    }


@pytest.fixture
def temp_course_folder():
    """Create a temporary folder with sample course documents."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create sample documents
        doc1_path = os.path.join(temp_dir, "course1.txt")
        with open(doc1_path, "w") as f:
            f.write("Machine Learning Course\nThis course covers the fundamentals of machine learning.")
        
        doc2_path = os.path.join(temp_dir, "course2.txt")
        with open(doc2_path, "w") as f:
            f.write("Deep Learning Course\nThis course explores advanced neural networks.")
        
        yield temp_dir


@pytest.fixture
def test_client():
    """Create a test client for FastAPI app testing."""
    # Import here to avoid circular imports
    from .test_app import create_test_app
    
    app = create_test_app()
    client = TestClient(app)
    return client