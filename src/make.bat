pyinstaller medit.py --onefile --windowed --icon=icon.ico --clean	--name "medit" --version-file version.txt
cd dist
md ui
cd ui
md icon
cd..
cd..
cd ui
copy *.ui ..\dist\ui
copy *.png ..\dist\ui
cd icon
copy new.png ..\..\dist\ui\icon
copy open.png ..\..\dist\ui\icon
copy save.png ..\..\dist\ui\icon
copy run.png ..\..\dist\ui\icon
copy text_case.png ..\..\dist\ui\icon
copy undo.png ..\..\dist\ui\icon
cd..
cd..
copy tamplate_guide.md dist
copy tamplate_readme.md dist
copy tamplate_style.md dist
