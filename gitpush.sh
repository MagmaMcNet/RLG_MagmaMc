git add .
git commit -m "1.2.0" -a 
git push -u origin master
gh release create v1.2.0 --generate-notes 'dist/Build_Windows.zip'