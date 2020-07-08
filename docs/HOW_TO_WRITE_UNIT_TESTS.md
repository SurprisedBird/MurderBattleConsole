## Unit tests implementation
1. Create new folder "tests" if the folder has not created
2. Create \_\_init\_\_.py file in the "tests" folder
3. Create subfolders: "unit", "integration", "system" for each types of unit tests
4. Create \_\_init\_\_.py file in each subfolder
5. Create new test file with name finished by "_test.py" (e.g. user_interaction_test.py) in necessary subfolder
6. Add import: `from unittest import TestCase`
7. Create class extended from TestCase
8. Define method started by "test_" (e.g. def test_show_global_instant(self))
9. Write the test
10. If all steps are performed correctly, then you can see the new bulb icon at the left side VSCode menu
11. You can click on bulb icon and run necessary tests by green run icons