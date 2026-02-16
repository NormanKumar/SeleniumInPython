import requests

def test_approve_restaurant(base_url):
    create = requests.post(
        f"{base_url}/api/v1/restaurants",
        json={"name": "Approve Cafe", "location": "Delhi"}
    )
    rid = create.json()["rid"]
    response = requests.patch(
        f"{base_url}/api/v1/admin/restaurants/{rid}/approve",
        json={"approved": True}
    )
    assert response.status_code == 200
    assert response.json()["data"]["approved"] is True

def test_unapprove_restaurant(base_url):
    create = requests.post(
        f"{base_url}/api/v1/restaurants",
        json={"name": "Unapprove Cafe", "location": "Mumbai"}
    )
    rid = create.json()["rid"]
    response = requests.patch(
        f"{base_url}/api/v1/admin/restaurants/{rid}/approve",
        json={"approved": False}
    )
    assert response.status_code == 200
    assert response.json()["data"]["approved"] is False

def test_approve_restaurant_not_found(base_url):
    response = requests.patch(
        f"{base_url}/api/v1/admin/restaurants/9999/approve",
        json={"approved": True}
    )
    assert response.status_code == 404
    assert response.json()["message"] == "Restaurant Not Found"

def test_disable_restaurant(base_url):
    create = requests.post(
        f"{base_url}/api/v1/restaurants",
        json={"name": "Disable Cafe", "location": "Delhi"}
    )
    rid = create.json()["rid"]
    response = requests.patch(
        f"{base_url}/api/v1/admin/restaurants/{rid}/disable",
        json={"disabled": True}
    )
    assert response.status_code == 200
    assert response.json()["data"]["disabled"] is True

def test_enable_restaurant(base_url):
    create = requests.post(
        f"{base_url}/api/v1/restaurants",
        json={"name": "Enable Cafe", "location": "Mumbai"}
    )
    rid = create.json()["rid"]
    response = requests.patch(
        f"{base_url}/api/v1/admin/restaurants/{rid}/disable",
        json={"disabled": False}
    )
    assert response.status_code == 200
    assert response.json()["data"]["disabled"] is False

def test_disable_restaurant_not_found(base_url):
    response = requests.patch(
        f"{base_url}/api/v1/admin/restaurants/9999/disable",
        json={"disabled": True}
    )
    assert response.status_code == 404
    assert response.json()["message"] == "Restaurant Not Found"

def test_get_feedback_empty(base_url):
    response = requests.get(f"{base_url}/api/v1/admin/feedback")
    assert response.status_code == 200
    assert response.json() == []

def test_get_feedback_with_data(base_url):
    restaurant = requests.post(
        f"{base_url}/api/v1/restaurants",
        json={"name": "Feedback Cafe", "location": "Delhi"}
    )
    rid = restaurant.json()["rid"]
    requests.patch(
        f"{base_url}/api/v1/admin/restaurants/{rid}/approve",
        json={"approved": True}
    )
    user = requests.post(
        f"{base_url}/api/v1/users/register",
        json={"name": "Rahul", "email": "rahul@test.com", "password": "1234"}
    )
    uid = user.json()["uid"]
    dish = requests.post(
        f"{base_url}/api/v1/restaurants/{rid}/dishes",
        json={"name": "Pizza", "price": 200}
    )
    order = requests.post(
        f"{base_url}/api/v1/orders",
        json={"uid": uid, "rid": rid, "dishes": ["Pizza"]}
    )
    oid = order.json()["data"]["oid"]
    requests.post(
        f"{base_url}/api/v1/ratings",
        json={"oid": oid, "rating": 5, "feedback": "Great food"}
    )
    response = requests.get(f"{base_url}/api/v1/admin/feedback")
    assert response.status_code == 200
    assert len(response.json()) >= 1
    assert response.json()[0]["rating"] == 5

def test_get_orders_with_data(base_url):
    restaurant = requests.post(
        f"{base_url}/api/v1/restaurants",
        json={"name": "Orders Cafe", "location": "Delhi"}
    )
    rid = restaurant.json()["rid"]
    requests.patch(
        f"{base_url}/api/v1/admin/restaurants/{rid}/approve",
        json={"approved": True}
    )
    user = requests.post(
        f"{base_url}/api/v1/users/register",
        json={"name": "Aman", "email": "aman@test.com", "password": "1234"}
    )
    uid = user.json()["uid"]
    requests.post(
        f"{base_url}/api/v1/restaurants/{rid}/dishes",
        json={"name": "Pizza", "price": 200}
    )
    requests.post(
        f"{base_url}/api/v1/orders",
        json={"uid": uid, "rid": rid, "dishes": ["Pizza"]}
    )
    response = requests.get(f"{base_url}/api/v1/admin/orders")
    assert response.status_code == 200
    assert len(response.json()) >= 1

