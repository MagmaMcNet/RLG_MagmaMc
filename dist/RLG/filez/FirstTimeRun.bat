@ECHO OFF
set PORT=8081
set RULE_NAME="Filez_Port %PORT%"

:::check_Permissions
::net session >nul 2>&1
::if %errorLevel% == 0 (
::    echo ^[32mAdministrator detected, continuing batch file.[0m
::    goto try
::) else (
::    echo ^[31mError: Administrator permissions required. Please restart the batch with Admin.[0m
::	pause
::    exit /b
::)

:try
::netsh advfirewall firewall show rule name=%RULE_NAME% >nul
::if not ERRORLEVEL 1 (
::    rem Rule %RULE_NAME% already exists.
::    echo Port Already Created
::) else (
::    echo Rule %RULE_NAME% does not exist. Creating...
::    netsh advfirewall firewall add rule name=%RULE_NAME% dir=in action=allow protocol=TCP localport=%PORT%
::)
cd PortForward
py Forward.py
type LES.txt
