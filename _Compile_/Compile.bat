cd ../
del dist\*.zip /Q
timeout /t 1 >nul
"C:\Program Files\7-Zip\7z.exe" a "dist/Build_Windows.zip" "dist/"
timeout /t 2
