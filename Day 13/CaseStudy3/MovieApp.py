from flask import Flask,jsonify,request
from datetime import datetime
import json

app = Flask(__name__)

movies = [
    {
        "id": 101,
        "movie_name": "Dhurandhar",
        "language": "Hindi",
        "duration": "3h 34m",
        "price": 250
    },
    {
        "id": 102,
        "movie_name": "3 Idiots",
        "language": "Hindi",
        "duration": "2h 50m",
        "price": 200
    },
    {
        "id": 103,
        "movie_name": "Dangal",
        "language": "Hindi",
        "duration": "2h 41m",
        "price": 220
    }
]

bookings = []
booking_id_counter = 1000

# Retrieve all movies Returns: JSON array of all movies with 200 status
@app.route('/api/movies', methods=['GET'])
def get_all_movies():
    return jsonify({
        "success": True,
        "count": len(movies),
        "data": movies
    }), 200
    

# Get movie by ID  Args: movie_id: Integer ID of the movie Returns: Movie object if found (200), error message if not (404)
@app.route('/api/movies/<int:movie_id>', methods=['GET'])
def get_movie_by_id(movie_id):
    
    movie = next((m for m in movies if m['id'] == movie_id), None)
    
    if movie:
        return jsonify({
            "success": True,
            "data": movie
        }), 200
    else:
        return jsonify({
            "success": False,
            "error": f"Movie with ID {movie_id} not found"
        }), 404

# Add a new movie Request Body: JSON with movie details Returns: Created movie with 201 status or error with 400
@app.route('/api/movies', methods=['POST'])
def add_movie():
    if not request.json:
        return jsonify({
            "success": False,
            "error": "Request body must be JSON"
        }), 400
    
    # Validate required fields
    required_fields = ['movie_name', 'language', 'duration', 'price']
    for field in required_fields:
        if field not in request.json:
            return jsonify({
                "success": False,
                "error": f"Missing required field: {field}"
            }), 400
    
    # Validate price is numeric
    try:
        price = float(request.json['price'])
        if price <= 0:
            raise ValueError("Price must be positive")
    except (ValueError, TypeError):
        return jsonify({
            "success": False,
            "error": "Price must be a positive number"
        }), 400
    
    # Generate new ID
    new_id = max([m['id'] for m in movies], default=100) + 1
    
    new_movie = {
        "id": new_id,
        "movie_name": request.json['movie_name'],
        "language": request.json['language'],
        "duration": request.json['duration'],
        "price": price
    }
    
    movies.append(new_movie)
    
    return jsonify({
        "success": True,
        "message": "Movie added successfully",
        "data": new_movie
    }), 201


# Update movie details Args: movie_id: Integer ID of the movie to update Request Body: JSON with fields to update Returns: Updated movie (200) or error (404/400)
@app.route('/api/movies/<int:movie_id>', methods=['PUT'])
def update_movie(movie_id):
    
    if not request.json:
        return jsonify({
            "success": False,
            "error": "Request body must be JSON"
        }), 400
    
    movie = next((m for m in movies if m['id'] == movie_id), None)
    
    if not movie:
        return jsonify({
            "success": False,
            "error": f"Movie with ID {movie_id} not found"
        }), 404
    
    # Update allowed fields
    allowed_fields = ['movie_name', 'language', 'duration', 'price']
    
    for field in allowed_fields:
        if field in request.json:
            if field == 'price':
                try:
                    price = float(request.json['price'])
                    if price <= 0:
                        raise ValueError("Price must be positive")
                    movie[field] = price
                except (ValueError, TypeError):
                    return jsonify({
                        "success": False,
                        "error": "Price must be a positive number"
                    }), 400
            else:
                movie[field] = request.json[field]
    
    return jsonify({
        "success": True,
        "message": "Movie updated successfully",
        "data": movie
    }), 200

# Delete a movie Args: movie_id: Integer ID of the movie to delete Returns: Success message (200) or error (404)
@app.route('/api/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    global movies
    
    movie = next((m for m in movies if m['id'] == movie_id), None)
    
    if not movie:
        return jsonify({
            "success": False,
            "error": f"Movie with ID {movie_id} not found"
        }), 404
    
    movies = [m for m in movies if m['id'] != movie_id]
    
    return jsonify({
        "success": True,
        "message": f"Movie '{movie['movie_name']}' deleted successfully"
    }), 200

@app.route('/api/bookings', methods=['POST'])
def book_tickets():
    global booking_id_counter
    
    if not request.json:
        return jsonify({
            "success": False,
            "error": "Request body must be JSON"
        }), 400
    
    # Validate required fields
    required_fields = ['movie_id', 'customer_name', 'seats']
    for field in required_fields:
        if field not in request.json:
            return jsonify({
                "success": False,
                "error": f"Missing required field: {field}"
            }), 400
    
    movie_id = request.json['movie_id']
    seats = request.json['seats']
    
    # Validate seats
    try:
        seats = int(seats)
        if seats <= 0:
            raise ValueError("Seats must be positive")
        if seats > 10:
            return jsonify({
                "success": False,
                "error": "Maximum 10 seats allowed per booking"
            }), 400
    except (ValueError, TypeError):
        return jsonify({
            "success": False,
            "error": "Seats must be a positive integer"
        }), 400
    
    # Check if movie exists
    movie = next((m for m in movies if m['id'] == movie_id), None)
    
    if not movie:
        return jsonify({
            "success": False,
            "error": f"Movie with ID {movie_id} not found"
        }), 404
    
    # Calculate total price
    total_price = movie['price'] * seats
    
    # Create booking
    booking = {
        "booking_id": booking_id_counter,
        "movie_id": movie_id,
        "movie_name": movie['movie_name'],
        "customer_name": request.json['customer_name'],
        "seats": seats,
        "show_time": request.json.get('show_time', 'Not specified'),
        "total_price": total_price,
        "booking_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "confirmed"
    }
    
    bookings.append(booking)
    booking_id_counter += 1
    
    return jsonify({
        "success": True,
        "message": "Booking confirmed successfully",
        "data": booking
    }), 201

# Retrieve all bookings (useful for testing) Returns: JSON array of all bookings
@app.route('/api/bookings', methods=['GET'])
def get_all_bookings():
    return jsonify({
        "success": True,
        "count": len(bookings),
        "data": bookings
    }), 200

#  Get booking by ID Args: booking_id: Integer ID of the booking Returns: Booking object if found (200), error if not (404)
@app.route('/api/bookings/<int:booking_id>', methods=['GET'])
def get_booking_by_id(booking_id):
    booking = next((b for b in bookings if b['booking_id'] == booking_id), None)
    
    if booking:
        return jsonify({
            "success": True,
            "data": booking
        }), 200
    else:
        return jsonify({
            "success": False,
            "error": f"Booking with ID {booking_id} not found"
        }), 404

#  Health check endpoint Returns: API status
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "Movie Ticket Booking API",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }), 200

# Reset data to initial state (for testing purposes) Returns: Success message
@app.route('/api/reset', methods=['POST'])
def reset_data():
    global movies, bookings, booking_id_counter
    
    movies = [
        {
            "id": 101,
            "movie_name": "Interstellar",
            "language": "English",
            "duration": "2h 49m",
            "price": 250
        },
        {
            "id": 102,
            "movie_name": "Inception",
            "language": "English",
            "duration": "2h 28m",
            "price": 200
        },
        {
            "id": 103,
            "movie_name": "The Dark Knight",
            "language": "English",
            "duration": "2h 32m",
            "price": 220
        }
    ]
    
    bookings = []
    booking_id_counter = 1000
    
    return jsonify({
        "success": True,
        "message": "Data reset successfully"
    }), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500

if __name__ == "__main__":
    app.run(debug=True)