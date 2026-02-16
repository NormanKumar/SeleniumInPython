*** Settings ***
Library    RequestsLibrary
Library    Collections
Library    BuiltIn

Suite Setup    Create Session    api    ${BASE_URL}
Suite Teardown    Delete All Sessions

*** Variables ***
${BASE_URL}    http://127.0.0.1:5000
${USERS_API}    /api/v1/users
${RESTAURANTS_API}    /api/v1/restaurants
${DISHES_API}    /api/v1/dishes
${ORDERS_API}    /api/v1/orders
${RATINGS_API}    /api/v1/ratings
${ADMIN_API}    /api/v1/admin
${TEST_RESET}    /test/reset

*** Test Cases ***
Test Register User Success
    [Documentation]    Test successful user registration
    ${payload}=    Create Dictionary
    ...    name=Ravi
    ...    email=ravi@test.com
    ...    password=1234
    
    ${response}=    POST On Session    api    ${USERS_API}/register    json=${payload}    expected_status=201
    ${data}=    Set Variable    ${response.json()}
    
    Should Be Equal As Strings    ${data}[email]    ravi@test.com
    Dictionary Should Contain Key    ${data}    uid

Test Register User Duplicate Email
    [Documentation]    Test that duplicate email returns 409 error
    ${payload}=    Create Dictionary
    ...    name=Neha
    ...    email=neha@test.com
    ...    password=1111
    
    POST On Session    api    ${USERS_API}/register    json=${payload}    expected_status=201
    ${response}=    POST On Session    api    ${USERS_API}/register    json=${payload}    expected_status=409
    ${data}=    Set Variable    ${response.json()}
    
    Should Be Equal As Strings    ${data}[message]    User Already Exists

Test Multiple Users Registration 1
    [Documentation]    Test registering multiple users with different emails
    ${payload}=    Create Dictionary    name=User    email=a@test.com    password=1234
    ${response}=    POST On Session    api    ${USERS_API}/register    json=${payload}    expected_status=201
    Should Be Equal As Numbers    ${response.status_code}    201

Test Multiple Users Registration 2
    [Documentation]    Test registering multiple users with different emails
    ${payload}=    Create Dictionary    name=User    email=b@test.com    password=1234
    ${response}=    POST On Session    api    ${USERS_API}/register    json=${payload}    expected_status=201
    Should Be Equal As Numbers    ${response.status_code}    201

Test Multiple Users Registration 3
    [Documentation]    Test registering multiple users with different emails
    ${payload}=    Create Dictionary    name=User    email=c@test.com    password=1234
    ${response}=    POST On Session    api    ${USERS_API}/register    json=${payload}    expected_status=201
    Should Be Equal As Numbers    ${response.status_code}    201

Test Search By Name
    [Documentation]    Test searching restaurants by name
    Setup Search Data
    
    ${response}=    GET On Session    api    ${RESTAURANTS_API}/search    params=name=Spice Hub    expected_status=200
    ${data}=    Set Variable    ${response.json()}
    ${length}=    Get Length    ${data}
    
    Should Be True    ${length} >= 2

Test Search By Name And Location
    [Documentation]    Test searching restaurants by name and location
    Setup Search Data
    
    ${params}=    Create Dictionary    name=Spice Hub    location=Delhi
    ${response}=    GET On Session    api    ${RESTAURANTS_API}/search    params=${params}    expected_status=200
    ${data}=    Set Variable    ${response.json()}
    
    Should Be Equal As Strings    ${data}[0][location]    Delhi

Test Search By Dish
    [Documentation]    Test searching restaurants by dish name
    Setup Search Data
    
    ${response}=    GET On Session    api    ${RESTAURANTS_API}/search    params=dish=Pizza    expected_status=200
    ${data}=    Set Variable    ${response.json()}
    
    Should Be Equal As Strings    ${data}[0][name]    Spice Hub

Test Search Location Not Found
    [Documentation]    Test search with unserviceable location
    ${response}=    GET On Session    api    ${RESTAURANTS_API}/search    params=location=Chennai    expected_status=404
    ${data}=    Set Variable    ${response.json()}
    
    Should Be Equal As Strings    ${data}[message]    Location unserviceable

Test Search Restaurant Not Found
    [Documentation]    Test search with non-existent restaurant name
    ${response}=    GET On Session    api    ${RESTAURANTS_API}/search    params=name=Unknown Cafe    expected_status=404
    ${data}=    Set Variable    ${response.json()}
    
    Should Be Equal As Strings    ${data}[message]    Restaurant not found

Test Search Dish Not Found
    [Documentation]    Test search with non-existent dish
    Setup Search Data
    
    ${response}=    GET On Session    api    ${RESTAURANTS_API}/search    params=dish=Pasta    expected_status=404
    ${data}=    Set Variable    ${response.json()}
    
    Should Be Equal As Strings    ${data}[message]    No dish found in this restaurant/location

Test Search Multiple Filters Name
    [Documentation]    Test search with name filter
    Setup Search Data
    ${response}=    GET On Session    api    ${RESTAURANTS_API}/search    params=name=Spice Hub    expected_status=200
    Should Be Equal As Numbers    ${response.status_code}    200

Test Search Multiple Filters Location
    [Documentation]    Test search with location filter
    Setup Search Data
    ${response}=    GET On Session    api    ${RESTAURANTS_API}/search    params=location=Delhi    expected_status=200
    Should Be Equal As Numbers    ${response.status_code}    200

Test Search Multiple Filters Dish
    [Documentation]    Test search with dish filter
    Setup Search Data
    ${response}=    GET On Session    api    ${RESTAURANTS_API}/search    params=dish=Burger    expected_status=200
    Should Be Equal As Numbers    ${response.status_code}    200

Test Order Success
    [Documentation]    Test successful order placement
    ${rid}    ${uid}=    Setup Order Environment
    
    ${dishes}=    Create List    Pizza    Burger
    ${payload}=    Create Dictionary    uid=${uid}    rid=${rid}    dishes=${dishes}
    
    ${response}=    POST On Session    api    ${ORDERS_API}    json=${payload}    expected_status=201
    ${data}=    Set Variable    ${response.json()}[data]
    
    Should Be Equal As Numbers    ${data}[total]    270
    Should Contain    ${data}[dishes]    Pizza
    Should Contain    ${data}[dishes]    Burger

Test Order Without Dishes
    [Documentation]    Test order placement without dishes returns 400
    ${payload}=    Create Dictionary    uid=${1}    rid=${1}
    
    ${response}=    POST On Session    api    ${ORDERS_API}    json=${payload}    expected_status=400
    ${data}=    Set Variable    ${response.json()}
    
    Should Be Equal As Strings    ${data}[message]    Add at least one dish

Test Order User Not Found
    [Documentation]    Test order with non-existent user
    ${dishes}=    Create List    Pizza
    ${payload}=    Create Dictionary    uid=${9999}    rid=${1}    dishes=${dishes}
    
    ${response}=    POST On Session    api    ${ORDERS_API}    json=${payload}    expected_status=404
    ${data}=    Set Variable    ${response.json()}
    
    Should Be Equal As Strings    ${data}[message]    User not found

Test Order Restaurant Not Found
    [Documentation]    Test order with non-existent restaurant
    POST On Session    api    ${TEST_RESET}    expected_status=any
    
    ${user_payload}=    Create Dictionary    name=U    email=u@test.com    password=1
    ${user}=    POST On Session    api    ${USERS_API}/register    json=${user_payload}    expected_status=201
    ${uid}=    Set Variable    ${user.json()}[uid]
    
    ${dishes}=    Create List    Pizza
    ${payload}=    Create Dictionary    uid=${uid}    rid=${9999}    dishes=${dishes}
    
    ${response}=    POST On Session    api    ${ORDERS_API}    json=${payload}    expected_status=404
    ${data}=    Set Variable    ${response.json()}
    
    Should Be Equal As Strings    ${data}[message]    Restaurant not found

Test Order Invalid Dish
    [Documentation]    Test order with invalid dish name
    ${rid}    ${uid}=    Setup Order Environment
    
    ${dishes}=    Create List    Pasta
    ${payload}=    Create Dictionary    uid=${uid}    rid=${rid}    dishes=${dishes}
    
    ${response}=    POST On Session    api    ${ORDERS_API}    json=${payload}    expected_status=400
    ${message}=    Set Variable    ${response.json()}[message]
    
    Should Contain    ${message}    not available

Test Order Disabled Dish
    [Documentation]    Test order with disabled dish returns 400
    ${rid}    ${uid}=    Setup Order Environment
    
    ${dishes_list}=    GET On Session    api    ${DISHES_API}    expected_status=200
    ${did}=    Set Variable    ${dishes_list.json()}[0][did]
    
    ${disable_payload}=    Create Dictionary    disabled=${True}
    PATCH On Session    api    ${DISHES_API}/${did}/status    json=${disable_payload}    expected_status=200
    
    ${order_dishes}=    Create List    Pizza
    ${order_payload}=    Create Dictionary    uid=${uid}    rid=${rid}    dishes=${order_dishes}
    
    ${response}=    POST On Session    api    ${ORDERS_API}    json=${order_payload}    expected_status=400
    Should Be Equal As Numbers    ${response.status_code}    400

Test Add Feedback Success
    [Documentation]    Test adding feedback to an order
    ${oid}=    Setup Rating Environment
    
    ${payload}=    Create Dictionary    oid=${oid}    rating=${5}    feedback=Excellent!
    ${response}=    POST On Session    api    ${RATINGS_API}    json=${payload}    expected_status=201
    ${data}=    Set Variable    ${response.json()}
    
    Should Be Equal As Strings    ${data}[message]    Feedback added

Test Average Rating
    [Documentation]    Test that average rating is calculated correctly
    ${oid}=    Setup Rating Environment
    
    ${payload1}=    Create Dictionary    oid=${oid}    rating=${4}    feedback=Good
    POST On Session    api    ${RATINGS_API}    json=${payload1}    expected_status=201
    
    ${payload2}=    Create Dictionary    oid=${oid}    rating=${2}    feedback=Okay
    ${response}=    POST On Session    api    ${RATINGS_API}    json=${payload2}    expected_status=201
    ${data}=    Set Variable    ${response.json()}
    
    Should Be Equal As Numbers    ${data}[rating]    3

Test Rating Order Not Found
    [Documentation]    Test rating with non-existent order
    ${payload}=    Create Dictionary    oid=${9999}    rating=${5}    feedback=Nice
    
    ${response}=    POST On Session    api    ${RATINGS_API}    json=${payload}    expected_status=404
    ${data}=    Set Variable    ${response.json()}
    
    Should Be Equal As Strings    ${data}[message]    Order not found

Test Update User Success
    [Documentation]    Test successful user profile update
    ${user_payload}=    Create Dictionary    name=Rohit    email=rohit@test.com    password=123
    ${user}=    POST On Session    api    ${USERS_API}/register    json=${user_payload}    expected_status=201
    ${uid}=    Set Variable    ${user.json()}[uid]
    
    ${update_payload}=    Create Dictionary    name=Rohit Sharma
    ${response}=    PUT On Session    api    /api/v1/${uid}/update    json=${update_payload}    expected_status=200
    ${data}=    Set Variable    ${response.json()}
    
    Should Be Equal As Strings    ${data}[data][name]    Rohit Sharma

Test Update User Not Found
    [Documentation]    Test update on non-existent user
    ${payload}=    Create Dictionary    name=Nobody
    
    ${response}=    PUT On Session    api    /api/v1/9999/update    json=${payload}    expected_status=404
    ${data}=    Set Variable    ${response.json()}
    
    Should Be Equal As Strings    ${data}[message]    User Not Found

Test Update User Name Field
    [Documentation]    Test updating user name field
    POST On Session    api    ${TEST_RESET}    expected_status=any
    
    ${user_payload}=    Create Dictionary    name=Test    email=field@test.com    password=111
    ${user}=    POST On Session    api    ${USERS_API}/register    json=${user_payload}    expected_status=201
    ${uid}=    Set Variable    ${user.json()}[uid]
    
    ${update_payload}=    Create Dictionary    name=New Name
    ${response}=    PUT On Session    api    /api/v1/${uid}/update    json=${update_payload}    expected_status=200
    Should Be Equal As Numbers    ${response.status_code}    200

Test Update User Password Field
    [Documentation]    Test updating user password field
    POST On Session    api    ${TEST_RESET}    expected_status=any
    
    ${user_payload}=    Create Dictionary    name=Test    email=pass@test.com    password=111
    ${user}=    POST On Session    api    ${USERS_API}/register    json=${user_payload}    expected_status=201
    ${uid}=    Set Variable    ${user.json()}[uid]
    
    ${update_payload}=    Create Dictionary    password=newpass
    ${response}=    PUT On Session    api    /api/v1/${uid}/update    json=${update_payload}    expected_status=200
    Should Be Equal As Numbers    ${response.status_code}    200

Test Update User Email Field
    [Documentation]    Test updating user email field
    POST On Session    api    ${TEST_RESET}    expected_status=any
    
    ${user_payload}=    Create Dictionary    name=Test    email=email@test.com    password=111
    ${user}=    POST On Session    api    ${USERS_API}/register    json=${user_payload}    expected_status=201
    ${uid}=    Set Variable    ${user.json()}[uid]
    
    ${update_payload}=    Create Dictionary    email=new@email.com
    ${response}=    PUT On Session    api    /api/v1/${uid}/update    json=${update_payload}    expected_status=200
    Should Be Equal As Numbers    ${response.status_code}    200

Test Delete User Success
    [Documentation]    Test successful user deletion
    ${user_payload}=    Create Dictionary    name=Delete Me    email=del@test.com    password=123
    ${user}=    POST On Session    api    ${USERS_API}/register    json=${user_payload}    expected_status=201
    ${uid}=    Set Variable    ${user.json()}[uid]
    
    ${response}=    DELETE On Session    api    /api/v1/${uid}/delete    expected_status=200
    ${data}=    Set Variable    ${response.json()}
    
    Should Be Equal As Strings    ${data}[message]    User Profile Deleted

Test Delete User Not Found
    [Documentation]    Test delete on non-existent user
    ${response}=    DELETE On Session    api    /api/v1/9999/delete    expected_status=404
    ${data}=    Set Variable    ${response.json()}
    
    Should Be Equal As Strings    ${data}[message]    User Not Found

Test User Removed From System
    [Documentation]    Test that deleted user cannot be updated
    ${user_payload}=    Create Dictionary    name=Gone    email=gone@test.com    password=123
    ${user}=    POST On Session    api    ${USERS_API}/register    json=${user_payload}    expected_status=201
    ${uid}=    Set Variable    ${user.json()}[uid]
    
    DELETE On Session    api    /api/v1/${uid}/delete    expected_status=200
    
    ${update_payload}=    Create Dictionary    name=Should Fail
    ${response}=    PUT On Session    api    /api/v1/${uid}/update    json=${update_payload}    expected_status=404
    
    Should Be Equal As Numbers    ${response.status_code}    404

*** Keywords ***
Setup Search Data
    [Documentation]    Setup test data for restaurant search tests
    POST On Session    api    ${TEST_RESET}    expected_status=any
    
    ${r1_payload}=    Create Dictionary    name=Spice Hub    location=Delhi
    ${r1}=    POST On Session    api    ${RESTAURANTS_API}    json=${r1_payload}    expected_status=201
    ${r1_data}=    Set Variable    ${r1.json()}
    
    ${r2_payload}=    Create Dictionary    name=Spice Hub    location=Mumbai
    ${r2}=    POST On Session    api    ${RESTAURANTS_API}    json=${r2_payload}    expected_status=201
    ${r2_data}=    Set Variable    ${r2.json()}
    
    ${approve_payload}=    Create Dictionary    approved=${True}
    PATCH On Session    api    ${ADMIN_API}/restaurants/${r1_data}[rid]/approve    json=${approve_payload}    expected_status=200
    PATCH On Session    api    ${ADMIN_API}/restaurants/${r2_data}[rid]/approve    json=${approve_payload}    expected_status=200
    
    ${dish1_payload}=    Create Dictionary    name=Pizza    price=${150}
    POST On Session    api    ${RESTAURANTS_API}/${r1_data}[rid]/dishes    json=${dish1_payload}    expected_status=201
    
    ${dish2_payload}=    Create Dictionary    name=Burger    price=${120}
    POST On Session    api    ${RESTAURANTS_API}/${r2_data}[rid]/dishes    json=${dish2_payload}    expected_status=201

Setup Order Environment
    [Documentation]    Setup test data for order tests - returns rid and uid
    POST On Session    api    ${TEST_RESET}    expected_status=any
    
    ${restaurant_payload}=    Create Dictionary    name=Order Cafe    location=Delhi
    ${restaurant}=    POST On Session    api    ${RESTAURANTS_API}    json=${restaurant_payload}    expected_status=201
    ${rid}=    Set Variable    ${restaurant.json()}[rid]
    
    ${approve_payload}=    Create Dictionary    approved=${True}
    PATCH On Session    api    ${ADMIN_API}/restaurants/${rid}/approve    json=${approve_payload}    expected_status=200
    
    ${dish1_payload}=    Create Dictionary    name=Pizza    price=${150}
    POST On Session    api    ${RESTAURANTS_API}/${rid}/dishes    json=${dish1_payload}    expected_status=201
    
    ${dish2_payload}=    Create Dictionary    name=Burger    price=${120}
    POST On Session    api    ${RESTAURANTS_API}/${rid}/dishes    json=${dish2_payload}    expected_status=201
    
    ${user_payload}=    Create Dictionary    name=Order User    email=order@test.com    password=123
    ${user}=    POST On Session    api    ${USERS_API}/register    json=${user_payload}    expected_status=201
    ${uid}=    Set Variable    ${user.json()}[uid]
    
    [Return]    ${rid}    ${uid}

Setup Rating Environment
    [Documentation]    Setup test data for rating tests - returns oid
    POST On Session    api    ${TEST_RESET}    expected_status=any
    
    ${restaurant_payload}=    Create Dictionary    name=Rating Cafe    location=Delhi
    ${restaurant}=    POST On Session    api    ${RESTAURANTS_API}    json=${restaurant_payload}    expected_status=201
    ${rid}=    Set Variable    ${restaurant.json()}[rid]
    
    ${approve_payload}=    Create Dictionary    approved=${True}
    PATCH On Session    api    ${ADMIN_API}/restaurants/${rid}/approve    json=${approve_payload}    expected_status=200
    
    ${dish_payload}=    Create Dictionary    name=Burger    price=${100}
    POST On Session    api    ${RESTAURANTS_API}/${rid}/dishes    json=${dish_payload}    expected_status=201
    
    ${user_payload}=    Create Dictionary    name=Rate User    email=rate@test.com    password=123
    ${user}=    POST On Session    api    ${USERS_API}/register    json=${user_payload}    expected_status=201
    ${uid}=    Set Variable    ${user.json()}[uid]
    
    ${dishes}=    Create List    Burger
    ${order_payload}=    Create Dictionary    uid=${uid}    rid=${rid}    dishes=${dishes}
    ${order}=    POST On Session    api    ${ORDERS_API}    json=${order_payload}    expected_status=201
    ${oid}=    Set Variable    ${order.json()}[data][oid]
    
    [Return]    ${oid}
