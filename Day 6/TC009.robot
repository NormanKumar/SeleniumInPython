*** Settings ***
Library    SeleniumLibrary
Library    DataDriver    file=C:/Users/KIIT/Desktop/Wipro/Robot/Register.csv    encoding=utf_8    dialect=excel
Test Template    RegisterWithExcel

*** Variables ***
${URL}        https://tutorialsninja.com/demo/index.php?route=account/register
${BROWSER}    edge

*** Test Cases ***
Register Test

*** Keywords ***
RegisterWithExcel
    [Arguments]    ${firstname}    ${lastname}    ${email}    ${telephone}    ${password}    ${confirm}
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Wait Until Element Is Visible    name=firstname    10s
    Input Text    name=firstname    ${firstname}
    Input Text    name=lastname     ${lastname}
    Input Text    name=email        ${email}
    Input Text    name=telephone    ${telephone}
    Input Text    name=password     ${password}
    Input Text    name=confirm      ${confirm}
    Click Element    xpath=//input[@name='agree']
    Click Button    xpath=//input[@value='Continue']
    Sleep    3s
    Capture Page Screenshot    register_result.png
    Close Browser