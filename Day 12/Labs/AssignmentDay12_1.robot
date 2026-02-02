*** Settings ***
Library    SeleniumLibrary

*** Test Cases ***
Open Google
    Open Browser    https://www.google.com    chrome
    Title Should Be    Google
    Capture Page Screenshot    google_homepage.png
    Close Browser