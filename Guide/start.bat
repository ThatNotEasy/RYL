@echo off

:: Start login process
login.exe

:: Terminate any running instance of Apache
nPro\home\admin\program\pskill.exe Apache.exe

:: Check if Apache was successfully stopped
IF NOT ERRORLEVEL 1 goto started

:: Get the disk letter from the argument or default to 'w'
set Disk=%1
IF "%Disk%"=="" set Disk=w

:: Create a virtual disk drive mapping to "nPro"
subst %Disk%: "nPro"
IF ERRORLEVEL 1 goto hint

:: Define paths for Apache and program executables
set apachepath=\usr\local\apache2\
set apacheit=%Disk%:%apachepath%bin\Apache.exe -f %apachepath%conf\httpd.conf -d %apachepath%.
set programit=%Disk%:\home\admin\program\
set closeit=%programit%close.bat %Disk%

:: Change to the PHP directory
%Disk%:
cd \usr\local\php

:: Clear the screen
CLS

:: Display status message
echo The server is working on the disk %Disk%: [http://127.0.0.1/a/]

:: Start the server
start %programit%miniserv.exe "%apacheit%" "%closeit%"

:: End of script
goto end

:hint
:: Clear the screen and show disk busy message
CLS
echo The disk %Disk% is busy. Use start.bat [disk letter]
goto pause

:started
:: Clear the screen and show error message
CLS
echo ERROR!!! 

:end
:: End of script
pause
