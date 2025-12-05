"""
Test suite for the Animation Calculator Flask API
Tests all endpoints and calculation logic
"""

import pytest
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestHealthEndpoint:
    """Tests for the /health endpoint"""
    
    def test_health_endpoint_returns_ok(self, client):
        """Test that /health returns 200 with ok: true"""
        response = client.get('/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data == {"ok": True}


class TestCalculateEndpoint:
    """Tests for the /calculate endpoint"""
    
    def test_addition(self, client):
        """Test addition operation"""
        response = client.post('/calculate', 
                             json={'num1': 10, 'num2': 5, 'operator': '+'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['result'] == 15.0
    
    def test_subtraction(self, client):
        """Test subtraction operation"""
        response = client.post('/calculate',
                             json={'num1': 10, 'num2': 3, 'operator': '-'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['result'] == 7.0
    
    def test_multiplication(self, client):
        """Test multiplication operation"""
        response = client.post('/calculate',
                             json={'num1': 10, 'num2': 5, 'operator': '*'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['result'] == 50.0
    
    def test_division(self, client):
        """Test division operation"""
        response = client.post('/calculate',
                             json={'num1': 15, 'num2': 3, 'operator': '/'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['result'] == 5.0
    
    def test_power_operation(self, client):
        """Test power operation"""
        response = client.post('/calculate',
                             json={'num1': 2, 'num2': 8, 'operator': 'pow'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['result'] == 256.0
    
    def test_division_by_zero(self, client):
        """Test that division by zero returns 400"""
        response = client.post('/calculate',
                             json={'num1': 10, 'num2': 0, 'operator': '/'})
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'Division by zero' in data['error']
    
    def test_missing_num1(self, client):
        """Test that missing num1 returns 400"""
        response = client.post('/calculate',
                             json={'num2': 5, 'operator': '+'})
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'num1' in data['error']
    
    def test_missing_num2(self, client):
        """Test that missing num2 returns 400"""
        response = client.post('/calculate',
                             json={'num1': 10, 'operator': '+'})
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'num2' in data['error']
    
    def test_missing_operator(self, client):
        """Test that missing operator returns 400"""
        response = client.post('/calculate',
                             json={'num1': 10, 'num2': 5})
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'operator' in data['error']
    
    def test_invalid_operator(self, client):
        """Test that invalid operator returns 400"""
        response = client.post('/calculate',
                             json={'num1': 10, 'num2': 5, 'operator': 'invalid'})
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'Invalid operator' in data['error']
    
    def test_invalid_numbers(self, client):
        """Test that non-numeric input returns 400"""
        response = client.post('/calculate',
                             json={'num1': 'abc', 'num2': 'xyz', 'operator': '+'})
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'valid numbers' in data['error']
    
    def test_empty_request(self, client):
        """Test that empty request returns 400"""
        response = client.post('/calculate', json={})
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_decimal_operations(self, client):
        """Test decimal number operations"""
        response = client.post('/calculate',
                             json={'num1': 10.5, 'num2': 3.2, 'operator': '+'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['result'] == 13.7
    
    def test_negative_numbers(self, client):
        """Test operations with negative numbers"""
        response = client.post('/calculate',
                             json={'num1': -10, 'num2': 5, 'operator': '+'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['result'] == -5.0


class TestIndexEndpoint:
    """Tests for the / (index) endpoint"""
    
    def test_index_returns_html(self, client):
        """Test that / returns HTML content"""
        response = client.get('/')
        assert response.status_code == 200
        assert 'html' in response.content_type.lower()
        assert b'Animation Calculator' in response.data
