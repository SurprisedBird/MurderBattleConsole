Contents
- [Project code style](#project-code-style)
  - [Docstring conventions](#docstring-conventions)
- [Additional rules](#additional-rules)
  - [Docs file names](#docs-file-names)
  - [Type hints](#type-hints)
  - [Protected and private class members](#protected-and-private-class-members)
  - [Import order](#import-order)
  - [Commit messages](#commit-messages)
- [Recomendation](#recomendation)


# Project code style

[PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/) should be used as a project code style.  

Significant portion of these conventions could be covered by [pep8 code formatting tools](ENVIRONMENT_SETUP.md#code-formatting-on-save) .

But several parts of code style should be tracked manually by developers. Such as:
- [Maximum Line Length](https://www.python.org/dev/peps/pep-0008/#maximum-line-length)
- [Comments](https://www.python.org/dev/peps/pep-0008/#comments)
- [Naming Conventions](https://www.python.org/dev/peps/pep-0008/#naming-conventions)

## Docstring conventions

[Docstring conventions](https://www.python.org/dev/peps/pep-0257/) should be used for docstrings.

Except - docstrings for packages, modules, and class constructors are not necessary.



# Additional rules

There are some additional rules that should be applied to the project.

## Docs file names

Every file in `docs/` directory should have an `UPPER_CASE_WITH_UNDERSCORES` names.


``` bash
# Right 

docs/CODE_STYLE.md

```

``` bash
# Wrong

docs/code_style.md

```

## Type hints

## Protected and private class members

## Import order
//use auto import sort 
//but always make a blank line between standard modules,
external libraries and local imports


## Commit messages
Following convention should be used for all commits:<br>
[Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)

# Recomendation

It's strongly recommended to enable appropriate code formatting (and automatic imports sort) on save in your IDE.
It will be much easier to follow code style rules.



[a relative link](ENVIRONMENT_SETUP.md)


//все неиспользуемые извне поля помечаются как приватные
//для те, что используются - создаются геттеры и сеттеры
//примечание: если мы используем эти поля в другом объетке того же типа - они все еще считаются
//приватными


//https://google.github.io/styleguide/pyguide.html?showone=Comments#Comments