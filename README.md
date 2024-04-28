![logo-400px](./neptunseye/resources/neptuns-eye-logo.ico)

# Neptun's Eye

Neptun's Eye is a ML-powered Point Cloud segmentation tool. The project have been realised by students
from [Czarna Magia Student Artificial Intelligence Society](https://github.com/knsiczarnamagia) and students from UWM
with mentorship from [Visimind](https://visimind.com/pl/).

[//]: # (Projekt realizowany w ramach przedmiotu Projekt Zespołowy na Uniwersytecie Warmińsko-Mazurskim w Olsztynie we współpracy)

[//]: # (z firmą Visimind.)

[//]: # ()

[//]: # (### Cel projektu)

[//]: # ()

[//]: # (Celem projektu jest stworzenie skryptu, aplikacji lub programu wykrywającego obiekty na chmurze punktów z wykorzystaniem)

[//]: # (elementów sztucznej inteligencji.)

[//]: # ()

[//]: # (<hr>)

[//]: # (Project realised as a part of a Team Project subject at University of Warmia and Mazury in Olsztyn in collaboration with the Visimind company.)

[//]: # ()

[//]: # ()

[//]: # (The aim of the project is to make a script, an app or a program detecting objects in a point cloud using elements of)

[//]: # (artificial intelligence.)

## Installation and running

### Run with `poetry`

- Install `pipx`.
- Install poetry using `pipx` (do not use brew).
- Install `pyenv`. Check if it is installed correctly by running `pyenv --vesion`.
- Create virtual environment using `pyenv` with python 3.11.
- Install `poetry`. Check if it is installed correctly by running `poetry --vesion`.
- Install dependencies using `poetry`.

### Installation Details

Create virtual environment:

```commandline
poetry env use $(pyenv which python)
```

You should see something like this:

```commandline
Using virtualenv: C:\Users\Admin\AppData\Local\pypoetry\Cache\virtualenvs\neptuns-eye-z6EeDWoH-py3.11
```

This command is used for installing dependencies from `requirements.txt` using `poetry`. You will probably not use it
and directly install dependencies from `pyproject.toml` file. This is left here only for reference.

```commandline
poetry add $(cat requirements.txt)
```

### Run

```commandline
make run
```

### Test

```commandline
make test
```

### Reference materials

- [Pyenv](https://realpython.com/intro-to-pyenv/#why-use-pyenv)
- [How install Pyenv?](https://k0nze.dev/posts/install-pyenv-venv-vscode/)
- [Pyenv for windows](https://github.com/pyenv-win/pyenv-win)
- [Poetry](https://realpython.com/dependency-management-python-poetry/#add-poetry-to-an-existing-project)

### Install `make` on Windows

1. Install [chocolatey](https://chocolatey.org/install)
2. Install make using choco.

```powershell
choco install make
```

[//]: # (*[Ogólna lista funkcji.]*)

[//]: # ()

[//]: # (- Function 1)

[//]: # (- Function 2)

[//]: # (- ...)

[//]: # ()

[//]: # (<hr>)

[//]: # ()

[//]: # (- Function 1)

[//]: # (- Function 2)

[//]: # (- ...)

## Usage

*[Przykłady zastosowania projektu.]*

## Used stack

*[Lista, czego użyliśmy do stworzenia projektu.]*

### IDEs & Programs:

- PyCharm
- ...

### Libraries:

- laspy
- ...

### Others:

- Github
- Docker
- ...

## License

This project is licensed under the [License Name](link).

## Screenshots

*[Screenshots / Demos.]*

## Links & Credits

- [Documentation](...)


