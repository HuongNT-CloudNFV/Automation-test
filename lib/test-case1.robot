*** Settings ***
Library                SSHLibrary

*** Keywords ***
test-case1    
   [Arguments]    ${HOST}   ${USERNAME}    ${PASSWORD}
   Open Connection    ${HOST}
   Login    ${USERNAME}    ${PASSWORD}
   Write    cd /home/ubuntu/robot-test
   Write    echo `date` >> log.txt