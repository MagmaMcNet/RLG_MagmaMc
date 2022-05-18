:check_Permissions
net session >nul 2>&1
if %errorLevel% == 0 (
    echo ^[32mAdministrator detected, continuing batch file.[0m
    goto try
) else (
    echo ^[31mError: Administrator permissions required. Please restart the batch with Admin.[0m
	pause
    exit /b
)
:try
py -m pip install --upgrade pip
pip install requests --force