*** Settings ***

Library    Process
# import selenium library
Library    SeleniumLibrary

*** Test Cases ***
Check Python Installation
    ${result}    Run Process    python3     --version
    Log    output:${result.stdout}
    Log To Console    OUTPUT:${result.stdout}
    Should Be Equal As Integers    ${result.rc}    0    msg=Python command failed to execute
    Should Contain    ${result.stdout}    Python 3

Check Robot Framework Installation ANd Print Its Version
    ${result}    Run Process    robot    --version
    Log    output:${result.stdout}
    Log To Console    OUTPUT:${result.stdout}
    Should Be Equal As Integers    ${result.rc}    251    msg=Robot command failed to execute
    Should Contain     ${result.stdout}    Robot Framework