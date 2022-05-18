git remote add origin https://github.com/SMLkaiellis08/RLG_MagmaMc.git
git add .
git commit -m "1.1.1" -a 
git push -u origin master
gh release create v1.1.1 --generate-notes 'dist/Build_Windows.zip# Windows Build'