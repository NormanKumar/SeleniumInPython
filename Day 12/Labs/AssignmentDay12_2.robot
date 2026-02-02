
*** Settings ***
Library    DataDriver    file=${CURDIR}/data.csv    dialect=unix    delimiter=,
Test Template    Login Test Flow

*** Variables ***
${valid_user}    admin
${valid_password}    admin123

*** Keywords ***
Login Test Flow
    [Arguments]    ${username}    ${password}     ${expected_result}
    Open Application
    Input Username    ${username}
    Input Password    ${password}
    Click Login Button
    Validate Login     ${username}    ${password}    ${expected_result}

Open Application
    Log To Console     Application opened

Input Username
    [Arguments]    ${username}
    Log To Console     Username entered: ${username}
Input Password
    [Arguments]    ${password}
    Log To Console     Password entered: ${password}
Click Login Button
    Log To Console     Login button clicked
Validate Login
    [Arguments]    ${username}    ${password}    ${expected_result}
    IF    $username == $valid_user and $password == $valid_password
        ${result} =    Set Variable    success
    ELSE
        ${result} =    Set Variable    failure
    END
    Log To Console    Expected: ${expected_result} | Actual: ${result}
    Should Be Equal    ${result}    ${expected_result}

*** Test Cases ***
Login Test with CSV Data
