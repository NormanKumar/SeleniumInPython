*** Settings ***
Library     SeleniumLibrary

*** Variables ***
${url}     https://opensource-demo.orangehrmlive.com/web/index.php/auth/login
${browser}    chrome

*** Keywords ***
Open Orangehrm
    Open Browser     ${url}    chrome
    Maximize Browser Window
    Sleep     5s

OrangeHRM Login
    [Arguments]    ${username}    ${password}
    Input Text    name=username    ${username}
    Input Text    name=password    ${password}
    Capture Page Screenshot    before.png
    Click Button    xpath=//*[@id="app"]/div[1]/div/div[1]/div/div[2]/div[2]/form/div[3]/button
    Capture Page Screenshot     after.png
    Close Browser

*** Test Cases ***
Login pass Test
    Open Orangehrm
    OrangeHRM Login    Admin    admin123
Login fail test
    Open Orangehrm
    OrangeHRM Login    Admin    admin