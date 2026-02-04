import pytest
import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:5000/api"

# Provide base API URL
@pytest.fixture(scope="session")
def api_url():
    return BASE_URL

# Reset data before each test
@pytest.fixture(scope="function")
def reset_data(api_url):
    response = requests.post(f"{api_url}/reset")
    assert response.status_code == 200
    yield


# Provide sample movie data
@pytest.fixture(scope="session")
def sample_movie():
    return {
        "movie_name": "Avatar",
        "language": "English",
        "duration": "2h 42m",
        "price": 300
    }

# Provide sample booking data    
@pytest.fixture(scope="session")
def sample_booking():
    return {
        "movie_id": 101,
        "customer_name": "John Doe",
        "seats": 2,
        "show_time": "7:00 PM"
    }

# Test cases for Movie CRUD operations    
class TestMovieAPI:    
    # Test GET /api/movies - Retrieve all movies
    def test_get_all_movies(self, api_url, reset_data):
        response = requests.get(f"{api_url}/movies")        
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert 'data' in data
        assert 'count' in data
        assert isinstance(data['data'], list)
        assert data['count'] == len(data['data'])
        assert data['count'] == 3
    
    # Test GET /api/movies/<id> - Get existing movie
    def test_get_movie_by_id_success(self, api_url, reset_data):
        movie_id = 101
        response = requests.get(f"{api_url}/movies/{movie_id}")
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert 'data' in data
        movie = data['data']
        assert movie['id'] == movie_id
        assert movie['movie_name'] == "Interstellar"
        assert 'language' in movie
        assert 'duration' in movie
        assert 'price' in movie
    
    # Test GET /api/movies/<id> - Non-existent movie
    def test_get_movie_by_id_not_found(self, api_url, reset_data):
        movie_id = 9999
        response = requests.get(f"{api_url}/movies/{movie_id}")
        assert response.status_code == 404
        data = response.json()
        assert data['success'] is False
        assert 'error' in data
        assert str(movie_id) in data['error']
    
    # Test POST /api/movies - Add new movie successfully
    def test_add_movie_success(self, api_url, reset_data, sample_movie):
        response = requests.post(
            f"{api_url}/movies",
            json=sample_movie,
            headers={'Content-Type': 'application/json'}
        )
        assert response.status_code == 201
        data = response.json()
        assert data['success'] is True
        assert 'data' in data
        assert 'message' in data
        movie = data['data']
        assert 'id' in movie
        assert movie['movie_name'] == sample_movie['movie_name']
        assert movie['language'] == sample_movie['language']
        assert movie['price'] == sample_movie['price']
        get_response = requests.get(f"{api_url}/movies/{movie['id']}")
        assert get_response.status_code == 200
    
    # Test POST /api/movies - Missing required fields
    def test_add_movie_missing_fields(self, api_url, reset_data):
        incomplete_movie = {
            "movie_name": "Incomplete Movie"
        }        
        response = requests.post(
            f"{api_url}/movies",
            json=incomplete_movie,
            headers={'Content-Type': 'application/json'}
        )
        assert response.status_code == 400
        data = response.json()
        assert data['success'] is False
        assert 'error' in data
        assert 'Missing required field' in data['error']
    
    # Test POST /api/movies - Invalid price
    def test_add_movie_invalid_price(self, api_url, reset_data):
        invalid_movie = {
            "movie_name": "Invalid Price Movie",
            "language": "English",
            "duration": "2h",
            "price": "not-a-number"
        }
        response = requests.post(
            f"{api_url}/movies",
            json=invalid_movie,
            headers={'Content-Type': 'application/json'}
        )
        assert response.status_code == 400
        data = response.json()
        assert data['success'] is False
        assert 'price' in data['error'].lower()
    
    # Test PUT /api/movies/<id> - Update movie successfully
    def test_update_movie_success(self, api_url, reset_data):
        movie_id = 101
        update_data = {
            "price": 280,
            "duration": "3h"
        }
        response = requests.put(
            f"{api_url}/movies/{movie_id}",
            json=update_data,
            headers={'Content-Type': 'application/json'}
        )
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert 'data' in data
        movie = data['data']
        assert movie['price'] == update_data['price']
        assert movie['duration'] == update_data['duration']
    
    # Test PUT /api/movies/<id> - Update non-existent movie
    def test_update_movie_not_found(self, api_url, reset_data):
        movie_id = 9999
        update_data = {"price": 300}
        response = requests.put(
            f"{api_url}/movies/{movie_id}",
            json=update_data,
            headers={'Content-Type': 'application/json'}
        )
        assert response.status_code == 404
        data = response.json()
        assert data['success'] is False
        assert 'not found' in data['error'].lower()
    
    # # Test DELETE /api/movies/<id> - Delete movie successfully
    def test_delete_movie_success(self, api_url, reset_data):
        movie_id = 103        
        response = requests.delete(f"{api_url}/movies/{movie_id}")
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert 'message' in data
        get_response = requests.get(f"{api_url}/movies/{movie_id}")
        assert get_response.status_code == 404
    
    # Test DELETE /api/movies/<id> - Delete non-existent movie
    def test_delete_movie_not_found(self, api_url, reset_data):
        movie_id = 9999        
        response = requests.delete(f"{api_url}/movies/{movie_id}")
        assert response.status_code == 404
        data = response.json()
        assert data['success'] is False


# Test cases for Booking operations
class TestBookingAPI:  
    
    # Test POST /api/bookings - Book tickets successfully
    def test_book_tickets_success(self, api_url, reset_data, sample_booking):
        response = requests.post(
            f"{api_url}/bookings",
            json=sample_booking,
            headers={'Content-Type': 'application/json'}
        )
        assert response.status_code == 201
        data = response.json()
        assert data['success'] is True
        assert 'data' in data
        assert 'message' in data
        booking = data['data']
        assert 'booking_id' in booking
        assert booking['movie_id'] == sample_booking['movie_id']
        assert booking['customer_name'] == sample_booking['customer_name']
        assert booking['seats'] == sample_booking['seats']
        assert 'total_price' in booking
        assert 'booking_date' in booking
        assert booking['status'] == "confirmed"
        expected_price = 250 * sample_booking['seats']
        assert booking['total_price'] == expected_price
    
    # Test POST /api/bookings - Missing required fields
    def test_book_tickets_missing_fields(self, api_url, reset_data):
        incomplete_booking = {
            "movie_id": 101,
            "customer_name": "Jane Doe"
        }        
        response = requests.post(
            f"{api_url}/bookings",
            json=incomplete_booking,
            headers={'Content-Type': 'application/json'}
        )
        assert response.status_code == 400
        data = response.json()
        assert data['success'] is False
        assert 'Missing required field' in data['error']
    
    # Test POST /api/bookings - Book for non-existent movie
    def test_book_tickets_invalid_movie(self, api_url, reset_data):
        booking = {
            "movie_id": 9999,
            "customer_name": "Test User",
            "seats": 2
        }
        response = requests.post(
            f"{api_url}/bookings",
            json=booking,
            headers={'Content-Type': 'application/json'}
        )
        assert response.status_code == 404
        data = response.json()
        assert data['success'] is False
        assert 'not found' in data['error'].lower()
    
    # Test POST /api/bookings - Invalid number of seats
    def test_book_tickets_invalid_seats(self, api_url, reset_data):
        booking = {
            "movie_id": 101,
            "customer_name": "Test User",
            "seats": 0 
        }
        response = requests.post(
            f"{api_url}/bookings",
            json=booking,
            headers={'Content-Type': 'application/json'}
        )
        assert response.status_code == 400
        data = response.json()
        assert data['success'] is False
    # Test POST /api/bookings - Exceeds maximum seats limit
    def test_book_tickets_exceeds_limit(self, api_url, reset_data):
        booking = {
            "movie_id": 101,
            "customer_name": "Test User",
            "seats": 15  
        }        
        response = requests.post(
            f"{api_url}/bookings",
            json=booking,
            headers={'Content-Type': 'application/json'}
        )
        assert response.status_code == 400
        data = response.json()
        assert data['success'] is False
        assert 'Maximum' in data['error']
        
    # Test GET /api/bookings - Retrieve all bookings
    def test_get_all_bookings(self, api_url, reset_data, sample_booking):
        requests.post(
            f"{api_url}/bookings",
            json=sample_booking,
            headers={'Content-Type': 'application/json'}
        )
        response = requests.get(f"{api_url}/bookings")
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert 'data' in data
        assert 'count' in data
        assert isinstance(data['data'], list)
        assert data['count'] >= 1
    
    # Test GET /api/bookings/<id> - Get booking by ID
    def test_get_booking_by_id(self, api_url, reset_data, sample_booking):
        create_response = requests.post(
            f"{api_url}/bookings",
            json=sample_booking,
            headers={'Content-Type': 'application/json'}
        )
        booking_id = create_response.json()['data']['booking_id']
        response = requests.get(f"{api_url}/bookings/{booking_id}")
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        booking = data['data']
        assert booking['booking_id'] == booking_id
        

# Parameterized test cases
class TestParameterized:    
    @pytest.mark.parametrize("movie_id,expected_status", [
        (101, 200),  
        (102, 200),  
        (103, 200),  
        (999, 404), 
    ])
    
    # Test GET /api/movies/<id> with various IDs
    def test_get_movie_various_ids(self, api_url, reset_data, movie_id, expected_status):
        response = requests.get(f"{api_url}/movies/{movie_id}")
        assert response.status_code == expected_status
    
    @pytest.mark.parametrize("seats,expected_status", [
        (1, 201),   
        (5, 201),   
        (10, 201), 
        (0, 400),
        (-1, 400),
        (11, 400),  
    ])
    
    # Test POST /api/bookings with various seat counts
    def test_booking_various_seats(self, api_url, reset_data, seats, expected_status):
        booking = {
            "movie_id": 101,
            "customer_name": "Test User",
            "seats": seats
        }        
        response = requests.post(
            f"{api_url}/bookings",
            json=booking,
            headers={'Content-Type': 'application/json'}
        )
        assert response.status_code == expected_status


# End-to-end integration test scenarios
class TestIntegration:    
    # Test complete CRUD lifecycle for a movie
    def test_complete_movie_lifecycle(self, api_url, reset_data):
        new_movie = {
            "movie_name": "The Matrix",
            "language": "English",
            "duration": "2h 16m",
            "price": 240
        }
        create_response = requests.post(
            f"{api_url}/movies",
            json=new_movie,
            headers={'Content-Type': 'application/json'}
        )
        assert create_response.status_code == 201
        movie_id = create_response.json()['data']['id']
        read_response = requests.get(f"{api_url}/movies/{movie_id}")
        assert read_response.status_code == 200
        assert read_response.json()['data']['movie_name'] == "The Matrix"
        update_response = requests.put(
            f"{api_url}/movies/{movie_id}",
            json={"price": 260},
            headers={'Content-Type': 'application/json'}
        )
        assert update_response.status_code == 200
        assert update_response.json()['data']['price'] == 260
        delete_response = requests.delete(f"{api_url}/movies/{movie_id}")
        assert delete_response.status_code == 200
        verify_response = requests.get(f"{api_url}/movies/{movie_id}")
        assert verify_response.status_code == 404
    
    # Test complete booking workflow
    def test_booking_workflow(self, api_url, reset_data):
        movies_response = requests.get(f"{api_url}/movies")
        assert movies_response.status_code == 200
        movies = movies_response.json()['data']
        assert len(movies) > 0
        movie = movies[0]
        booking_data = {
            "movie_id": movie['id'],
            "customer_name": "Alice Smith",
            "seats": 3,
            "show_time": "9:00 PM"
        }        
        booking_response = requests.post(
            f"{api_url}/bookings",
            json=booking_data,
            headers={'Content-Type': 'application/json'}
        )
        assert booking_response.status_code == 201
        booking = booking_response.json()['data']
        assert booking['movie_name'] == movie['movie_name']
        assert booking['total_price'] == movie['price'] * booking_data['seats']
        assert booking['status'] == "confirmed"


# Test error handling scenarios
class TestErrorHandling:
    
    # Test accessing non-existent endpoint
    def test_invalid_endpoint(self, api_url):
        response = requests.get(f"{api_url}/invalid_endpoint")
        assert response.status_code == 404
    
    # Test sending invalid JSON
    def test_invalid_json(self, api_url, reset_data):
        response = requests.post(
            f"{api_url}/movies",
            data="Not a JSON",
            headers={'Content-Type': 'application/json'}
        )
        assert response.status_code in [400, 500]
    
    # Test request without Content-Type header
    def test_missing_content_type(self, api_url, reset_data):
        new_movie = {
            "movie_name": "Test Movie",
            "language": "English",
            "duration": "2h",
            "price": 200
        }
        response = requests.post(f"{api_url}/movies", json=new_movie)
        assert response.status_code == 201