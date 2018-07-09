*** Settings ***
Library                SSHLibrary

*** Keywords ***
test-case    ${HOST}   ${USERNAME}    ${PASSWORD}
   Open Connection    ${HOST}
   Login    ${USERNAME}    ${PASSWORD}
   Write    cd /home/ubuntu/robot-test
   Write    echo `date` >> log.txt