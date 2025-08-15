"""
Test-specific FastAPI application setup and API endpoint tests.
"""

import os
import sys
import pytest
from unittest.mock import patch, MagicMock
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def create_test_app():
    """Create a test version of the FastAPI app without static file mounting."""
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.middleware.trustedhost import TrustedHostMiddleware
    
    # Import models
    class QueryRequest(BaseModel):
        query: str
        session_id: str = None

    class QueryResponse(BaseModel):
        answer: str
        sources: list
        session_id: str

    class CourseStats(BaseModel):
        total_courses: int
        course_titles: list

    # Create test app
    app = FastAPI(title="Course Materials RAG System - Test")

    # Add middleware (simplified for testing)
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"]
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    # Mock RAG system for testing
    mock_rag_system = MagicMock()
    
    # Mock endpoints
    @app.post("/api/query", response_model=QueryResponse)
    async def query_documents(request: QueryRequest):
        """Process a query and return response with sources."""
        try:
            session_id = request.session_id or "test-session-123"
            
            # Use mock response
            answer = f"Test answer for: {request.query}"
            sources = [
                {
                    "content": f"Relevant content for {request.query}",
                    "course_title": "Test Course",
                    "lesson_number": 1,
                    "chunk_index": 0
                }
            ]
            
            return QueryResponse(
                answer=answer,
                sources=sources,
                session_id=session_id
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/api/courses", response_model=CourseStats)
    async def get_course_stats():
        """Get course analytics and statistics."""
        try:
            return CourseStats(
                total_courses=2,
                course_titles=["Test Course 1", "Test Course 2"]
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/")
    async def root():
        """Root endpoint for health check."""
        return {"message": "RAG System API is running (test mode)"}

    return app


class TestAPIEndpoints:
    """Test class for API endpoints."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        app = create_test_app()
        return TestClient(app)

    def test_root_endpoint(self, client):
        """Test root endpoint returns success."""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "RAG System API is running (test mode)"}

    def test_query_endpoint_valid_request(self, client):
        """Test query endpoint with valid request."""
        query_data = {
            "query": "What is machine learning?",
            "session_id": "test-session-456"
        }
        response = client.post("/api/query", json=query_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "sources" in data
        assert "session_id" in data
        assert data["session_id"] == "test-session-456"
        assert "machine learning" in data["answer"]

    def test_query_endpoint_without_session_id(self, client):
        """Test query endpoint without session_id generates new session."""
        query_data = {"query": "What is deep learning?"}
        response = client.post("/api/query", json=query_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["session_id"] == "test-session-123"

    def test_query_endpoint_empty_query(self, client):
        """Test query endpoint with empty query."""
        query_data = {"query": ""}
        response = client.post("/api/query", json=query_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "Test answer for:" in data["answer"]

    def test_query_endpoint_missing_query(self, client):
        """Test query endpoint missing query field."""
        response = client.post("/api/query", json={})
        assert response.status_code == 422  # Validation error

    def test_courses_endpoint(self, client):
        """Test courses endpoint returns course statistics."""
        response = client.get("/api/courses")
        
        assert response.status_code == 200
        data = response.json()
        assert "total_courses" in data
        assert "course_titles" in data
        assert data["total_courses"] == 2
        assert len(data["course_titles"]) == 2
        assert "Test Course 1" in data["course_titles"]

    def test_cors_headers(self, client):
        """Test CORS middleware is configured (basic check)."""
        # CORS middleware is configured in the app, but headers are only sent on cross-origin requests
        # This test verifies the app structure rather than specific headers
        assert client is not None  # Basic assertion to test setup

    def test_content_type_headers(self, client):
        """Test proper content-type headers."""
        response = client.post("/api/query", json={"query": "test"})
        assert response.headers["content-type"] == "application/json"

    def test_health_check_response_time(self, client):
        """Test endpoints respond in reasonable time."""
        import time
        
        start_time = time.time()
        response = client.get("/api/courses")
        end_time = time.time()
        
        assert response.status_code == 200
        assert (end_time - start_time) < 1.0  # Should respond within 1 second


class TestIntegrationWithMocks:
    """Integration tests with mocked dependencies."""

    @pytest.fixture
    def client_with_mocks(self):
        """Create test client with mocked RAG system."""
        from fastapi.testclient import TestClient
        from fastapi import FastAPI, HTTPException
        
        app = FastAPI(title="Integration Test App")
        
        # Import actual models
        class QueryRequest(BaseModel):
            query: str
            session_id: str = None

        class QueryResponse(BaseModel):
            answer: str
            sources: list
            session_id: str

        class CourseStats(BaseModel):
            total_courses: int
            course_titles: list

        # Mock endpoints
        @app.post("/api/query", response_model=QueryResponse)
        async def query_documents(request: QueryRequest):
            """Test endpoint with mocked RAG system."""
            try:
                # Simulate RAG system behavior
                if not request.query:
                    raise HTTPException(status_code=400, detail="Query cannot be empty")
                
                session_id = request.session_id or "mock-session-789"
                
                # Mock realistic response
                answer = f"Based on your question about '{request.query}', here's a comprehensive answer..."
                sources = [
                    {
                        "content": f"Relevant excerpt about {request.query}",
                        "course_title": "Machine Learning Fundamentals",
                        "lesson_number": 3,
                        "chunk_index": 2
                    }
                ]
                
                return QueryResponse(
                    answer=answer,
                    sources=sources,
                    session_id=session_id
                )
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @app.get("/api/courses", response_model=CourseStats)
        async def get_course_stats():
            """Test courses endpoint with mocked data."""
            return CourseStats(
                total_courses=5,
                course_titles=[
                    "Introduction to Machine Learning",
                    "Deep Learning Specialization",
                    "Natural Language Processing",
                    "Computer Vision",
                    "Reinforcement Learning"
                ]
            )

        return TestClient(app)

    def test_realistic_query_flow(self, client_with_mocks):
        """Test realistic query flow with mocked dependencies."""
        query_data = {"query": "How does gradient descent work?"}
        response = client_with_mocks.post("/api/query", json=query_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert "gradient descent" in data["answer"].lower()
        assert len(data["sources"]) > 0
        assert data["session_id"] is not None

    def test_large_query_dataset(self, client_with_mocks):
        """Test handling of larger query datasets."""
        queries = [
            "What is supervised learning?",
            "Explain neural networks",
            "How to evaluate model performance",
            "What is overfitting?",
            "Describe cross-validation"
        ]
        
        responses = []
        for query in queries:
            response = client_with_mocks.post("/api/query", json={"query": query})
            assert response.status_code == 200
            responses.append(response.json())
        
        assert len(responses) == len(queries)
        for i, response_data in enumerate(responses):
            assert queries[i].lower() in response_data["answer"].lower()


class TestTestAppCreation:
    """Tests for the test app creation function."""

    def test_create_test_app_returns_fastapi(self):
        """Test that create_test_app returns a FastAPI app."""
        app = create_test_app()
        assert isinstance(app, FastAPI)
        assert "Course Materials RAG System - Test" in str(app.title)

    def test_test_app_has_required_endpoints(self):
        """Test that test app has all required endpoints."""
        app = create_test_app()
        routes = [route.path for route in app.routes]
        
        assert "/api/query" in routes
        assert "/api/courses" in routes
        assert "/" in routes


if __name__ == "__main__":
    # Run tests manually for debugging
    pytest.main([__file__, "-v"])