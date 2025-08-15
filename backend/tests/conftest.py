"""
Test configuration and shared fixtures for RAG system testing.
"""

import os
import sys
import tempfile
import pytest
from typing import Dict, Any, List
from unittest.mock import Mock, patch, MagicMock

# Add backend directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.models import Course, Lesson, CourseChunk
from backend.config import Config


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
def mock_rag_system():
    """Create a mock RAG system for testing."""
    mock_rag = Mock()
    
    # Mock query method
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
    
    # Mock get_course_analytics method
    mock_rag.get_course_analytics.return_value = {
        "total_courses": 2,
        "course_titles": ["Test Course 1", "Test Course 2"]
    }
    
    # Mock add_course_folder method
    mock_rag.add_course_folder.return_value = (1, 5)
    
    return mock_rag


@pytest.fixture
def mock_session_manager():
    """Create a mock session manager for testing."""
    mock_manager = Mock()
    mock_manager.create_session.return_value = "test-session-123"
    mock_manager.get_session.return_value = {"messages": []}
    mock_manager.add_message.return_value = None
    return mock_manager


@pytest.fixture
def mock_vector_store():
    """Create a mock vector store for testing."""
    mock_store = Mock()
    
    # Mock search methods
    mock_store.search_course_metadata.return_value = [
        {"title": "Test Course 1", "score": 0.95},
        {"title": "Test Course 2", "score": 0.87}
    ]
    
    mock_store.search_course_content.return_value = [
        {"content": "Test content", "metadata": {"course_title": "Test Course", "lesson_number": 1}, "score": 0.92}
    ]
    
    mock_store.add_course_metadata.return_value = None
    mock_store.add_course_chunks.return_value = None
    
    return mock_store


@pytest.fixture
def mock_ai_generator():
    """Create a mock AI generator for testing."""
    mock_ai = Mock()
    mock_ai.generate_response.return_value = "This is a generated test response"
    return mock_ai


@pytest.fixture
def sample_query_data():
    """Create sample query data for testing."""
    return {
        "query": "What is machine learning?",
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
    from fastapi.testclient import TestClient
    
    # Import here to avoid circular imports
    from .test_app import create_test_app
    
    app = create_test_app()
    client = TestClient(app)
    return client