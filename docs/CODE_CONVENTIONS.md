Contents
- [Project code style](#project-code-style)
- [Naming Conventions](#naming-conventions)
- [Quotes](#quotes)
- [Comments](#comments)
- [Docstring conventions](#docstring-conventions)
- [Commit messages](#commit-messages)
- [Type hints](#type-hints)
- [Recomendations](#recomendations)


## Project code style

[PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/) should be used as a project code style.

Mostly, these conventions are maintained automatically by [YAPF](https://github.com/google/yapf#introduction) code formatter.<br>
Setup instruction could be found here: [pep8 code formatting tools](ENVIRONMENT_SETUP.md#enable-code-formatting-in-vscode).

But several conventions should be supported by developers manually.
Info about these conventions could be found below.

## Naming Conventions

You should follow pep8 [Naming Conventions](https://www.python.org/dev/peps/pep-0008/#naming-conventions).

Additional notes:
- Single underscore prefix for every protected field or method in class should be used.
- Utility fields which are used ONLY inside the current class and SHOULD NOT be accessed any way outside of current class - should be treated as protected.
- Fields which are accessed from outside of the current class or COULD BE accessed outside of the current class - should be treated as public.
- All class methods which are not used and SHOULD NOT be used outside the current class - should be treated as protected.
- Try to avoid using double underscore prefix for protected/private fields and methods in class.
  - An exception of this rule: fields or methods that should not be inherited by child classes 

Example:
``` python
class ExampleClass:
    def __init__(self) -> None:
        self.public_field = SomeType()
        # Protected field have a single underscore prefix
        self._utility_protected_field = SomeType()
        # WRONG! Try to AVOID such prefix
        self.__private_field = SomeType()

    # WRONG! If field is accessed from outside 
    # (even through getter and event if it is read-only), 
    # this field should be treated as public - not protected.
    @property
    def utility_protected_field(self) -> 'SomeType':
        return self._utility_protected_field

    # Public method which is used outside the class
    def some_method(self) -> None:
        pass
        
    # Protected method which is used ONLY inside the class    
    def _utility_protected_methos(self) -> None:
        pass  


```

## Quotes
You should use only double quotes "" for each string in project, except the Type hints.
For type hints should be used single quotes.

## Comments
You should follow pep8 [Comments](https://www.python.org/dev/peps/pep-0008/#comments) conventions.

## Docstring conventions
You should follow [Docstring conventions](https://www.python.org/dev/peps/pep-0257/).

## Commit messages
You should follow: [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
for every commit message.

## Type hints
You should use [Type hints](https://docs.python.org/3/library/typing.html) in code.

Additional notes:
- For every method should be defined it return type
- If method returns nothing - return type should be specified as `None`
  - This statement is true for every method, including method `__init__()`   
- Type should be specified for every method parameter
- Type hints should NOT be used for variables in code
  - An exception of this rule: type hints should be specified for **class fields** which type is not obvious during initialization (example: different containers)
- In case if method can return objects with different type - `Any` return type should be specified
- To avoid unnecessary imports - several type names could be written inside the quotes

Example:
``` python
class ExampleClass:
    # Method condtructor returns nothing
    def __init__(self) -> None:
        # Field type IS NOT hinted because it is obvious from initialization
        self._field_1 = SomeType1()
        # Field type IS NOT hinted because it could be easily
        # inspected by viewing create_field_method specification
        self._field_2 = create_field_method()
        # Field type IS hinted because it is no way to
        # understand which elements should contain this list - during initialization
        self._field_3: List[SomeType3] = []
    
    # All method arguments marked with type hints
    # Argument2Type is written inside quotes to avoid unnecessary import of Argument2Type in current module
    def some_method_1(self, argument_1: Argument1Type, argument_2: 'Argument2Type') -> ReturnValueType:
        # Local variable type should not be hinted
        local_variable = LocalVariable() 

        # Method return value type is specified as ReturnValueType
        # which is type of returnValue object
        return returnValue
    
    def some_method_2(self) -> Any:
        # Objects returnValue1 and returnValue2 have different types
        if some_condition:
            return returnValue1
        else
            return returnValue2

```

## Recomendations
It is much easier to write clean and consistent code with code formatting tools.
Please, use [this instruction](ENVIRONMENT_SETUP.md#enable-code-formatting-in-vscode) to set up it properly.