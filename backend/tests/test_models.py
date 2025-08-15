"""
Unit tests for data models.
"""

import pytest
from backend.models import Course, Lesson, CourseChunk


class TestCourseModel:
    """Test Course model."""
    
    def test_course_creation(self):
        """Test basic course creation."""
        course = Course(
            title="Test Course",
            instructor="Test Instructor",
            course_link="https://example.com",
            lessons=[
                Lesson(lesson_number=1, title="Lesson 1", lesson_link="https://example.com/1")
            ]
        )
        
        assert course.title == "Test Course"
        assert course.instructor == "Test Instructor"
        assert len(course.lessons) == 1
        assert course.lessons[0].lesson_number == 1
    
    def test_course_to_dict(self):
        """Test course serialization to dict."""
        course = Course(
            title="Test Course",
            instructor="Test Instructor",
            course_link="https://example.com",
            lessons=[
                Lesson(lesson_number=1, title="Lesson 1", lesson_link="https://example.com/1")
            ]
        )
        
        course_dict = course.model_dump()
        assert course_dict["title"] == "Test Course"
        assert course_dict["instructor"] == "Test Instructor"
        assert len(course_dict["lessons"]) == 1


class TestLessonModel:
    """Test Lesson model."""
    
    def test_lesson_creation(self):
        """Test basic lesson creation."""
        lesson = Lesson(
            lesson_number=1,
            title="Introduction",
            lesson_link="https://example.com/intro"
        )
        
        assert lesson.lesson_number == 1
        assert lesson.title == "Introduction"
        assert lesson.lesson_link == "https://example.com/intro"
    
    def test_lesson_to_dict(self):
        """Test lesson serialization to dict."""
        lesson = Lesson(
            lesson_number=1,
            title="Introduction",
            lesson_link="https://example.com/intro"
        )
        
        lesson_dict = lesson.model_dump()
        assert lesson_dict["lesson_number"] == 1
        assert lesson_dict["title"] == "Introduction"
        assert lesson_dict["lesson_link"] == "https://example.com/intro"


class TestCourseChunkModel:
    """Test CourseChunk model."""
    
    def test_course_chunk_creation(self):
        """Test basic course chunk creation."""
        chunk = CourseChunk(
            content="This is test content",
            course_title="Test Course",
            lesson_number=1,
            chunk_index=0
        )
        
        assert chunk.content == "This is test content"
        assert chunk.course_title == "Test Course"
        assert chunk.lesson_number == 1
        assert chunk.chunk_index == 0
    
    def test_course_chunk_to_dict(self):
        """Test course chunk serialization to dict."""
        chunk = CourseChunk(
            content="This is test content",
            course_title="Test Course",
            lesson_number=1,
            chunk_index=0
        )
        
        chunk_dict = chunk.model_dump()
        assert chunk_dict["content"] == "This is test content"
        assert chunk_dict["course_title"] == "Test Course"
        assert chunk_dict["lesson_number"] == 1
        assert chunk_dict["chunk_index"] == 0