*** Settings ***
Library    BuiltIn

*** Test Cases ***

For loop example
    FOR    ${name}    IN    Ravi    Ram    Teja
        Log To Console    ${name}
    END

For loop with list
    @{fruits}=    Create List    Apple    Mango
    FOR    ${fruit}    IN    @{fruits}
        Log To Console    ${fruit}
    END

For loop with range
    FOR    ${i}    IN RANGE    1    6
        Log To Console    ${i}
    END

FOR Loop Enumerate
    FOR    ${index}    ${value}    IN ENUMERATE    a    b    c
        Log    ${index} = ${value}
    END

While loop example
    ${count}=    Set Variable    1
    WHILE    ${count} <= 5
        Log To Console    ${count}
        ${count}=    Evaluate    ${count} + 1
    END

If condition example
    ${temperature}=    Set Variable    90
    IF    ${temperature} > 95
        Log To Console    Heat
    END

If - Else example
    ${age}=    Set Variable    19
    IF    ${age} > 18
        Log To Console    Major
    ELSE
        Log To Console    Minor
    END

If - Else If - Else Example
    ${wheels}=    Set Variable    2
    IF    ${wheels} == 2
        Log To Console    Bike/Cycle
    ELSE IF    ${wheels} == 3
        Log To Console    Auto
    ELSE
        Log To Console    Car
    END

Inline-if Example
    ${Signal}=    Set Variable    Green
    IF    '${Signal}' == 'Green'    Log To Console    GO

BREAK Example
    FOR    ${i}    IN RANGE    1    10
        IF    ${i} == 5
            BREAK
        END
        Log    ${i}
    END

CONTINUE Example
    FOR    ${i}    IN RANGE    1    6
        IF    ${i} == 3
            CONTINUE
        END
        Log    ${i}
    END

Try Except Example
    TRY
        Fail    Something went wrong
    EXCEPT
        Log    Error handled
    FINALLY
        Log    Always executed
    END

Run Keyword If Example
    ${status}=    Set Variable    PASS
    Run Keyword If    '${status}' == 'PASS'    Log    Test Passed

Run Keyword Unless Example
    ${status}=    Set Variable    FAIL
    Run Keyword Unless    '${status}' == 'PASS'    Log    Test Failed