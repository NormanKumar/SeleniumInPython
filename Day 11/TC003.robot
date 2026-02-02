*** Settings ***
Library     SeleniumLibrary

*** Keywords ***
Open application
    Open Browser    https://www.google.com      chrome
    Maximize Browser Window
*** Test Cases ***
Google Search Test
    Open application
    Title Should Be     Google
    Close Browser