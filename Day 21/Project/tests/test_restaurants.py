import requests
import pytest

def test_register_restaurant_success(base_url):
    payload = {
        "name": "Emirates Hotel",
        "category": "Indian",
        "location": "Delhi",
        "contact": "9999999999"
    }
    response = requests.post(f"{base_url}/api/v1/restaurants", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Emirates Hotel"
    assert data["approved"] is False
    assert data["disabled"] is False
    assert isinstance(data["dishes"], list)
    assert isinstance(data["feedback"], list)
    assert isinstance(data["orders"], list)
    
@pytest.mark.parametrize("payload", [
    {"name": "CafeOne", "location": "Delhi"},
])
def test_duplicate_restaurant(base_url, payload):
    requests.post(f"{base_url}/api/v1/restaurants", json=payload)
    response = requests.post(f"{base_url}/api/v1/restaurants", json=payload)
    assert response.status_code == 409
    assert response.json()["message"] == "Restaurant Already Exist"
    
def test_same_name_different_location(base_url):
    requests.post(f"{base_url}/api/v1/restaurants", json={
        "name": "Global Cafe",
        "location": "Delhi"
    })
    response = requests.post(f"{base_url}/api/v1/restaurants", json={
        "name": "Global Cafe",
        "location": "Mumbai"
    })
    assert response.status_code == 201
    
def test_response_keys(base_url):
    response = requests.post(f"{base_url}/api/v1/restaurants", json={
        "name": "KeyTest",
        "location": "Chennai"
    })
    data = response.json()
    expected_keys = [
        "rid", "name", "category", "location",
        "dishes", "feedback", "rating",
        "orders", "approved", "disabled"
    ]
    for key in expected_keys:
        assert key in data
        
def test_update_restaurant_success(base_url):
    create = requests.post(f"{base_url}/api/v1/restaurants", json={
        "name": "Update Cafe",
        "location": "Delhi"
    })
    rid = create.json()["rid"]
    response = requests.put(
        f"{base_url}/api/v1/restaurants/{rid}",
        json={"location": "Mumbai"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Updated restaurant"
    assert data["data"]["location"] == "Mumbai"
    
def test_update_restaurant_not_found(base_url):
    response = requests.put(
        f"{base_url}/api/v1/restaurants/9999",
        json={"location": "Pune"}
    )
    assert response.status_code == 404
    assert response.json()["message"] == "Restaurant Not Found"

@pytest.mark.parametrize("payload, idx", [
    ({"name": "New Name"}, 1),
    ({"category": "Italian"}, 2),
    ({"contact": "8888888888"}, 3),
])
def test_update_multiple_fields(base_url, payload, idx):
    restaurant_name = f"Delhi Cafe {idx}"
    create = requests.post(
        f"{base_url}/api/v1/restaurants",
        json={
            "name": restaurant_name,
            "location": "Delhi"
        }
    )
    assert create.status_code == 201
    rid = create.json()["rid"]
    response = requests.put(
        f"{base_url}/api/v1/restaurants/{rid}",
        json=payload
    )
    assert response.status_code == 200
    
def test_disable_restaurant(base_url):
    create = requests.post(f"{base_url}/api/v1/restaurants", json={
        "name": "Disable Cafe",
        "location": "Delhi"
    })
    rid = create.json()["rid"]
    response = requests.put(
        f"{base_url}/api/v1/restaurants/{rid}/disable",
        json={"disabled": True}
    )
    assert response.status_code == 200
    assert response.json()["data"]["disabled"] is True
    
def test_enable_restaurant(base_url):
    create = requests.post(f"{base_url}/api/v1/restaurants", json={
        "name": "Enable Cafe",
        "location": "Delhi"
    })
    rid = create.json()["rid"]
    response = requests.put(
        f"{base_url}/api/v1/restaurants/{rid}/disable",
        json={"disabled": False}
    )
    assert response.status_code == 200
    assert response.json()["data"]["disabled"] is False
    
def test_disable_restaurant_not_found(base_url):
    response = requests.put(
        f"{base_url}/api/v1/restaurants/9999/disable",
        json={"disabled": True}
    )
    assert response.status_code == 404
    assert response.json()["message"] == "Restaurant Not Found"
    
def test_get_restaurant_success(base_url):
    create = requests.post(f"{base_url}/api/v1/restaurants", json={
        "name": "Profile Cafe",
        "location": "Delhi"
    })
    rid = create.json()["rid"]
    response = requests.get(f"{base_url}/api/v1/restaurants/{rid}")
    assert response.status_code == 200
    assert response.json()["rid"] == rid
    assert response.json()["name"] == "Profile Cafe"
    
def test_get_restaurant_not_found(base_url):
    response = requests.get(f"{base_url}/api/v1/restaurants/9999")
    assert response.status_code == 404
    assert response.json()["message"] == "Restaurant Not Found"
    
def test_get_all_restaurants(base_url):
    requests.post(f"{base_url}/api/v1/restaurants", json={
        "name": "Cafe One",
        "location": "Delhi"
    })
    requests.post(f"{base_url}/api/v1/restaurants", json={
        "name": "Cafe Two",
        "location": "Mumbai"
    })
    response = requests.get(f"{base_url}/api/v1/restaurants")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2
    
def test_delete_restaurant_success(base_url):
    create = requests.post(f"{base_url}/api/v1/restaurants", json={
        "name": "Delete Cafe",
        "location": "Delhi"
    })
    rid = create.json()["rid"]
    response = requests.delete(
        f"{base_url}/api/v1/restaurants/{rid}/delete"
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Restaurant Removed"
    
def test_delete_restaurant_not_found(base_url):
    response = requests.delete(
        f"{base_url}/api/v1/restaurants/9999/delete"
    )
    assert response.status_code == 404
    assert response.json()["message"] == "Restaurant Not Found"
    
def test_restaurant_deleted_from_list(base_url):
    create = requests.post(f"{base_url}/api/v1/restaurants", json={
        "name": "Gone Cafe",
        "location": "Mumbai"
    })
    rid = create.json()["rid"]
    requests.delete(f"{base_url}/api/v1/restaurants/{rid}/delete")
    response = requests.get(f"{base_url}/api/v1/restaurants")
    ids = [r["rid"] for r in response.json()]
    assert rid not in ids