*** Settings ***
Library                SSHLibrary
*** Variables ***
${HOST}                10.15.99.219
${USERNAME}            ubuntu
${PASSWORD}            ssdc123!

*** Keywords ***
remote server
   Open Connection    ${HOST}
   Login    ${USERNAME}    ${PASSWORD}
   Write    cd /home/ubuntu/robot-test
   Write    echo `date` >> log.txt