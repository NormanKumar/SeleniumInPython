*** Settings ***
Library           RequestsLibrary
Library           Collections
Suite Setup       Create Session    api    ${BASE_URL}
Suite Teardown    Delete All Sessions
Test Setup        Reset Test Data

*** Variables ***
${BASE_URL}       http://127.0.0.1:5000

*** Test Cases ***
Test Approve Restaurant
    [Documentation]    Test approving a restaurant
    ${restaurant}=    Create Restaurant    Approve Cafe    Delhi
    ${rid}=    Get From Dictionary    ${restaurant}    rid
    
    &{payload}=    Create Dictionary    approved=${True}
    ${response}=    PATCH On Session    api    /api/v1/admin/restaurants/${rid}/approve
    ...    json=${payload}
    ...    expected_status=200
    
    Should Be Equal As Numbers    ${response.status_code}    200
    ${data}=    Get From Dictionary    ${response.json()}    data
    ${approved}=    Get From Dictionary    ${data}    approved
    Should Be True    ${approved}

Test Unapprove Restaurant
    [Documentation]    Test unapproving a restaurant
    ${restaurant}=    Create Restaurant    Unapprove Cafe    Mumbai
    ${rid}=    Get From Dictionary    ${restaurant}    rid
    
    &{payload}=    Create Dictionary    approved=${False}
    ${response}=    PATCH On Session    api    /api/v1/admin/restaurants/${rid}/approve
    ...    json=${payload}
    ...    expected_status=200
    
    Should Be Equal As Numbers    ${response.status_code}    200
    ${data}=    Get From Dictionary    ${response.json()}    data
    ${approved}=    Get From Dictionary    ${data}    approved
    Should Not Be True    ${approved}

Test Approve Restaurant Not Found
    [Documentation]    Test approving a non-existent restaurant
    &{payload}=    Create Dictionary    approved=${True}
    ${response}=    PATCH On Session    api    /api/v1/admin/restaurants/9999/approve
    ...    json=${payload}
    ...    expected_status=404
    
    Should Be Equal As Numbers    ${response.status_code}    404
    ${message}=    Get From Dictionary    ${response.json()}    message
    Should Be Equal    ${message}    Restaurant Not Found

Test Disable Restaurant
    [Documentation]    Test disabling a restaurant
    ${restaurant}=    Create Restaurant    Disable Cafe    Delhi
    ${rid}=    Get From Dictionary    ${restaurant}    rid
    
    &{payload}=    Create Dictionary    disabled=${True}
    ${response}=    PATCH On Session    api    /api/v1/admin/restaurants/${rid}/disable
    ...    json=${payload}
    ...    expected_status=200
    
    Should Be Equal As Numbers    ${response.status_code}    200
    ${data}=    Get From Dictionary    ${response.json()}    data
    ${disabled}=    Get From Dictionary    ${data}    disabled
    Should Be True    ${disabled}

Test Enable Restaurant
    [Documentation]    Test enabling a restaurant
    ${restaurant}=    Create Restaurant    Enable Cafe    Mumbai
    ${rid}=    Get From Dictionary    ${restaurant}    rid
    
    &{payload}=    Create Dictionary    disabled=${False}
    ${response}=    PATCH On Session    api    /api/v1/admin/restaurants/${rid}/disable
    ...    json=${payload}
    ...    expected_status=200
    
    Should Be Equal As Numbers    ${response.status_code}    200
    ${data}=    Get From Dictionary    ${response.json()}    data
    ${disabled}=    Get From Dictionary    ${data}    disabled
    Should Not Be True    ${disabled}

Test Disable Restaurant Not Found
    [Documentation]    Test disabling a non-existent restaurant
    &{payload}=    Create Dictionary    disabled=${True}
    ${response}=    PATCH On Session    api    /api/v1/admin/restaurants/9999/disable
    ...    json=${payload}
    ...    expected_status=404
    
    Should Be Equal As Numbers    ${response.status_code}    404
    ${message}=    Get From Dictionary    ${response.json()}    message
    Should Be Equal    ${message}    Restaurant Not Found

Test Get Feedback Empty
    [Documentation]    Test getting feedback when none exists
    ${response}=    GET On Session    api    /api/v1/admin/feedback
    ...    expected_status=200
    
    Should Be Equal As Numbers    ${response.status_code}    200
    ${feedbacks}=    Set Variable    ${response.json()}
    Should Be Empty    ${feedbacks}

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
