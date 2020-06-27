Contents
- [Project code style](#project-code-style)
- [Naming Conventions](#naming-conventions)
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
- You should use a single underscore prefix for every protected field or method in class.
  - For every protected field that should be accessed outside of the class - create property without an underscore in its name
  - Don't create property setter for field if it shouldn't be changed outside the class
  - You should refer to protected fields inside this class directly (without using properties). The only exception - if getter or setter property contains some additional logic.
  - Note that if protected field is accessed by another object of the SAME class - it should NOT be treated as "access outside of the class". 
- All class fields should be treated as protected by default
  - An exception of this rule: model classes which doesn't contain any sophisticated logic and created only to store data.
  In this case - internal fields could remain public.  
- All class methods which are not used outside of the class should be treated as protected
- Try to avoid using double underscore prefix for protected/private fields and methods in class.
  - An exception of this rule: fields or methods that should not be inherited by child classes 

Example:
``` python
class ExampleClass:
    def __init__(self) -> None:
        # Protected field have a single underscore prefix
        self._protected_field = SomeType()
        # Try to AVOID such prefix
        self.__private_field = SomeType()
    
    # Protected field is accessed outside the class, so getter property
    # was created. 
    @property
    def protected_field(self) -> SomeType:
        return self._protected_field

    # Setter should NOT be crated if field is not changed ounside this class
    @property.setter
    def protected_field(self, some_value: SomeType) -> None: 
        self._protected_field = some_value

    def some_method(self) -> None:
        # Field inside the class is reffered by it's name directly. 
        # Not by property
        self._protected_field = SomeType()

# This is a model class.
# Getter and setter properties should NOT be used for fields of this class
# sinse it just stores the data.
class ModelClass:
    def __init__(self):
        self.data_field_1 = DataType()
        self.data_field_2 = DataType()
        self.data_field_3 = DataType()

```


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