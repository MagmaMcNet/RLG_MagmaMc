git add .
git commit -m "1.1.6" -a 
git push -u origin master
gh release create v1.1.6 --generate-notes 'dist/Build_Windows.zip' -p