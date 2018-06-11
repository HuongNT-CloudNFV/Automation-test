*** Settings ***
Library                SSHLibrary

*** Variables ***
${HOST}                10.15.99.219
${USERNAME}            ubuntu
${PASSWORD}            ssdc123!

*** Keywords ***
test case9
   Open Connection    ${HOST}
   Login    ${USERNAME}    ${PASSWORD}
   Write    cd /home/ubuntu/robot-test
   Write    echo `date` >> log.txt