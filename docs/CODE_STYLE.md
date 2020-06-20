Contents
- [Project code style](#project-code-style)
- [Additional rules](#additional-rules)
  - [Docs file names](#docs-file-names)
  - [Type hints](#type-hints)
  - [Protected and private class members](#protected-and-private-class-members)
  - [Import order](#import-order)
  - [Commit messages](#commit-messages)
- [Recomendation](#recomendation)


# Project code style

Standard "[PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)" should be used as a code style.

The most important (must read) parts of this convention are:
- [Comments](https://www.python.org/dev/peps/pep-0008/#comments)
- [Naming Conventions](https://www.python.org/dev/peps/pep-0008/#naming-conventions)

Also, there will be useful to read [docstring conventions](https://www.python.org/dev/peps/pep-0257/)

There are some additional rules that should be applied to the project.


# Additional rules

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
