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

    def test_course_creation_basic(self):
        """Test basic course creation (original test)."""
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

    def test_course_to_dict_with_model_dump(self):
        """Test course serialization to dict (model_dump)."""
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

    def test_lesson_creation_basic(self):
        """Test basic lesson creation (original test)."""
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
            lesson_number=2,
            title="Data Structures",
            lesson_link="/course/python/lesson2"
        )
        
        lesson_dict = lesson.dict()
        assert lesson_dict["lesson_number"] == 2
        assert lesson_dict["title"] == "Data Structures"

    def test_lesson_to_dict_original(self):
        """Test lesson serialization to dict (original test)."""
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

    def test_chunk_creation_basic(self):
        """Test basic chunk creation (original test)."""
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

    def test_chunk_to_dict_original(self):
        """Test chunk serialization to dict (original test)."""
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

    def test_empty_strings_handled(self):
        """Test model handles empty strings appropriately."""
        chunk = CourseChunk(
            content="",
            course_title="",
            lesson_number=1,
            chunk_index=0
        )
        
        assert chunk.content == ""
        assert chunk.course_title == ""

    def test_zero_and_negative_values(self):
        """Test model handles zero and negative values."""
        chunk = CourseChunk(
            content="Test",
            course_title="Test Course",
            lesson_number=0,
            chunk_index=-1
        )
        
        assert chunk.lesson_number == 0
        assert chunk.chunk_index == -1


class TestModelIntegration:
    """Integration tests for models working together."""

    def test_course_with_multiple_lessons_and_chunks(self):
        """Test complete course structure with lessons and chunks."""
        lessons = [
            Lesson(lesson_number=1, title="Intro", lesson_link="/lesson1"),
            Lesson(lesson_number=2, title="Advanced", lesson_link="/lesson2")
        ]
        
        course = Course(
            title="Complete Course",
            instructor="Complete Instructor",
            course_link="/complete-course",
            lessons=lessons
        )
        
        chunks = [
            CourseChunk(
                content="Lesson 1 content",
                course_title=course.title,
                lesson_number=1,
                chunk_index=0
            ),
            CourseChunk(
                content="Lesson 2 content",
                course_title=course.title,
                lesson_number=2,
                chunk_index=0
            )
        ]
        
        assert len(course.lessons) == 2
        assert len(chunks) == 2
        assert chunks[0].course_title == course.title
        assert chunks[1].lesson_number == 2

    def test_serialization_consistency(self):
        """Test that serialization and deserialization are consistent."""
        original_course = Course(
            title="Serialization Test",
            instructor="Test Instructor",
            course_link="/test-link",
            lessons=[
                Lesson(lesson_number=1, title="Test Lesson", lesson_link="/test/lesson")
            ]
        )
        
        # Serialize
        course_dict = original_course.dict()
        
        # Deserialize (simulate)
        reconstructed_course = Course(**course_dict)
        
        assert reconstructed_course.title == original_course.title
        assert len(reconstructed_course.lessons) == len(original_course.lessons)
        assert reconstructed_course.lessons[0].title == original_course.lessons[0].title