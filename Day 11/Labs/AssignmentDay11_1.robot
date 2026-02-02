*** Settings ***
Library    SeleniumLibrary
*** Variables ***

${Message}    This is my first robot assignment
@{numbers}    1 2 3 4 5

*** Test Cases ***
Use scalar variable and logging
    Log     message=This message will be logged into log.html file
    Log To Console     message=Printing to console: ${Message}
    Should End With     ${Message}    str2=assignment

Use list variables
    Should Contain    ${numbers}    4