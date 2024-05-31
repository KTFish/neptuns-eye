![logo-400px](./neptunseye/resources/neptuns-eye-logo.ico)

# Neptun's Eye

Neptun's Eye is a ML-powered Point Cloud segmentation tool. The project have been realised by students
from [Czarna Magia Student Artificial Intelligence Society](https://github.com/knsiczarnamagia) and students from UWM
with mentorship from [Visimind](https://visimind.com/pl/).

## Usage

*[Przykłady zastosowania projektu.]*

## Run locally

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

#### Run

```commandline
make run
```

#### Test

```commandline
make test
```

#### Reference materials

- [Pyenv](https://realpython.com/intro-to-pyenv/#why-use-pyenv)
- [How install Pyenv?](https://k0nze.dev/posts/install-pyenv-venv-vscode/)
- [Pyenv for windows](https://github.com/pyenv-win/pyenv-win)
- [Poetry](https://realpython.com/dependency-management-python-poetry/#add-poetry-to-an-existing-project)

#### Install `make` on Windows

1. Install [chocolatey](https://chocolatey.org/install)
2. Install make using choco.

```powershell
choco install make
```

### Research & ML

During the project a lot of effort has been invested in the data preprocessing. Each dataset that we worked with have
been described by a Dataset Card. It was crucial for the project because it was the first time we have been working with
Point Clouds and `.las` file format.

At the beginning we researched the PointNet and PointNet++ architectures because they are neural networks dedicated for
Point Clouds. During the research we decided to begin with more baseline models. Finally we ended up with using tee
models like **Random Forest** or **Extra Trees Classifier**. The Point Net architecture is planned to be implemented in
the near future.

For experiment tracking we used Weights and Biases, which helped us tremendously with finding the best hyperparameters
for our models. Latter we used also Optuna.

### Used stack

- ML: Sklearn, Pandas, Laspy
- Experiment Tracking: Weights and Biases, Optuna
- Version Control: Git & GitHub
- Organization: Scrum

### License

This project is licensed under the [License Name](link).

### Neptun's Eye Team

- Nikodem Przybyszewski
- [Michał Sztymelski](https://github.com/Stimm147)
- [Kacper Gutowski](https://github.com/Perunio)
- Alan Ferenc
- [Jan Karaś](https://github.com/KTFish)

