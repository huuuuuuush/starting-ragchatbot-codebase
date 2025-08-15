"""
Unit tests for data models in the RAG system.
"""

import pytest
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.models import Course, Lesson, CourseChunk


class TestCourseModel:
    """Tests for Course model."""

    def test_course_creation(self):
        """Test basic course creation."""
        course = Course(
            title="Machine Learning Fundamentals",
            instructor="Dr. Smith",
            course_link="https://example.com/ml-course",
            lessons=[]
        )
        
        assert course.title == "Machine Learning Fundamentals"
        assert course.instructor == "Dr. Smith"
        assert course.course_link == "https://example.com/ml-course"
        assert course.lessons == []

    def test_course_with_lessons(self):
        """Test course creation with lessons."""
        lessons = [
            Lesson(lesson_number=1, title="Introduction", lesson_link="/lesson1"),
            Lesson(lesson_number=2, title="Advanced Topics", lesson_link="/lesson2")
        ]
        
        course = Course(
            title="Test Course",
            instructor="Test Instructor",
            course_link="/test-course",
            lessons=lessons
        )
        
        assert len(course.lessons) == 2
        assert course.lessons[0].lesson_number == 1
        assert course.lessons[1].title == "Advanced Topics"

    def test_course_to_dict(self):
        """Test course serialization to dict."""
        course = Course(
            title="Test",
            instructor="Test",
            course_link="/test",
            lessons=[Lesson(lesson_number=1, title="Test Lesson", lesson_link="/test/lesson1")]
        )
        
        course_dict = course.dict()
        assert course_dict["title"] == "Test"
        assert course_dict["lessons"][0]["lesson_number"] == 1


class TestLessonModel:
    """Tests for Lesson model."""

    def test_lesson_creation(self):
        """Test basic lesson creation."""
        lesson = Lesson(
            lesson_number=1,
            title="Introduction to Python",
            lesson_link="/course/python/lesson1"
        )
        
        assert lesson.lesson_number == 1
        assert lesson.title == "Introduction to Python"
        assert lesson.lesson_link == "/course/python/lesson1"

    def test_lesson_to_dict(self):
        """Test lesson serialization to dict."""
        lesson = Lesson(
            lesson_number=2,
            title="Data Structures",
            lesson_link="/course/python/lesson2"
        )
        
        lesson_dict = lesson.dict()
        assert lesson_dict["lesson_number"] == 2
        assert lesson_dict["title"] == "Data Structures"


class TestCourseChunkModel:
    """Tests for CourseChunk model."""

    def test_chunk_creation(self):
        """Test basic chunk creation."""
        chunk = CourseChunk(
            content="This is a test chunk of content.",
            course_title="Test Course",
            lesson_number=1,
            chunk_index=0
        )
        
        assert chunk.content == "This is a test chunk of content."
        assert chunk.course_title == "Test Course"
        assert chunk.lesson_number == 1
        assert chunk.chunk_index == 0

    def test_chunk_to_dict(self):
        """Test chunk serialization to dict."""
        chunk = CourseChunk(
            content="Test content",
            course_title="Test Course",
            lesson_number=3,
            chunk_index=5
        )
        
        chunk_dict = chunk.dict()
        assert chunk_dict["content"] == "Test content"
        assert chunk_dict["course_title"] == "Test Course"
        assert chunk_dict["lesson_number"] == 3
        assert chunk_dict["chunk_index"] == 5

    def test_chunk_with_long_content(self):
        """Test chunk with long content."""
        long_content = "a" * 1000
        chunk = CourseChunk(
            content=long_content,
            course_title="Long Content Course",
            lesson_number=1,
            chunk_index=0
        )
        
        assert len(chunk.content) == 1000
        assert chunk.content == long_content

    def test_chunk_metadata_includes_all_fields(self):
        """Test chunk includes all necessary metadata."""
        chunk = CourseChunk(
            content="Sample content",
            course_title="Advanced ML",
            lesson_number=5,
            chunk_index=10
        )
        
        expected_fields = {"content", "course_title", "lesson_number", "chunk_index"}
        actual_fields = set(chunk.dict().keys())
        assert expected_fields.issubset(actual_fields)