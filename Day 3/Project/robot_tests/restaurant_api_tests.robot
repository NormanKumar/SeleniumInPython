*** Settings ***
Library    RequestsLibrary
Library    Collections
Library    BuiltIn

Suite Setup    Create Session    api    ${BASE_URL}
Suite Teardown    Delete All Sessions

*** Variables ***
${BASE_URL}    http://127.0.0.1:5000
${API_PATH}    /api/v1/restaurants

*** Test Cases ***
Test Register Restaurant Success
    [Documentation]    Test successful restaurant registration with all fields
    ${payload}=    Create Dictionary
    ...    name=Emirates Hotel
    ...    category=Indian
    ...    location=Delhi
    ...    contact=9999999999
    
    ${response}=    POST On Session    api    ${API_PATH}    json=${payload}    expected_status=201
    ${data}=    Set Variable    ${response.json()}
    
    Should Be Equal As Strings    ${data}[name]    Emirates Hotel
    Should Be Equal    ${data}[approved]    ${False}
    Should Be Equal    ${data}[disabled]    ${False}
    Should Be True    isinstance($data['dishes'], list)
    Should Be True    isinstance($data['feedback'], list)
    Should Be True    isinstance($data['orders'], list)

Test Duplicate Restaurant
    [Documentation]    Test that duplicate restaurant returns 409 error
    ${payload}=    Create Dictionary    name=CafeOne    location=Delhi
    
    POST On Session    api    ${API_PATH}    json=${payload}    expected_status=201
    ${response}=    POST On Session    api    ${API_PATH}    json=${payload}    expected_status=409
    ${data}=    Set Variable    ${response.json()}
    
    Should Be Equal As Strings    ${data}[message]    Restaurant Already Exist

Test Same Name Different Location
    [Documentation]    Test that same name with different location is allowed
    ${payload1}=    Create Dictionary    name=Global Cafe    location=Delhi
    ${payload2}=    Create Dictionary    name=Global Cafe    location=Mumbai
    
    POST On Session    api    ${API_PATH}    json=${payload1}    expected_status=201
    ${response}=    POST On Session    api    ${API_PATH}    json=${payload2}    expected_status=201
    
    Should Be Equal As Numbers    ${response.status_code}    201

Test Response Keys
    [Documentation]    Verify all expected keys are present in response
    ${payload}=    Create Dictionary    name=KeyTest    location=Chennai
    
    ${response}=    POST On Session    api    ${API_PATH}    json=${payload}    expected_status=201
    ${data}=    Set Variable    ${response.json()}
    
    @{expected_keys}=    Create List    rid    name    category    location    dishes    feedback    rating    orders    approved    disabled
    
    FOR    ${key}    IN    @{expected_keys}
        Dictionary Should Contain Key    ${data}    ${key}
    END

Test Update Restaurant Success
    [Documentation]    Test successful restaurant update
    ${create_payload}=    Create Dictionary    name=Update Cafe    location=Delhi
    ${response}=    POST On Session    api    ${API_PATH}    json=${create_payload}    expected_status=201
    ${rid}=    Set Variable    ${response.json()}[rid]
    
    ${update_payload}=    Create Dictionary    location=Mumbai
    ${response}=    PUT On Session    api    ${API_PATH}/${rid}    json=${update_payload}    expected_status=200
    ${data}=    Set Variable    ${response.json()}
    
    Should Be Equal As Strings    ${data}[message]    Updated restaurant
    Should Be Equal As Strings    ${data}[data][location]    Mumbai

Test Update Restaurant Not Found
    [Documentation]    Test update on non-existent restaurant returns 404
    ${payload}=    Create Dictionary    location=Pune
    
    ${response}=    PUT On Session    api    ${API_PATH}/9999    json=${payload}    expected_status=404
    ${data}=    Set Variable    ${response.json()}
    
    Should Be Equal As Strings    ${data}[message]    Restaurant Not Found

Test Update Name Field
    [Documentation]    Test updating restaurant name
    ${create_payload}=    Create Dictionary    name=Delhi Cafe 1    location=Delhi
    ${response}=    POST On Session    api    ${API_PATH}    json=${create_payload}    expected_status=201
    ${rid}=    Set Variable    ${response.json()}[rid]
    
    ${update_payload}=    Create Dictionary    name=New Name
    ${response}=    PUT On Session    api    ${API_PATH}/${rid}    json=${update_payload}    expected_status=200
    
    Should Be Equal As Numbers    ${response.status_code}    200

Test Update Category Field
    [Documentation]    Test updating restaurant category
    ${create_payload}=    Create Dictionary    name=Delhi Cafe 2    location=Delhi
    ${response}=    POST On Session    api    ${API_PATH}    json=${create_payload}    expected_status=201
    ${rid}=    Set Variable    ${response.json()}[rid]
    
    ${update_payload}=    Create Dictionary    category=Italian
    ${response}=    PUT On Session    api    ${API_PATH}/${rid}    json=${update_payload}    expected_status=200
    
    Should Be Equal As Numbers    ${response.status_code}    200

Test Update Contact Field
    [Documentation]    Test updating restaurant contact
    ${create_payload}=    Create Dictionary    name=Delhi Cafe 3    location=Delhi
    ${response}=    POST On Session    api    ${API_PATH}    json=${create_payload}    expected_status=201
    ${rid}=    Set Variable    ${response.json()}[rid]
    
    ${update_payload}=    Create Dictionary    contact=8888888888
    ${response}=    PUT On Session    api    ${API_PATH}/${rid}    json=${update_payload}    expected_status=200
    
    Should Be Equal As Numbers    ${response.status_code}    200

Test Disable Restaurant
    [Documentation]    Test disabling a restaurant
    ${create_payload}=    Create Dictionary    name=Disable Cafe    location=Delhi
    ${response}=    POST On Session    api    ${API_PATH}    json=${create_payload}    expected_status=201
    ${rid}=    Set Variable    ${response.json()}[rid]
    
    ${disable_payload}=    Create Dictionary    disabled=${True}
    ${response}=    PUT On Session    api    ${API_PATH}/${rid}/disable    json=${disable_payload}    expected_status=200
    ${data}=    Set Variable    ${response.json()}
    
    Should Be Equal    ${data}[data][disabled]    ${True}

Test Enable Restaurant
    [Documentation]    Test enabling a restaurant
    ${create_payload}=    Create Dictionary    name=Enable Cafe    location=Delhi
    ${response}=    POST On Session    api    ${API_PATH}    json=${create_payload}    expected_status=201
    ${rid}=    Set Variable    ${response.json()}[rid]
    
    ${enable_payload}=    Create Dictionary    disabled=${False}
    ${response}=    PUT On Session    api    ${API_PATH}/${rid}/disable    json=${enable_payload}    expected_status=200
    ${data}=    Set Variable    ${response.json()}
    
    Should Be Equal    ${data}[data][disabled]    ${False}

Test Disable Restaurant Not Found
    [Documentation]    Test disable on non-existent restaurant returns 404
    ${payload}=    Create Dictionary    disabled=${True}
    
    ${response}=    PUT On Session    api    ${API_PATH}/9999/disable    json=${payload}    expected_status=404
    ${data}=    Set Variable    ${response.json()}
    
    Should Be Equal As Strings    ${data}[message]    Restaurant Not Found

Test Get Restaurant Success
    [Documentation]    Test getting a restaurant by ID
    ${create_payload}=    Create Dictionary    name=Profile Cafe    location=Delhi
    ${response}=    POST On Session    api    ${API_PATH}    json=${create_payload}    expected_status=201
    ${rid}=    Set Variable    ${response.json()}[rid]
    
    ${response}=    GET On Session    api    ${API_PATH}/${rid}    expected_status=200
    ${data}=    Set Variable    ${response.json()}
    
    Should Be Equal    ${data}[rid]    ${rid}
    Should Be Equal As Strings    ${data}[name]    Profile Cafe

Test Get Restaurant Not Found
    [Documentation]    Test getting non-existent restaurant returns 404
    ${response}=    GET On Session    api    ${API_PATH}/9999    expected_status=404
    ${data}=    Set Variable    ${response.json()}
    
    Should Be Equal As Strings    ${data}[message]    Restaurant Not Found

Test Get All Restaurants
    [Documentation]    Test getting all restaurants returns list
    ${payload1}=    Create Dictionary    name=Cafe One    location=Delhi
    ${payload2}=    Create Dictionary    name=Cafe Two    location=Mumbai
    
    POST On Session    api    ${API_PATH}    json=${payload1}    expected_status=201
    POST On Session    api    ${API_PATH}    json=${payload2}    expected_status=201
    
    ${response}=    GET On Session    api    ${API_PATH}    expected_status=200
    ${data}=    Set Variable    ${response.json()}
    
    Should Be True    isinstance($data, list)
    ${length}=    Get Length    ${data}
    Should Be True    ${length} >= 2

Test Delete Restaurant Success
    [Documentation]    Test successful restaurant deletion
    ${create_payload}=    Create Dictionary    name=Delete Cafe    location=Delhi
    ${response}=    POST On Session    api    ${API_PATH}    json=${create_payload}    expected_status=201
    ${rid}=    Set Variable    ${response.json()}[rid]
    
    ${response}=    DELETE On Session    api    ${API_PATH}/${rid}/delete    expected_status=200
    ${data}=    Set Variable    ${response.json()}
    
    Should Be Equal As Strings    ${data}[message]    Restaurant Removed

Test Delete Restaurant Not Found
    [Documentation]    Test delete on non-existent restaurant returns 404
    ${response}=    DELETE On Session    api    ${API_PATH}/9999/delete    expected_status=404
    ${data}=    Set Variable    ${response.json()}
    
    Should Be Equal As Strings    ${data}[message]    Restaurant Not Found

Test Restaurant Deleted From List
    [Documentation]    Test that deleted restaurant is removed from list
    ${create_payload}=    Create Dictionary    name=Gone Cafe    location=Mumbai
    ${response}=    POST On Session    api    ${API_PATH}    json=${create_payload}    expected_status=201
    ${rid}=    Set Variable    ${response.json()}[rid]
    
    DELETE On Session    api    ${API_PATH}/${rid}/delete    expected_status=200
    
    ${response}=    GET On Session    api    ${API_PATH}    expected_status=200
    ${data}=    Set Variable    ${response.json()}
    
    @{ids}=    Create List
    FOR    ${restaurant}    IN    @{data}
        Append To List    ${ids}    ${restaurant}[rid]
    END
    
    List Should Not Contain Value    ${ids}    ${rid}

*** Keywords ***
Create Restaurant
    [Arguments]    ${name}    ${location}
    [Documentation]    Helper keyword to create a restaurant
    ${payload}=    Create Dictionary    name=${name}    location=${location}
    ${response}=    POST On Session    api    ${API_PATH}    json=${payload}    expected_status=201
    [Return]    ${response.json()}[rid]
