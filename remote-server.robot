*** Settings ***
Library                SSHLibrary
*** Variables ***
${HOST}                10.15.99.219
${USERNAME}            ubuntu
${PASSWORD}            ssdc123!
*** Test Cases ***
Remote server
   Open Connection And Log In
   Remote and execute command
*** Keywords ***
Open Connection And Log In
   Open Connection    ${HOST}
   Login    ${USERNAME}    ${PASSWORD}
Remote and execute command
    Write    cd /home/ubuntu/robot-test
    Write    echo `date` >> log.txt