
del /Q "dist\RLG\*"
del /Q "dist\Server\*"
del /Q "dist\Data\*"

FOR /D %%p IN ("dist\Server\*.*") DO rmdir "%%p" /s /q
FOR /D %%p IN ("dist\Data\*.*") DO rmdir "%%p" /s /q
FOR /D %%p IN ("dist\RLG\*.*") DO rmdir "%%p" /s /q
rmdir /Q "dist\Data"
rmdir /Q "dist\Server"
rmdir /Q "dist\RLG"

pyinstaller --noconfirm --onedir --windowed --icon "M:/pgzero/favicon.ico" --name "RLG" --splash "C:/Users/kaicy/Desktop/logo.png" --add-data "C:/Users/kaicy/Documents/website_python/MagmaMc_RLG_test/images;images/" --add-data "C:/Users/kaicy/Documents/website_python/MagmaMc_RLG_test/files;files/" --add-data "C:/Users/kaicy/Documents/website_python/MagmaMc_RLG_test/pgzero;pgzero/" --collect-all "commentjson" --collect-all "lark" --collect-all "pgzero" --add-data "C:/Users/kaicy/Documents/website_python/MagmaMc_RLG_test/filez;filez/" --add-data "C:/Users/kaicy/Documents/website_python/MagmaMc_RLG_test/sounds;sounds/"  "C:/Users/kaicy/Documents/website_python/MagmaMc_RLG_test/main.py"
pyinstaller --noconfirm --onedir --console --icon "M:/pgzero/favicon.ico" --name "Server" --splash "C:/Users/kaicy/Desktop/logo.png" --add-data "C:/Users/kaicy/Documents/website_python/MagmaMc_RLG_test/images;images/" --add-data "C:/Users/kaicy/Documents/website_python/MagmaMc_RLG_test/files;files/" --add-data "C:/Users/kaicy/Documents/website_python/MagmaMc_RLG_test/pgzero;pgzero/" --add-data "C:/Users/kaicy/Documents/website_python/MagmaMc_RLG_test/Modloader.py;." --collect-all "commentjson" --collect-all "lark" --collect-all "pgzero" --add-data "C:/Users/kaicy/Documents/website_python/MagmaMc_RLG_test/filez;filez/"  "C:/Users/kaicy/Documents/website_python/MagmaMc_RLG_test/Server.py"

del dist\*.zip /Q

"C:\Program Files\7-Zip\7z.exe" a "dist/Build_Windows.zip" "dist/"

del /Q "dist\RLG\*"
del /Q "dist\Server\*"
del /Q "dist\Data\*"

FOR /D %%p IN ("dist\Server\*.*") DO rmdir "%%p" /s /q
FOR /D %%p IN ("dist\Data\*.*") DO rmdir "%%p" /s /q
FOR /D %%p IN ("dist\RLG\*.*") DO rmdir "%%p" /s /q
rmdir /Q "dist\Data"
rmdir /Q "dist\Server"
rmdir /Q "dist\RLG"