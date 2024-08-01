@echo off

:: Terminate any running instance of Apache
nPro\home\admin\program\pskill.exe Apache.exe c

:: Get the disk letter from the argument or default to 'w'
IF "%Disk%"=="" set Disk=w

:: Remove the virtual disk drive mapping
subst "%Disk%": /D
