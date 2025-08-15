# RAG System Testing Framework

This directory contains comprehensive tests for the RAG (Retrieval-Augmented Generation) system.

## Test Structure

- **test_models.py**: Unit tests for data models (Course, Lesson, CourseChunk)
- **test_app.py**: API endpoint tests for FastAPI endpoints
- **conftest.py**: Shared fixtures and test utilities

## Running Tests

### All Tests
```bash
cd /path/to/project
PYTHONPATH=. uv run python -m pytest backend/tests/ -v --ignore=/opt/ros
```

### Specific Test Files
```bash
# Run model tests
PYTHONPATH=. uv run python -m pytest backend/tests/test_models.py -v

# Run API tests
PYTHONPATH=. uv run python -m pytest backend/tests/test_app.py -v
```

### Using the Test Runner
```bash
chmod +x run_tests.sh
./run_tests.sh
```

## Test Categories

### Unit Tests
- Data model validation
- Serialization/deserialization
- Edge cases and boundary conditions

### API Tests
- Endpoint functionality
- Request/response validation
- Error handling
- Performance checks

## Fixtures Available

- `test_config`: Test configuration with temporary directories
- `mock_course`: Mock course object
- `mock_course_chunks`: Mock course chunk objects
- `mock_rag_system`: Mock RAG system
- `mock_session_manager`: Mock session manager
- `mock_vector_store`: Mock vector store
- `mock_ai_generator`: Mock AI generator
- `test_client`: Test client for FastAPI app

## Test Markers

- `@pytest.mark.unit`: Unit tests
- `@pytest.mark.integration`: Integration tests
- `@pytest.mark.api`: API endpoint tests
- `@pytest.mark.slow`: Slow-running tests

## Environment Setup

Tests run in an isolated environment using temporary directories to avoid interference with production data.

## Test Data

All test data is created dynamically using fixtures and temporary files, ensuring clean test runs without external dependencies.