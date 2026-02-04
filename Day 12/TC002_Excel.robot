*** Settings ***
Library    SeleniumLibrary
Library    DataDriver    ${CURDIR}/Datasheet.xlsx    Sheet1    dialect=Excel
Suite Setup       Open Orangehrm
Test Template     Orangehrmlogin With Excel
Suite Teardown    Close All Browsers

*** Variables ***
${url}      https://opensource-demo.orangehrmlive.com/web/index.php/auth/login
${browser}  chrome

*** Keywords ***
Open Orangehrm
    Open Browser    ${url}    ${browser}
    Maximize Browser Window

Orangehrmlogin With Excel
    [Arguments]    ${username}    ${password}
    Sleep   5s
    Wait Until Element Is Visible    name=username    10s
    Input Text    name=username    ${username}
    Input Text    name=password    ${password}
    Click Button    xpath=//button[@type="submit"]
    Sleep   10s
    Click Element    xpath=//*[@id="app"]/div[1]/div[1]/header/div[1]/div[3]/ul/li/span
    # Click Element    xpath=//*[@id="app"]/div[1]/div[1]/header/div[1]/div[3]/ul/li/ul/li[4]
    Click Link    Logout


# *** Test Cases ***
# Login with user from Excel
#     [Tags]    DDT