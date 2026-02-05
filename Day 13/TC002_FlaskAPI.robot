*** Settings ***
Library    RequestsLibrary

*** Variables ***
${url}    http://127.0.0.1:5000
*** Test Cases ***

Verify get-single=user

    Create Session    Mysession    ${url}
    # Create Session    Mysession    ${url}
    ${response}=    GET On Session    Mysession    /users/2
    Status Should Be    200    ${response}
    # ${resp.json}=    To Json    ${response.content} // Deprecated
    Log To Console    ${response.json()}

Verify user-not-found

    ${response}=    GET On Session    Mysession    /users/4
    Status Should Be    200    ${response}
    # ${resp.json}=    To Json    ${response.content} // Deprecated
    Log To Console    ${response.json()}

verify create-user
    ${data}=    Create Dictionary    name=Bhanu
    ${response}=    POST On Session    Mysession    /users    json=${data}
    Status Should Be    201    ${response}
    Log To Console    ${response.json()}

Verify update-user(put)
    ${data}=    Create Dictionary    name=bhanuprasad
    ${response}=    PUT On Session    Mysession    /users/2    json=${data}
    Status Should Be    200    ${response}
    Log To Console    ${response.json()}
verify update-user(patch)
    ${data}=    Create Dictionary    name=bhanupatched
    ${response}=    PATCH On Session    Mysession    /users/2    json=${data}
    Status Should Be    200    ${response}
    Log To Console    ${response.json()}

Verify get-all-user

    ${response}=    GET On Session    Mysession    /users
    Status Should Be    200    ${response}
    # ${resp.json}=    To Json    ${response.content} // Deprecated
    Log To Console    ${response.json()}
verify delete-user
    ${response}=    DELETE On Session    Mysession    /users/3
    Status Should Be    200    ${response}
    Log To Console    ${response.json()}