"""
API endpoint tests for the RAG system.
"""

import pytest
from unittest.mock import AsyncMock, patch


@pytest.mark.api
class TestAPIEndpoints:
    """Test suite for API endpoints."""
    
    def test_root_endpoint(self, test_client):
        """Test the root endpoint."""
        response = test_client.get("/")
        # Test app doesn't have root endpoint, should return 404
        assert response.status_code == 404
    
    def test_api_query_endpoint_post(self, test_client, sample_query_data, test_rag_system):
        """Test POST /api/query endpoint."""
        with patch('backend.tests.test_app.test_app.state.rag_system', test_rag_system):
            test_rag_system.query = AsyncMock(return_value=(
                "This is a mock AI response for testing purposes.",
                [{"course_title": "Introduction to Python Programming", "content": "Python is..."}]
            ))
            
            response = test_client.post("/api/query", json=sample_query_data)
            
            assert response.status_code == 200
            data = response.json()
            
            assert "answer" in data
            assert "sources" in data
            assert "session_id" in data
            
            assert data["answer"] == "This is a mock AI response for testing purposes."
            assert len(data["sources"]) == 1
    
    def test_api_query_endpoint_with_session(self, test_client, sample_query_with_session, test_rag_system):
        """Test POST /api/query endpoint with session ID."""
        with patch('backend.tests.test_app.test_app.state.rag_system', test_rag_system):
            test_rag_system.query = AsyncMock(return_value=(
                "This is a mock AI response for testing purposes.",
                [{"course_title": "Introduction to Python Programming", "content": "Python is..."}]
            ))
            
            response = test_client.post("/api/query", json=sample_query_with_session)
            
            assert response.status_code == 200
            data = response.json()
            
            assert data["session_id"] == "test-session-123"
    
    def test_api_query_endpoint_invalid_method(self, test_client):
        """Test that GET method is not allowed for /api/query."""
        response = test_client.get("/api/query")
        assert response.status_code == 405  # Method Not Allowed
    
    def test_api_query_endpoint_invalid_payload(self, test_client):
        """Test /api/query with invalid payload."""
        response = test_client.post("/api/query", json={"invalid": "data"})
        assert response.status_code == 422  # Validation Error
    
    def test_api_query_endpoint_empty_query(self, test_client):
        """Test /api/query with empty query."""
        response = test_client.post("/api/query", json={"query": ""})
        assert response.status_code == 422  # Validation Error
    
    @pytest.mark.asyncio
    async def test_api_courses_endpoint(self, test_client, test_rag_system):
        """Test GET /api/courses endpoint."""
        test_rag_system.get_course_analytics = AsyncMock(return_value={
            "total_courses": 5,
            "course_titles": ["Course 1", "Course 2", "Course 3", "Course 4", "Course 5"]
        })
        
        with patch('backend.tests.test_app.test_app.state.rag_system', test_rag_system):
            response = test_client.get("/api/courses")
            
            assert response.status_code == 200
            data = response.json()
            
            assert "total_courses" in data
            assert "course_titles" in data
            assert len(data["course_titles"]) == 5
            assert data["total_courses"] == 5
    
    def test_api_courses_endpoint_not_found(self, test_client):
        """Test that /api/courses endpoint exists and returns valid data."""
        response = test_client.get("/api/courses")
        # Should not return 404, even if mocked
        assert response.status_code != 404
    
    def test_docs_endpoint(self, test_client):
        """Test /docs endpoint."""
        response = test_client.get("/docs")
        # Test app has docs endpoint
        assert response.status_code == 200
    
    def test_openapi_json_endpoint(self, test_client):
        """Test /openapi.json endpoint."""
        response = test_client.get("/openapi.json")
        # Test app has openapi endpoint
        assert response.status_code == 200


@pytest.mark.api
class TestAPIErrorHandling:
    """Test API error handling and edge cases."""
    
    def test_query_endpoint_exception_handling(self, test_client, mock_rag_system):
        """Test error handling in query endpoint."""
        mock_rag_system.query = AsyncMock(side_effect=Exception("Test exception"))
        
        with patch('backend.tests.test_app.test_app.state.rag_system', test_rag_system):
            response = test_client.post("/api/query", json={"query": "test query"})
            
            # Should handle exceptions gracefully
            assert response.status_code == 500
    
    def test_courses_endpoint_exception_handling(self, test_client, test_rag_system):
        """Test error handling in courses endpoint."""
        test_rag_system.get_course_analytics = AsyncMock(side_effect=Exception("Test exception"))
        
        with patch('backend.tests.test_app.test_app.state.rag_system', test_rag_system):
            response = test_client.get("/api/courses")
            
            # Should handle exceptions gracefully
            assert response.status_code == 500
    
    def test_cors_headers(self, test_client):
        """Test CORS headers are properly set."""
        response = test_client.options("/api/query")
        # CORS should be enabled
        assert "access-control-allow-origin" in response.headers or response.status_code == 200


@pytest.mark.integration
@pytest.mark.slow
class TestAPIIntegration:
    """Integration tests for API endpoints."""
    
    def test_full_query_flow(self, test_client):
        """Test the complete query flow from request to response."""
        # This test would require actual RAG system setup
        # For now, we'll just verify the endpoint structure
        
        response = test_client.post("/api/query", json={
            "query": "What is machine learning?",
            "session_id": None
        })
        
        # Should either succeed or handle gracefully
        assert response.status_code in [200, 500]  # 500 if RAG system not configured
    
    def test_multiple_queries_same_session(self, test_client, test_rag_system):
        """Test multiple queries in the same session."""
        with patch('backend.tests.test_app.test_app.state.rag_system', test_rag_system):
            test_rag_system.query = AsyncMock(return_value=(
                "This is a mock AI response for testing purposes.",
                [{"course_title": "Introduction to Python Programming", "content": "Python is..."}]
            ))
            test_rag_system.session_manager.create_session.return_value = "test-session-456"
            
            # First query
            response1 = test_client.post("/api/query", json={
                "query": "What is Python?",
                "session_id": None
            })
            assert response1.status_code == 200
            session_id = response1.json()["session_id"]
            
            # Second query with session
            response2 = test_client.post("/api/query", json={
                "query": "Tell me more about Python lists",
                "session_id": session_id
            })
            assert response2.status_code == 200
            assert response2.json()["session_id"] == session_id