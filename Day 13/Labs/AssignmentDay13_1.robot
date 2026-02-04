*** Settings ***
Suite Setup       Suite Level Setup
Suite Teardown    Suite Level Teardown
Test Setup        Test Level Setup
Test Teardown     Test Level Teardown
Library           OperatingSystem

*** Variables ***
${MESSAGE}    Hello from Robot Framework

*** Keywords ***
Suite Level Setup
    Log    Running Suite Setup

Suite Level Teardown
    Log    Running Suite Teardown

Test Level Setup
    Log    Running Test Setup

Test Level Teardown
    Log    Running Test Teardown

*** Test Cases ***
Sample Tagged Test
    [Tags]    smoke    cli
    Log    ${MESSAGE}

Another Test Without Tag
    Log    This test has no tag
