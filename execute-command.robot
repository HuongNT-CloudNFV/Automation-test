*** Settings ***
Library                SSHLibrary

*** Variables ***
${HOST}                10.15.99.219
${USERNAME}            ubuntu
${PASSWORD}            ssdc123!

*** Test Cases ***
Execute Commands
   Open Connection And execute command
   Execute command

*** Keywords ***
Open Connection And execute command
   Open Connection    ${HOST}
   Login    ${USERNAME}    ${PASSWORD}
Execute command
    Write    cd /home/ubuntu/robot-test
    Write    echo `date` >> log.txt
