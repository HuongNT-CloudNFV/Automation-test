*** Settings ***
Library                SSHLibrary

*** Keywords ***
test-case1    
   [Arguments]    ${HOST}   ${USERNAME}    ${PASSWORD}
   Sleep           60
   Open Connection    ${HOST}
   Login    ${USERNAME}    ${PASSWORD}
   Write    cd /home/ubuntu/robot-test
   Write    echo `date` >> log.txt
   Sleep           10   