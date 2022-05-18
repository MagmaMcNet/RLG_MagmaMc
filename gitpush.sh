#git remote add origin https://github.com/SMLkaiellis08/RLG_MagmaMc.git
cd _Compile_
start ClientCompileConfig.bat
start ServerCompileConfig.bat
start Compile.bat
cd ../
git add .
git commit -m "1.1.2" -a 
git push -u origin master
gh release create v1.1.2 --generate-notes 'dist/Build_Windows.zip# Windows Build'