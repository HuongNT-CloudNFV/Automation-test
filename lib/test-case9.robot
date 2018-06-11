*** Settings ***
Library                SSHLibrary

*** Variables ***
${HOST}                10.15.7.175
${USERNAME}            ubuntu
${PASSWORD}            123

*** Keywords ***
test case9
   Open Connection    ${HOST}
   Login    ${USERNAME}    ${PASSWORD}
   Write    cd /home/ubuntu/robot-test
   Write    echo `date` >> log.txt