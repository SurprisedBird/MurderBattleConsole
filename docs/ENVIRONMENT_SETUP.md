## TODO list:

1. Install VSCode
2. Install Python extention
3. Install other useful extentions: 
   1. PlantUML extention
   2. TabNine extention  
   3. Markdown All in One extention
4. Reload VSCode
5. Create virtual environment inside the project using python venv or any other tool 
6. Setup Python interpreter from venv as VSCode intepreter for current project
7. Install all dependencies from requirements.txt file
8. Install pep8 code formatter tools
9. Enable code formatting on save in VSCode preferences
10. Enable sort Python imports automatically on save

---

## Python VSCode extention
`ms-python.python`

## Useful VSCode extentions
`jebbs.plantuml`<br>
`TabNine.tabnine-vscode`<br>
`yzhang.markdown-all-in-one`

## Virtual environment creation
Navigate to project directory and use commands:<br>
``` bash
cd MurderBattleConsole
python3 -m venv ./venv
```

## Dependencies installation
Use command:<br>
``` bash
pip3 install -r requirements.txt
```

## Code formatting on save
Enable this settings on UI preferences<br>
OR<br>
Add to a global VSCode "settings.json" file following line:<br>
``` json
"editor.formatOnSave": true
```

## Enable sort imports on save
Add to a global VSCode "settings.json" file following snippet:
``` json
"[python]": {
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
``` 