import requests
import pytest

def test_add_dish_success(base_url):
    create_restaurant = requests.post(
        f"{base_url}/api/v1/restaurants",
        json={"name": "Dish Cafe", "location": "Delhi"}
    )
    rid = create_restaurant.json()["rid"]
    response = requests.post(
        f"{base_url}/api/v1/restaurants/{rid}/dishes",
        json={
            "name": "Pizza",
            "type": "Veg",
            "price": 250,
            "time": "20 min"
        }
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Pizza"
    assert response.json()["rid"] == rid
    
def test_add_duplicate_dish(base_url):
    create_restaurant = requests.post(
        f"{base_url}/api/v1/restaurants",
        json={"name": "Dup Dish Cafe", "location": "Mumbai"}
    )
    rid = create_restaurant.json()["rid"]
    payload = {
        "name": "Burger",
        "type": "Veg",
        "price": 150
    }
    requests.post(f"{base_url}/api/v1/restaurants/{rid}/dishes", json=payload)
    response = requests.post(
        f"{base_url}/api/v1/restaurants/{rid}/dishes",
        json=payload
    )
    assert response.status_code == 409
    assert response.json()["message"] == "Dish Already Exist"
    
def test_add_dish_restaurant_not_found(base_url):
    response = requests.post(
        f"{base_url}/api/v1/restaurants/9999/dishes",
        json={"name": "Pasta", "price": 200}
    )
    assert response.status_code == 404
    assert response.json()["message"] == "Restaurant Not Found"

def test_update_dish_success(base_url):
    create_restaurant = requests.post(
        f"{base_url}/api/v1/restaurants",
        json={"name": "Update Dish Cafe", "location": "Delhi"}
    )
    rid = create_restaurant.json()["rid"]
    create_dish = requests.post(
        f"{base_url}/api/v1/restaurants/{rid}/dishes",
        json={"name": "Pizza", "price": 200}
    )
    did = create_dish.json()["did"]
    response = requests.put(
        f"{base_url}/api/v1/dishes/{did}",
        json={"price": 300}
    )
    assert response.status_code == 200
    assert response.json()["data"]["price"] == 300
    
def test_update_dish_not_found(base_url):
    response = requests.put(
        f"{base_url}/api/v1/dishes/9999",
        json={"price": 100}
    )
    assert response.status_code == 404
    assert response.json()["message"] == "Dish Not Found"

@pytest.mark.parametrize("payload, idx", [
    ({"name": "New Dish Name"}, 1),
    ({"price": 180}, 2),
    ({"time": "15 min"}, 3),
])
def test_update_dish_fields(base_url, payload, idx):
    restaurant_name = f"Multi Dish Cafe {idx}"
    create_restaurant = requests.post(
        f"{base_url}/api/v1/restaurants",
        json={
            "name": restaurant_name,
            "location": "Mumbai"
        }
    )
    assert create_restaurant.status_code == 201
    rid = create_restaurant.json()["rid"]
    create_dish = requests.post(
        f"{base_url}/api/v1/restaurants/{rid}/dishes",
        json={
            "name": "Burger",
            "price": 120
        }
    )
    assert create_dish.status_code == 201
    did = create_dish.json()["did"]
    response = requests.put(
        f"{base_url}/api/v1/dishes/{did}",
        json=payload
    )
    assert response.status_code == 200

def test_disable_dish(base_url):
    create_restaurant = requests.post(
        f"{base_url}/api/v1/restaurants",
        json={"name": "Status Dish Cafe", "location": "Delhi"}
    )
    rid = create_restaurant.json()["rid"]
    create_dish = requests.post(
        f"{base_url}/api/v1/restaurants/{rid}/dishes",
        json={"name": "Pizza", "price": 200}
    )
    did = create_dish.json()["did"]
    response = requests.patch(
        f"{base_url}/api/v1/dishes/{did}/status",
        json={"disabled": True}
    )
    assert response.status_code == 200
    assert response.json()["data"]["disabled"] is True

def test_enable_dish(base_url):
    create_restaurant = requests.post(
        f"{base_url}/api/v1/restaurants",
        json={"name": "Enable Dish Cafe", "location": "Mumbai"}
    )
    rid = create_restaurant.json()["rid"]
    create_dish = requests.post(
        f"{base_url}/api/v1/restaurants/{rid}/dishes",
        json={"name": "Burger", "price": 150}
    )
    did = create_dish.json()["did"]
    response = requests.patch(
        f"{base_url}/api/v1/dishes/{did}/status",
        json={"disabled": False}
    )
    assert response.status_code == 200
    assert response.json()["data"]["disabled"] is False

def test_disable_dish_not_found(base_url):
    response = requests.patch(
        f"{base_url}/api/v1/dishes/9999/status",
        json={"disabled": True}
    )
    assert response.status_code == 404
    assert response.json()["message"] == "Dish Not Found"

def test_delete_dish_success(base_url):
    create_restaurant = requests.post(
        f"{base_url}/api/v1/restaurants",
        json={"name": "Delete Dish Cafe", "location": "Delhi"}
    )
    rid = create_restaurant.json()["rid"]
    create_dish = requests.post(
        f"{base_url}/api/v1/restaurants/{rid}/dishes",
        json={"name": "Pizza", "price": 200}
    )
    did = create_dish.json()["did"]
    response = requests.delete(
        f"{base_url}/api/v1/dishes/{did}/delete"
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Dish Removed"

def test_delete_dish_not_found(base_url):
    response = requests.delete(
        f"{base_url}/api/v1/dishes/9999/delete"
    )
    assert response.status_code == 404
    assert response.json()["message"] == "Dish Not Found"

def test_dish_removed_from_list(base_url):
    create_restaurant = requests.post(
        f"{base_url}/api/v1/restaurants",
        json={"name": "Gone Dish Cafe", "location": "Mumbai"}
    )
    rid = create_restaurant.json()["rid"]
    create_dish = requests.post(
        f"{base_url}/api/v1/restaurants/{rid}/dishes",
        json={"name": "Burger", "price": 150}
    )
    did = create_dish.json()["did"]
    requests.delete(f"{base_url}/api/v1/dishes/{did}/delete")
    response = requests.get(f"{base_url}/api/v1/dishes")
    ids = [d["did"] for d in response.json()]
    assert did not in ids

def test_get_all_dishes_with_data(base_url):
    create_restaurant = requests.post(
        f"{base_url}/api/v1/restaurants",
        json={"name": "Dish List Cafe", "location": "Delhi"}
    )
    rid = create_restaurant.json()["rid"]
    requests.post(
        f"{base_url}/api/v1/restaurants/{rid}/dishes",
        json={"name": "Pizza", "price": 200}
    )
    requests.post(
        f"{base_url}/api/v1/restaurants/{rid}/dishes",
        json={"name": "Burger", "price": 150}
    )
    response = requests.get(f"{base_url}/api/v1/dishes")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2

def test_get_all_dishes_empty(base_url):
    response = requests.get(f"{base_url}/api/v1/dishes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
