import requests
import pytest

def test_register_user_success(base_url):
    response = requests.post(
        f"{base_url}/api/v1/users/register",
        json={
            "name": "Ravi",
            "email": "ravi@test.com",
            "password": "1234"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "ravi@test.com"
    assert "uid" in data

def test_register_user_duplicate_email(base_url):
    payload = {
        "name": "Neha",
        "email": "neha@test.com",
        "password": "1111"
    }
    requests.post(f"{base_url}/api/v1/users/register", json=payload)
    response = requests.post(
        f"{base_url}/api/v1/users/register",
        json=payload
    )
    assert response.status_code == 409
    assert response.json()["message"] == "User Already Exists"

@pytest.mark.parametrize("email", [
    "a@test.com",
    "b@test.com",
    "c@test.com"
])
def test_multiple_users(base_url, email):
    response = requests.post(
        f"{base_url}/api/v1/users/register",
        json={
            "name": "User",
            "email": email,
            "password": "1234"
        }
    )
    assert response.status_code == 201

def setup_search_data(base_url):
    requests.post(f"{base_url}/test/reset")
    r1 = requests.post(
        f"{base_url}/api/v1/restaurants",
        json={"name": "Spice Hub", "location": "Delhi"}
    ).json()
    r2 = requests.post(
        f"{base_url}/api/v1/restaurants",
        json={"name": "Spice Hub", "location": "Mumbai"}
    ).json()
    requests.patch(
        f"{base_url}/api/v1/admin/restaurants/{r1['rid']}/approve",
        json={"approved": True}
    )
    requests.patch(
        f"{base_url}/api/v1/admin/restaurants/{r2['rid']}/approve",
        json={"approved": True}
    )
    requests.post(
        f"{base_url}/api/v1/restaurants/{r1['rid']}/dishes",
        json={"name": "Pizza", "price": 150}
    )
    requests.post(
        f"{base_url}/api/v1/restaurants/{r2['rid']}/dishes",
        json={"name": "Burger", "price": 120}
    )



def test_search_by_name(base_url):
    setup_search_data(base_url)
    response = requests.get(
        f"{base_url}/api/v1/restaurants/search",
        params={"name": "Spice Hub"}
    )
    assert response.status_code == 200
    assert len(response.json()) >= 2

def test_search_by_name_and_location(base_url):
    setup_search_data(base_url)
    response = requests.get(
        f"{base_url}/api/v1/restaurants/search",
        params={"name": "Spice Hub", "location": "Delhi"}
    )
    assert response.status_code == 200
    assert response.json()[0]["location"] == "Delhi"

def test_search_by_dish(base_url):
    setup_search_data(base_url)
    response = requests.get(
        f"{base_url}/api/v1/restaurants/search",
        params={"dish": "Pizza"}
    )
    assert response.status_code == 200
    assert response.json()[0]["name"] == "Spice Hub"


def test_search_location_not_found(base_url):
    response = requests.get(
        f"{base_url}/api/v1/restaurants/search",
        params={"location": "Chennai"}
    )
    assert response.status_code == 404
    assert response.json()["message"] == "Location unserviceable"

def test_search_restaurant_not_found(base_url):
    response = requests.get(
        f"{base_url}/api/v1/restaurants/search",
        params={"name": "Unknown Cafe"}
    )
    assert response.status_code == 404
    assert response.json()["message"] == "Restaurant not found"

def test_search_dish_not_found(base_url):
    setup_search_data(base_url)
    response = requests.get(
        f"{base_url}/api/v1/restaurants/search",
        params={"dish": "Pasta"}
    )
    assert response.status_code == 404
    assert response.json()["message"] == "No dish found in this restaurant/location"

@pytest.mark.parametrize("params", [
    {"name": "Spice Hub"},
    {"location": "Delhi"},
    {"dish": "Burger"},
])
def test_search_multiple_filters(base_url, params):
    setup_search_data(base_url)
    response = requests.get(
        f"{base_url}/api/v1/restaurants/search",
        params=params
    )
    assert response.status_code == 200

def setup_order_env(base_url):
    requests.post(f"{base_url}/test/reset")
    r = requests.post(
        f"{base_url}/api/v1/restaurants",
        json={"name": "Order Cafe", "location": "Delhi"}
    ).json()
    rid = r["rid"]
    requests.patch(
        f"{base_url}/api/v1/admin/restaurants/{rid}/approve",
        json={"approved": True}
    )
    requests.post(
        f"{base_url}/api/v1/restaurants/{rid}/dishes",
        json={"name": "Pizza", "price": 150}
    )
    requests.post(
        f"{base_url}/api/v1/restaurants/{rid}/dishes",
        json={"name": "Burger", "price": 120}
    )
    user = requests.post(
        f"{base_url}/api/v1/users/register",
        json={"name": "Order User", "email": "order@test.com", "password": "123"}
    ).json()
    return rid, user["uid"]

def test_order_success(base_url):
    rid, uid = setup_order_env(base_url)
    response = requests.post(
        f"{base_url}/api/v1/orders",
        json={
            "uid": uid,
            "rid": rid,
            "dishes": ["Pizza", "Burger"]
        }
    )
    assert response.status_code == 201
    data = response.json()["data"]
    assert data["total"] == 270
    assert "Pizza" in data["dishes"]
    assert "Burger" in data["dishes"]

def test_order_without_dishes(base_url):
    response = requests.post(
        f"{base_url}/api/v1/orders",
        json={"uid": 1, "rid": 1}
    )
    assert response.status_code == 400
    assert response.json()["message"] == "Add at least one dish"

def test_order_user_not_found(base_url):
    response = requests.post(
        f"{base_url}/api/v1/orders",
        json={"uid": 9999, "rid": 1, "dishes": ["Pizza"]}
    )
    assert response.status_code == 404
    assert response.json()["message"] == "User not found"

def test_order_restaurant_not_found(base_url):
    requests.post(f"{base_url}/test/reset")
    user = requests.post(
        f"{base_url}/api/v1/users/register",
        json={"name": "U", "email": "u@test.com", "password": "1"}
    ).json()
    response = requests.post(
        f"{base_url}/api/v1/orders",
        json={
            "uid": user["uid"],
            "rid": 9999,
            "dishes": ["Pizza"]
        }
    )
    assert response.status_code == 404
    assert response.json()["message"] == "Restaurant not found"

def test_order_invalid_dish(base_url):
    rid, uid = setup_order_env(base_url)
    response = requests.post(
        f"{base_url}/api/v1/orders",
        json={
            "uid": uid,
            "rid": rid,
            "dishes": ["Pasta"]
        }
    )
    assert response.status_code == 400
    assert "not available" in response.json()["message"]

def test_order_disabled_dish(base_url):
    rid, uid = setup_order_env(base_url)
    dishes_list = requests.get(f"{base_url}/api/v1/dishes").json()
    did = dishes_list[0]["did"]
    requests.patch(
        f"{base_url}/api/v1/dishes/{did}/status",
        json={"disabled": True}
    )
    response = requests.post(
        f"{base_url}/api/v1/orders",
        json={
            "uid": uid,
            "rid": rid,
            "dishes": ["Pizza"]
        }
    )
    assert response.status_code == 400

def setup_rating_env(base_url):
    requests.post(f"{base_url}/test/reset")
    r = requests.post(
        f"{base_url}/api/v1/restaurants",
        json={"name": "Rating Cafe", "location": "Delhi"}
    ).json()
    rid = r["rid"]
    requests.patch(
        f"{base_url}/api/v1/admin/restaurants/{rid}/approve",
        json={"approved": True}
    )
    requests.post(
        f"{base_url}/api/v1/restaurants/{rid}/dishes",
        json={"name": "Burger", "price": 100}
    )
    user = requests.post(
        f"{base_url}/api/v1/users/register",
        json={"name": "Rate User", "email": "rate@test.com", "password": "123"}
    ).json()
    order = requests.post(
        f"{base_url}/api/v1/orders",
        json={
            "uid": user["uid"],
            "rid": rid,
            "dishes": ["Burger"]
        }
    ).json()
    return order["data"]["oid"]

def test_add_feedback_success(base_url):
    oid = setup_rating_env(base_url)
    response = requests.post(
        f"{base_url}/api/v1/ratings",
        json={
            "oid": oid,
            "rating": 5,
            "feedback": "Excellent!"
        }
    )
    assert response.status_code == 201
    assert response.json()["message"] == "Feedback added"

def test_average_rating(base_url):
    oid = setup_rating_env(base_url)
    requests.post(
        f"{base_url}/api/v1/ratings",
        json={"oid": oid, "rating": 4, "feedback": "Good"}
    )
    response = requests.post(
        f"{base_url}/api/v1/ratings",
        json={"oid": oid, "rating": 2, "feedback": "Okay"}
    )
    assert response.status_code == 201
    assert response.json()["rating"] == 3

def test_rating_order_not_found(base_url):
    response = requests.post(
        f"{base_url}/api/v1/ratings",
        json={"oid": 9999, "rating": 5, "feedback": "Nice"}
    )
    assert response.status_code == 404
    assert response.json()["message"] == "Order not found"

def test_update_user_success(base_url):
    user = requests.post(
        f"{base_url}/api/v1/users/register",
        json={"name": "Rohit", "email": "rohit@test.com", "password": "123"}
    ).json()
    uid = user["uid"]
    response = requests.put(
        f"{base_url}/api/v1/{uid}/update",
        json={"name": "Rohit Sharma"}
    )
    assert response.status_code == 200
    assert response.json()["data"]["name"] == "Rohit Sharma"

def test_update_user_not_found(base_url):
    response = requests.put(
        f"{base_url}/api/v1/9999/update",
        json={"name": "Nobody"}
    )
    assert response.status_code == 404
    assert response.json()["message"] == "User Not Found"

@pytest.mark.parametrize("payload", [
    {"name": "New Name"},
    {"password": "newpass"},
    {"email": "new@email.com"}
])
def test_update_user_fields(base_url, payload):
    requests.post(f"{base_url}/test/reset")
    user = requests.post(
        f"{base_url}/api/v1/users/register",
        json={
            "name": "Test",
            "email": "field@test.com",
            "password": "111"
        }
    ).json()
    uid = user["uid"]
    response = requests.put(
        f"{base_url}/api/v1/{uid}/update",
        json=payload
    )
    assert response.status_code == 200

def test_delete_user_success(base_url):
    user = requests.post(
        f"{base_url}/api/v1/users/register",
        json={"name": "Delete Me", "email": "del@test.com", "password": "123"}
    ).json()
    uid = user["uid"]
    response = requests.delete(
        f"{base_url}/api/v1/{uid}/delete"
    )
    assert response.status_code == 200
    assert response.json()["message"] == "User Profile Deleted"

def test_delete_user_not_found(base_url):
    response = requests.delete(
        f"{base_url}/api/v1/9999/delete"
    )
    assert response.status_code == 404
    assert response.json()["message"] == "User Not Found"

def test_user_removed_from_system(base_url):
    user = requests.post(
        f"{base_url}/api/v1/users/register",
        json={"name": "Gone", "email": "gone@test.com", "password": "123"}
    ).json()
    uid = user["uid"]
    requests.delete(f"{base_url}/api/v1/{uid}/delete")
    response = requests.put(
        f"{base_url}/api/v1/{uid}/update",
        json={"name": "Should Fail"}
    )
    assert response.status_code == 404
