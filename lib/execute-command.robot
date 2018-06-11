*** Settings ***
Library                SSHLibrary

*** Variables ***
${HOST}                10.15.7.175
${USERNAME}            ubuntu
${PASSWORD}            123

*** Keyword ***
execute command
   Open Connection    ${HOST}
   Login    ${USERNAME}    ${PASSWORD}
   Write    cd /home/ubuntu
   Write    echo `date` >> log.txt
