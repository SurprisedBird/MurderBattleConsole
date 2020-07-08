TODO list:

- [Install VSCode](#install-vscode)
- [Install Python extention](#install-python-extention)
- [[OPTIONAL] Install Additional extentions](#optional-install-additional-extentions)
- [Create virtual environment](#create-virtual-environment)
- [Setup Python interpreter](#setup-python-interpreter)
- [Install project dependencies from 'requirements.txt'](#install-project-dependencies-from-requirementstxt)
- [Enable code formatting in VSCode](#enable-code-formatting-in-vscode)
- [Reload VSCode](#reload-vscode)
- [Check VSCode funtionality](#check-vscode-funtionality)
- [Setup unit tests](#setup-unit-tests)

---

## Install VSCode
VSCode [setup guide](https://code.visualstudio.com/docs/setup/setup-overview).

## Install Python extention
Navigate to VSCode Marketplace tab and install Python extention with following name:<br>
`ms-python.python`

## [OPTIONAL] Install Additional extentions
Find and install below extentions from VSCode Marketplace if it is needed:<br>
Extention for work with PlantUML: `jebbs.plantuml`<br>
All-language auticompleter: `TabNine.tabnine-vscode`<br>
Extention for work with Markdown format: `yzhang.markdown-all-in-one`

## Create virtual environment
``` bash
# Navigate to project directory
cd MurderBattleConsole

# Create new virtual environment
python3 -m venv ./venv
```
*These commands will create a new virtual environment inside project directory.*

## Setup Python interpreter
Add to a local `.vscode/settings.json` file following line:<br>
``` json
"python.pythonPath": ".venv/bin/python",
```
*This setting will be applied only to a current project.*

## Install project dependencies from 'requirements.txt'

``` bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip3 install -r requirements.txt
```

## Enable code formatting in VSCode
Add to a local `.vscode/settings.json` file following snippet:<br>
``` json
"python.linting.enabled": true,
"python.linting.pylintPath": "pylint",
"python.formatting.provider": "yapf",
"python.linting.pylintEnabled": true,
"python.formatting.yapfArgs": [
    "--style={based_on_style: pep8, indent_width: 4}"
],
"editor.formatOnSave": true,
"editor.codeActionsOnSave": {
    "source.organizeImports": true
},
``` 

*These settings enable [YAPF](https://github.com/google/yapf#introduction) code formatter.<br>
Also, these settings enables code formatting and import sorting on Save.*

## Reload VSCode

## Check VSCode funtionality

## Setup unit tests
Add to a local `.vscode/settings.json` file following snippet:<br>
``` json
"python.testing.unittestArgs": [
    "-v",
    "-s",
    "./tests",
    "-p",
    "*_test.py"
],
"python.testing.pytestEnabled": false,
"python.testing.nosetestsEnabled": false,
"python.testing.unittestEnabled": true
```

*Also you can review:
[how to write and setup unit tests](HOW_TO_WRITE_UNIT_TESTS.md)*