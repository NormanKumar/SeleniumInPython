*** Settings ***
Library           RequestsLibrary
Library           Collections
Suite Setup       Create Session    api    ${BASE_URL}
Suite Teardown    Delete All Sessions
Test Setup        Reset Test Data

*** Variables ***
${BASE_URL}       http://127.0.0.1:5000

*** Test Cases ***
Test User Orders Empty
    [Documentation]    Test getting orders for a user with no orders
    ${user}=    Create User    Empty    empty@test.com    123
    ${uid}=    Get From Dictionary    ${user}    uid
    
    ${response}=    GET On Session    api    /api/v1/users/${uid}/orders
    ...    expected_status=200
    
    Should Be Equal As Numbers    ${response.status_code}    200
    ${message}=    Get From Dictionary    ${response.json()}    message
    Should Be Equal    ${message}    No Orders Yet

Test User Orders Not Found
    [Documentation]    Test getting orders for a non-existent user
    ${response}=    GET On Session    api    /api/v1/users/9999/orders
    ...    expected_status=404
    
    Should Be Equal As Numbers    ${response.status_code}    404
    ${message}=    Get From Dictionary    ${response.json()}    message
    Should Be Equal    ${message}    User Not Found

Test Restaurant Orders Empty
    [Documentation]    Test getting orders for a restaurant with no orders
    ${restaurant}=    Create Restaurant    Empty Orders Cafe    Delhi
    ${rid}=    Get From Dictionary    ${restaurant}    rid
    
    ${response}=    GET On Session    api    /api/v1/restaurants/${rid}/orders
    ...    expected_status=200
    
    Should Be Equal As Numbers    ${response.status_code}    200
    ${message}=    Get From Dictionary    ${response.json()}    message
    Should Be Equal    ${message}    No Orders Yet

Test Restaurant Orders Not Found
    [Documentation]    Test getting orders for a non-existent restaurant
    ${response}=    GET On Session    api    /api/v1/restaurants/9999/orders
    ...    expected_status=404
    
    Should Be Equal As Numbers    ${response.status_code}    404
    ${message}=    Get From Dictionary    ${response.json()}    message
    Should Be Equal    ${message}    Restaurant Not Found

*** Keywords ***
Reset Test Data
    [Documentation]    Reset all test data before each test
    POST On Session    api    /test/reset    expected_status=200

Create Restaurant
    [Arguments]    ${name}    ${location}
    [Documentation]    Create a restaurant and return the response JSON
    &{payload}=    Create Dictionary    name=${name}    location=${location}
    ${response}=    POST On Session    api    /api/v1/restaurants
    ...    json=${payload}
    ...    expected_status=201
    ${restaurant}=    Set Variable    ${response.json()}
    RETURN    ${restaurant}

Create User
    [Arguments]    ${name}    ${email}    ${password}
    [Documentation]    Create a user and return the response JSON
    &{payload}=    Create Dictionary    name=${name}    email=${email}    password=${password}
    ${response}=    POST On Session    api    /api/v1/users/register
    ...    json=${payload}
    ...    expected_status=201
    ${user}=    Set Variable    ${response.json()}
    RETURN    ${user}

Create Dish
    [Arguments]    ${rid}    ${dish_name}    ${price}
    [Documentation]    Create a dish for a restaurant
    &{payload}=    Create Dictionary    name=${dish_name}    price=${price}
    ${response}=    POST On Session    api    /api/v1/restaurants/${rid}/dishes
    ...    json=${payload}
    ...    expected_status=201
    ${dish}=    Set Variable    ${response.json()}
    RETURN    ${dish}

Place Order
    [Arguments]    ${uid}    ${rid}    ${dish_name}
    [Documentation]    Place an order
    @{dishes}=    Create List    ${dish_name}
    &{payload}=    Create Dictionary    uid=${uid}    rid=${rid}    dishes=${dishes}
    ${response}=    POST On Session    api    /api/v1/orders
    ...    json=${payload}
    ...    expected_status=201
    ${order}=    Set Variable    ${response.json()}
    RETURN    ${order}
