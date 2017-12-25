*** Settings ***
Library                SSHLibrary
Suite Setup            Open Connection And Log In
Suite Teardown         Close All Connections

*** Variables ***
${HOST}                10.15.99.219
${USERNAME}            ubuntu
${PASSWORD}            ssdc123!

*** Test Cases ***
execute command
    Write    cd /home/ubuntu/robot-test
    Write    echo `date` >> log.txt
*** Keywords ***
Open Connection And Log In
   Open Connection    ${HOST}
   Login    ${USERNAME}    ${PASSWORD}
