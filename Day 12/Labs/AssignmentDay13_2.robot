*** Settings ***
Library           SeleniumLibrary
Suite Setup       Open Test Browser
Suite Teardown    Close Browser

*** Variables ***
${URL}            https://www.selenium.dev/selenium/web/web-form.html
${BROWSER}        chrome
${EXPECTED_MSG}   Received!

*** Keywords ***
Open Test Browser
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window

*** Test Cases ***
Form Submission Validation
    [Tags]    smoke    browser

    # Text box
    Input Text    name=my-text    Robot User

    # Radio button
    Click Element    css=input[value="option2"]

    # Check box
    Click Element    id=my-check-2

    # Drop-down
    Select From List By Label    name=my-select    Two

    Sleep    2s

    # Submit form
    Click Button    css=button[type="submit"]

    # Validation using Built-in keywords
    ${actual_msg}=    Get Text    id=message

    Run Keyword If    '${actual_msg}' == '${EXPECTED_MSG}'
    ...    Log    Form submitted successfully
    ...    ELSE    Fail    Form submission failed

    Should Be Equal    ${actual_msg}    ${EXPECTED_MSG}
