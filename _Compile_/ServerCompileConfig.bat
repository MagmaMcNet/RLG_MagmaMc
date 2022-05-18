cd ../
pyinstaller --noconfirm --onedir --console --icon "M:/pgzero/favicon.ico" --name "Server" --splash "C:/Users/kaicy/Desktop/logo.png" --add-data "C:/Users/kaicy/Documents/website_python/MagmaMc_RLG_test/images;images/" --add-data "C:/Users/kaicy/Documents/website_python/MagmaMc_RLG_test/files;files/" --add-data "C:/Users/kaicy/Documents/website_python/MagmaMc_RLG_test/pgzero;pgzero/" --add-data "C:/Users/kaicy/Documents/website_python/MagmaMc_RLG_test/Modloader.py;." --collect-all "commentjson" --collect-all "lark" --collect-all "pgzero" --add-data "C:/Users/kaicy/Documents/website_python/MagmaMc_RLG_test/filez;filez/"  "C:/Users/kaicy/Documents/website_python/MagmaMc_RLG_test/Server.py"
ren dist/Server Data

