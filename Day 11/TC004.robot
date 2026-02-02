*** Settings ***
Library     SeleniumLibrary

*** Variables ***
${url}          https://opensource-demo.orangehrmlive.com/web/index.php/auth/login
${Browser}      chrome
${Username}     Admin
${Password}     admin123

*** Test Cases ***
Login Authentication
    Open Browser    ${url}    ${Browser}
    Sleep    5s
    Input Text      name=username   ${Username}
    Input Text      name=password    ${Password}
    Capture Page Screenshot     filename=before.png
    Click Button    xpath=//*[@id="app"]/div[1]/div/div[1]/div/div[2]/div[2]/form/div[3]/button
    Capture Page Screenshot     filename=after.png
    Close Browser