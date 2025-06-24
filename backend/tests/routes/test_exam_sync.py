import asyncio
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from unigate.main import app
from unigate.utils.exam_sync import sync_exam_results

client: TestClient = TestClient(app)

test_student_username = "S1234567"
test_student_password = "testpassword"


def authenticate_user() -> dict:
    """Authenticate a test user and return the access token."""
    login_payload = {
        "username": test_student_username,
        "password": test_student_password,
    }

    response = client.post("/auth/login", data=login_payload)
    assert response.status_code == 200, (
        f"Failed to authenticate user: {response.json()}"
    )
    return response.json()


def test_sync_exam_results_success() -> None:
    """Test that exam sync works correctly with valid university stub response."""
    
    mock_response_data = {
        "course": "Test Course",
        "date": "2025-01-01",
        "enrolled": [1234567, 4891185],
        "passed": [1234567]
    }
    
    with patch('httpx.AsyncClient.get') as mock_get:
        mock_get.return_value = AsyncMock()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = AsyncMock(return_value=mock_response_data)
        
        asyncio.run(sync_exam_results())
        
        assert mock_get.called, "HTTP request should have been made"


def test_sync_exam_results_university_stub_unavailable() -> None:
    """Test that exam sync handles university stub unavailability gracefully."""
    
    with patch('httpx.AsyncClient.get') as mock_get:
        mock_get.return_value = AsyncMock()
        mock_get.return_value.status_code = 500
        
        try:
            asyncio.run(sync_exam_results())
        except Exception as e:
            assert False, f"sync_exam_results should handle errors gracefully, but got: {e}"
        
        assert mock_get.called, "HTTP request should have been made"


def test_sync_exam_results_invalid_response() -> None:
    """Test that exam sync handles invalid response data gracefully."""
    
    mock_response_data = {
        "course": "Test Course",
        "date": "2025-01-01",
    }
    
    with patch('httpx.AsyncClient.get') as mock_get:
        mock_get.return_value = AsyncMock()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = AsyncMock(return_value=mock_response_data)
        
        try:
            asyncio.run(sync_exam_results())
        except Exception as e:
            assert False, f"sync_exam_results should handle invalid data gracefully, but got: {e}"
        
        assert mock_get.called, "HTTP request should have been made"


def test_exam_results_endpoint_returns_data() -> None:
    """Test that exam results are accessible through API after sync."""
    token_data = authenticate_user()
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    with patch('httpx.AsyncClient.get') as mock_get:
        mock_get.return_value = AsyncMock()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = AsyncMock(return_value={
            "course": "Test Course",
            "date": "2025-01-01",
            "enrolled": [1234567, 4891185],
            "passed": [1234567]
        })
        
        asyncio.run(sync_exam_results())

    response = client.get("/courses", headers=headers)
    assert response.status_code == 200, (
        f"Expected status code 200, but got {response.status_code}"
    )
    
    data = response.json()
    assert len(data) > 0, "Should return at least one course"
    
    test_course = next((course for course in data if course["name"] == "Test Course"), None)
    assert test_course is not None, "Test Course should exist in the response"


def test_sync_exam_results_with_multiple_courses() -> None:
    """Test that exam sync works with multiple courses."""
    
    mock_responses = [
        AsyncMock(return_value={
            "course": "Test Course",
            "date": "2025-01-01",
            "enrolled": [1234567, 4891185],
            "passed": [1234567]
        }),
        AsyncMock(return_value={
            "course": "Capstone",
            "date": "2025-02-03",
            "enrolled": [1234567, 4989646],
            "passed": [1234567, 4989646]
        })
    ]
    def side_effect(*args, **kwargs):
        if side_effect.counter < len(mock_responses):
            resp = mock_responses[side_effect.counter]
            side_effect.counter += 1
            return resp()
        return AsyncMock(return_value={})()
    side_effect.counter = 0
    with patch('httpx.AsyncClient.get') as mock_get:
        mock_get.return_value = AsyncMock()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.side_effect = side_effect
        asyncio.run(sync_exam_results())
        assert mock_get.call_count >= 2, "Should make requests for multiple courses"


def test_sync_exam_results_network_timeout() -> None:
    """Test that exam sync handles network timeouts gracefully."""
    with patch('httpx.AsyncClient.get') as mock_get:
        mock_get.side_effect = Exception("Connection timeout")
        try:
            asyncio.run(sync_exam_results())
        except Exception as e:
            assert False, f"sync_exam_results should not crash on network error, but got: {e}"
        assert mock_get.called, "HTTP request should have been attempted" 