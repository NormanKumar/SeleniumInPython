import requests
import pytest

def test_user_orders_empty(base_url):
    user = requests.post(
        f"{base_url}/api/v1/users/register",
        json={"name": "Empty", "email": "empty@test.com", "password": "123"}
    ).json()
    uid = user["uid"]
    response = requests.get(
        f"{base_url}/api/v1/users/{uid}/orders"
    )
    assert response.status_code == 200
    assert response.json()["message"] == "No Orders Yet"

def test_user_orders_with_data(base_url):
    restaurant = requests.post(
        f"{base_url}/api/v1/restaurants",
        json={"name": "Orders Cafe", "location": "Delhi"}
    ).json()
    rid = restaurant["rid"]
    requests.patch(
        f"{base_url}/api/v1/admin/restaurants/{rid}/approve",
        json={"approved": True}
    )
    requests.post(
        f"{base_url}/api/v1/restaurants/{rid}/dishes",
        json={"name": "Pizza", "price": 200}
    )
    user = requests.post(
        f"{base_url}/api/v1/users/register",
        json={"name": "Buyer", "email": "buyer@test.com", "password": "123"}
    ).json()
    uid = user["uid"]
    requests.post(
        f"{base_url}/api/v1/orders",
        json={"uid": uid, "rid": rid, "dishes": ["Pizza"]}
    )
    response = requests.get(
        f"{base_url}/api/v1/users/{uid}/orders"
    )
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_user_orders_not_found(base_url):
    response = requests.get(
        f"{base_url}/api/v1/users/9999/orders"
    )
    assert response.status_code == 404
    assert response.json()["message"] == "User Not Found"

def test_restaurant_orders_empty(base_url):
    restaurant = requests.post(
        f"{base_url}/api/v1/restaurants",
        json={"name": "Empty Orders Cafe", "location": "Delhi"}
    ).json()
    rid = restaurant["rid"]
    response = requests.get(
        f"{base_url}/api/v1/restaurants/{rid}/orders"
    )
    assert response.status_code == 200
    assert response.json()["message"] == "No Orders Yet"

def test_restaurant_orders_with_data(base_url):
    restaurant = requests.post(
        f"{base_url}/api/v1/restaurants",
        json={"name": "Orders Cafe", "location": "Mumbai"}
    ).json()
    rid = restaurant["rid"]
    requests.patch(
        f"{base_url}/api/v1/admin/restaurants/{rid}/approve",
        json={"approved": True}
    )
    requests.post(
        f"{base_url}/api/v1/restaurants/{rid}/dishes",
        json={"name": "Burger", "price": 150}
    )
    user = requests.post(
        f"{base_url}/api/v1/users/register",
        json={"name": "Buyer2", "email": "buyer2@test.com", "password": "123"}
    ).json()
    uid = user["uid"]
    requests.post(
        f"{base_url}/api/v1/orders",
        json={"uid": uid, "rid": rid, "dishes": ["Burger"]}
    )
    response = requests.get(
        f"{base_url}/api/v1/restaurants/{rid}/orders"
    )
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_restaurant_orders_not_found(base_url):
    response = requests.get(
        f"{base_url}/api/v1/restaurants/9999/orders"
    )
    assert response.status_code == 404
    assert response.json()["message"] == "Restaurant Not Found"
