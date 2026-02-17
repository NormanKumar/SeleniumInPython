*** Settings ***
Library    RequestsLibrary
Library    Collections
Library    BuiltIn

Suite Setup    Create Session    api    ${BASE_URL}
Suite Teardown    Delete All Sessions

*** Variables ***
${BASE_URL}    http://127.0.0.1:5000
${RESTAURANTS_API}    /api/v1/restaurants
${DISHES_API}    /api/v1/dishes

*** Test Cases ***
Test Add Dish Success
    [Documentation]    Test successful dish addition to a restaurant
    ${rid}=    Create Test Restaurant    Dish Cafe    Delhi
    
    ${payload}=    Create Dictionary
    ...    name=Pizza
    ...    type=Veg
    ...    price=${250}
    ...    time=20 min
    
    ${response}=    POST On Session    api    ${RESTAURANTS_API}/${rid}/dishes    json=${payload}    expected_status=201
    ${data}=    Set Variable    ${response.json()}
    
    Should Be Equal As Strings    ${data}[name]    Pizza
    Should Be Equal    ${data}[rid]    ${rid}

Test Add Duplicate Dish
    [Documentation]    Test that duplicate dish returns 409 error
    ${rid}=    Create Test Restaurant    Dup Dish Cafe    Mumbai
    
    ${payload}=    Create Dictionary
    ...    name=Burger
    ...    type=Veg
    ...    price=${150}
    
    POST On Session    api    ${RESTAURANTS_API}/${rid}/dishes    json=${payload}    expected_status=201
    ${response}=    POST On Session    api    ${RESTAURANTS_API}/${rid}/dishes    json=${payload}    expected_status=409
    ${data}=    Set Variable    ${response.json()}
    
    Should Be Equal As Strings    ${data}[message]    Dish Already Exist

Test Add Dish Restaurant Not Found
    [Documentation]    Test adding dish to non-existent restaurant returns 404
    ${payload}=    Create Dictionary    name=Pasta    price=${200}
    
    ${response}=    POST On Session    api    ${RESTAURANTS_API}/9999/dishes    json=${payload}    expected_status=404
    ${data}=    Set Variable    ${response.json()}
    
    Should Be Equal As Strings    ${data}[message]    Restaurant Not Found

Test Update Dish Success
    [Documentation]    Test successful dish update
    ${rid}=    Create Test Restaurant    Update Dish Cafe    Delhi
    ${did}=    Create Test Dish    ${rid}    Pizza    ${200}
    
    ${update_payload}=    Create Dictionary    price=${300}
    ${response}=    PUT On Session    api    ${DISHES_API}/${did}    json=${update_payload}    expected_status=200
    ${data}=    Set Variable    ${response.json()}
    
    Should Be Equal As Numbers    ${data}[data][price]    300

Test Update Dish Not Found
    [Documentation]    Test update on non-existent dish returns 404
    ${payload}=    Create Dictionary    price=${100}
    
    ${response}=    PUT On Session    api    ${DISHES_API}/9999    json=${payload}    expected_status=404
    ${data}=    Set Variable    ${response.json()}
    
    Should Be Equal As Strings    ${data}[message]    Dish Not Found

Test Update Dish Name Field
    [Documentation]    Test updating dish name
    ${rid}=    Create Test Restaurant    Multi Dish Cafe 1    Mumbai
    ${did}=    Create Test Dish    ${rid}    Burger    ${120}
    
    ${update_payload}=    Create Dictionary    name=New Dish Name
    ${response}=    PUT On Session    api    ${DISHES_API}/${did}    json=${update_payload}    expected_status=200
    
    Should Be Equal As Numbers    ${response.status_code}    200

Test Update Dish Price Field
    [Documentation]    Test updating dish price
    ${rid}=    Create Test Restaurant    Multi Dish Cafe 2    Mumbai
    ${did}=    Create Test Dish    ${rid}    Burger    ${120}
    
    ${update_payload}=    Create Dictionary    price=${180}
    ${response}=    PUT On Session    api    ${DISHES_API}/${did}    json=${update_payload}    expected_status=200
    
    Should Be Equal As Numbers    ${response.status_code}    200

Test Update Dish Time Field
    [Documentation]    Test updating dish preparation time
    ${rid}=    Create Test Restaurant    Multi Dish Cafe 3    Mumbai
    ${did}=    Create Test Dish    ${rid}    Burger    ${120}
    
    ${update_payload}=    Create Dictionary    time=15 min
    ${response}=    PUT On Session    api    ${DISHES_API}/${did}    json=${update_payload}    expected_status=200
    
    Should Be Equal As Numbers    ${response.status_code}    200

Test Disable Dish
    [Documentation]    Test disabling a dish
    ${rid}=    Create Test Restaurant    Status Dish Cafe    Delhi
    ${did}=    Create Test Dish    ${rid}    Pizza    ${200}
    
    ${payload}=    Create Dictionary    disabled=${True}
    ${response}=    PATCH On Session    api    ${DISHES_API}/${did}/status    json=${payload}    expected_status=200
    ${data}=    Set Variable    ${response.json()}
    
    Should Be Equal    ${data}[data][disabled]    ${True}

Test Enable Dish
    [Documentation]    Test enabling a dish
    ${rid}=    Create Test Restaurant    Enable Dish Cafe    Mumbai
    ${did}=    Create Test Dish    ${rid}    Burger    ${150}
    
    ${payload}=    Create Dictionary    disabled=${False}
    ${response}=    PATCH On Session    api    ${DISHES_API}/${did}/status    json=${payload}    expected_status=200
    ${data}=    Set Variable    ${response.json()}
    
    Should Be Equal    ${data}[data][disabled]    ${False}

Test Disable Dish Not Found
    [Documentation]    Test disable on non-existent dish returns 404
    ${payload}=    Create Dictionary    disabled=${True}
    
    ${response}=    PATCH On Session    api    ${DISHES_API}/9999/status    json=${payload}    expected_status=404
    ${data}=    Set Variable    ${response.json()}
    
    Should Be Equal As Strings    ${data}[message]    Dish Not Found

Test Delete Dish Success
    [Documentation]    Test successful dish deletion
    ${rid}=    Create Test Restaurant    Delete Dish Cafe    Delhi
    ${did}=    Create Test Dish    ${rid}    Pizza    ${200}
    
    ${response}=    DELETE On Session    api    ${DISHES_API}/${did}/delete    expected_status=200
    ${data}=    Set Variable    ${response.json()}
    
    Should Be Equal As Strings    ${data}[message]    Dish Removed

Test Delete Dish Not Found
    [Documentation]    Test delete on non-existent dish returns 404
    ${response}=    DELETE On Session    api    ${DISHES_API}/9999/delete    expected_status=404
    ${data}=    Set Variable    ${response.json()}
    
    Should Be Equal As Strings    ${data}[message]    Dish Not Found

Test Dish Removed From List
    [Documentation]    Test that deleted dish is removed from list
    ${rid}=    Create Test Restaurant    Gone Dish Cafe    Mumbai
    ${did}=    Create Test Dish    ${rid}    Burger    ${150}
    
    DELETE On Session    api    ${DISHES_API}/${did}/delete    expected_status=200
    
    ${response}=    GET On Session    api    ${DISHES_API}    expected_status=200
    ${data}=    Set Variable    ${response.json()}
    
    @{ids}=    Create List
    FOR    ${dish}    IN    @{data}
        Append To List    ${ids}    ${dish}[did]
    END
    
    List Should Not Contain Value    ${ids}    ${did}

Test Get All Dishes With Data
    [Documentation]    Test getting all dishes returns list with data
    ${rid}=    Create Test Restaurant    Dish List Cafe    Delhi
    
    ${payload1}=    Create Dictionary    name=Pizza    price=${200}
    ${payload2}=    Create Dictionary    name=Burger    price=${150}
    
    POST On Session    api    ${RESTAURANTS_API}/${rid}/dishes    json=${payload1}    expected_status=201
    POST On Session    api    ${RESTAURANTS_API}/${rid}/dishes    json=${payload2}    expected_status=201
    
    ${response}=    GET On Session    api    ${DISHES_API}    expected_status=200
    ${data}=    Set Variable    ${response.json()}
    
    Should Be True    isinstance($data, list)
    ${length}=    Get Length    ${data}
    Should Be True    ${length} >= 2

Test Get All Dishes Empty
    [Documentation]    Test getting all dishes returns empty list when no dishes exist
    ${response}=    GET On Session    api    ${DISHES_API}    expected_status=200
    ${data}=    Set Variable    ${response.json()}
    
    Should Be True    isinstance($data, list)

*** Keywords ***
Create Test Restaurant
    [Arguments]    ${name}    ${location}
    [Documentation]    Helper keyword to create a restaurant and return its ID
    ${payload}=    Create Dictionary    name=${name}    location=${location}
    ${response}=    POST On Session    api    ${RESTAURANTS_API}    json=${payload}    expected_status=201
    ${rid}=    Set Variable    ${response.json()}[rid]
    [Return]    ${rid}

Create Test Dish
    [Arguments]    ${rid}    ${dish_name}    ${price}
    [Documentation]    Helper keyword to create a dish and return its ID
    ${payload}=    Create Dictionary    name=${dish_name}    price=${price}
    ${response}=    POST On Session    api    ${RESTAURANTS_API}/${rid}/dishes    json=${payload}    expected_status=201
    ${did}=    Set Variable    ${response.json()}[did]
    [Return]    ${did}
