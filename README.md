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

## Research & ML

During the project a lot of effort has been invested in the data preprocessing. Each dataset that we worked with have
been described by a Dataset Card. It was crucial for the project because it was the first time we have been working with
Point Clouds and `.las` file format.

At the beginning we researched the PointNet and PointNet++ architectures because they are neural networks dedicated for
Point Clouds. During the research we decided to begin with more baseline models. Finally we ended up with using tee
models like **Random Forest** or **Extra Trees Classifier**. The Point Net architecture is planned to be implemented in
the near future.

For experiment tracking we used Weights and Biases, which helped us tremendously with finding the best hyperparameters
for our models. Latter we used also Optuna.

## Data

### Data types and description

| Exact Name        | Data Type | Description                                                  |
|-------------------|-----------|--------------------------------------------------------------|
| X                 | float64     | Positional value                                             |
| Y                 | float64     | Positional value                                             |
| Z                 | float64     | Positional value                                             |
| intensity         | uint16    | The return strength of the laser pulse that generated the lidar point |
| return_number     | int32     | An emitted laser pulse can have multiple returns. This marks the order of the return |
| number_of_returns | int32     | Total number of returns for a given pulse                    |
| scan_direction_flag | int32     | Direction the laser scanning mirror was traveling at the time of the laser pulse |
| edge_of_flight_line | uint8     | Points at the edge of the flight line are given a value of 1; all others are 0 |
| classification   | int32     | Numeric integer codes defining the type of object that reflected the laser pulse |
| synthetic        | int32     | Points created by methods other than lidar collection        |
| key_point        | int32     | A point considered to be a model key-point                   |
| withheld         | int32     | Points that should not be included in processing             |
| scan_angle_rank  | int8      | Value in degrees between -90 and +90 indicating the laser pulse's direction relative to the aircraft |
| user_data        | uint8     | N/A                                                          |
| point_source_id  | uint16    | N/A                                                          |
| red              | uint16    | Red band value for lidar data attributed with RGB bands      |
| green            | uint16    | Green band value for lidar data attributed with RGB bands    |
| blue             | uint16    | Blue band value for lidar data attributed with RGB bands     |

**If you want to see detailed description of las files go [here](detailed_las_data_information.md)**

### Classified data:

### USER AREA.las
USER AREA.las is a fragment of Słoneczna street (hole roads leading to wmii).

**Point count**: 6,375,629

| Attribute             | Unique Values | Min Value  | Max Value   | Mean Value   | Median Value | Std Value    |
|-----------------------|---------------|------------|-------------|--------------|--------------|--------------|
| X                     | 56632         | -1690300   | 699         | -869617.32   | -855190.0    | 415378.86    |
| Y                     | 22782         | -947100    | 372500      | -250536.68   | -237199.0    | 275937.13    |
| Z                     | 11788         | -35199     | 2076400     | 37069.63     | 17610.0      | 51632.39     |
| intensity             | 2090          | 10         | 37003       | 11735.05     | 12812.0      | 4176.02      |
| return_number         | 3             | 1          | 3           | 1.35         | 1.0          | 0.72         |
| number_of_returns     | 2             | 1          | 3           | 1.71         | 1.0          | 0.96         |
| scan_direction_flag   | 1             | 0          | 0           | 0.0          | 0.0          | 0.0          |
| edge_of_flight_line   | 2             | 0          | 1           | 0.0          | 0.0          | 0.03         |
| classification        | 8             | 0          | 25          | 12.43        | 11.0         | 2.77         |
| synthetic             | 1             | 0          | 0           | 0.0          | 0.0          | 0.0          |
| key_point             | 1             | 0          | 0           | 0.0          | 0.0          | 0.0          |
| withheld              | 1             | 0          | 0           | 0.0          | 0.0          | 0.0          |
| scan_angle_rank       | 76            | -38        | 37          | -2.33        | -3.0         | 19.72        |
| user_data             | 1             | 0          | 0           | 0.0          | 0.0          | 0.0          |
| point_source_id       | 1             | 0          | 0           | 0.0          | 0.0          | 0.0          |
| red                   | 255           | 0          | 65278       | 24117.83     | 22873.0      | 9991.81      |
| green                 | 255           | 0          | 65278       | 22556.78     | 21588.0      | 8483.26      |
| blue                  | 255           | 0          | 65278       | 10336.84     | 7967.0       | 9300.42      |

### Data features
Point count: 6215173

Return number: 

| Value | Frequency   |
|-------|-------------|
| 1     | 4,922,896   |
| 3     | 893,683     |
| 2     | 398,594     |

Number of returns: 

| Value | Frequency   |
|-------|-------------|
| 1     | 4,001,189   |
| 3     | 2,213,984   |

Edge of flight line:

| Value | Frequency   |
|-------|-------------|
| 0     | 6,208,309   |
| 1     | 6,864       |

Classification:

| Value | Frequency   |
|-------|-------------|
| 11    | 3,418,176   |
| 13    | 2,102,971   |
| 0     | 517         |
| 15    | 193,239     |
| 17    | 277,429     |
| 19    | 12,387      |
| 25    | 177,455     |
| 1     | 32,999      |

### WMII_CLASS.las

WMII.las is a point cloud that represents the faculty of mathematics and computer science at the University of Warmia and Mazury in Olsztyn.

### Data features

**Point count**: 6,375,629

| Feature               | Unique Values | Min Value | Max Value | Mean Value | Median Value | Std Value   |
|-----------------------|---------------|-----------|-----------|------------|--------------|-------------|
| X                     | 29783         | -10399    | 1805300   | 923767.0   | 955100.0     | 384899.73   |
| Y                     | 27647         | -437599   | 1436500   | 481229.23  | 459399.0     | 461857.01   |
| Z                     | 8038          | -153290   | 1689709   | 11679.5    | -18389.0     | 73511.46    |
| Intensity             | 2714          | 10        | 49977     | 12050.97   | 13006.0      | 3842.38     |
| Return Number         | 3             | 1         | 3         | 1.25       | 1.0          | 0.62        |
| Number of Returns     | 2             | 1         | 3         | 1.52       | 1.0          | 0.88        |
| Scan Direction Flag   | 1             | 0         | 0         | 0.0        | 0.0          | 0.0         |
| Edge of Flight Line   | 2             | 0         | 1         | 0.0        | 0.0          | 0.03        |
| Classification        | 8             | 0         | 25        | 16.5       | 15.0         | 5.8         |
| Synthetic             | 1             | 0         | 0         | 0.0        | 0.0          | 0.0         |
| Key Point             | 1             | 0         | 0         | 0.0        | 0.0          | 0.0         |
| Withheld              | 1             | 0         | 0         | 0.0        | 0.0          | 0.0         |
| Scan Angle Rank       | 76            | -38       | 37        | -8.99      | -15.0        | 21.89       |
| User Data             | 1             | 0         | 0         | 0.0        | 0.0          | 0.0         |
| Point Source ID       | 1             | 0         | 0         | 0.0        | 0.0          | 0.0         |
| Red                   | 255           | 0         | 65278     | 30586.61   | 29041.0      | 12719.36    |
| Green                 | 255           | 0         | 65278     | 28387.99   | 26728.0      | 11927.79    |
| Blue                  | 255           | 0         | 65278     | 19756.12   | 17476.0      | 13781.5     |

### Number of individual values
Return Number:

| Value | Frequency   |
|-------|-------------|
| 1     | 5384103     |
| 3     | 628143      |
| 2     | 363383      |


Number of returns:

| Value | Frequency   |
|-------|-------------|
| 1     | 4721515     |
| 3     | 1654114     |

Edge of Flight Line:

| Value | Frequency   |
|-------|-------------|
| 0     | 6368465     |
| 1     | 7164        |

Classification:

| Value | Frequency |
|-------|-----------|
| 11    | 1452334   |
| 13    | 1581882   |
| 25    | 1884562   |
| 0     | 4521      |
| 1     | 46760     |
| 15    | 1199369   |
| 17    | 205686    |
| 19    | 515       |

### Unclassified data:

### kortowo.las
kortowo.las represents a fragment of the kortowo district in Olsztyn.

**Point count**: 122,973,708

| Attribute            | Num of unique values | Min Value  | Max Value  | Median Value | Std Value   |
|----------------------|---------------|------------|------------|--------------|-------------|
| X                    | 131984        | -3825800   | 5020799    | 303599.0     | 2162246.29  |
| Y                    | 115503        | -9516200   | 1143099    | -5820300.0   | 2816468.48  |
| Z                    | 61367         | -200449    | 2210610    | 43320.0      | 102688.18   |
| intensity            | 3784          | 10         | 51777      | 12344.0      | 4293.94     |
| return_number        | 3             | 1          | 3          | 1.0          | 0.76        |
| number_of_returns    | 2             | 1          | 3          | 1.0          | 0.99        |
| scan_direction_flag  | 1             | 0          | 0          | 0.0          | 0.0         |
| edge_of_flight_line  | 2             | 0          | 1          | 0.0          | 0.03        |
| classification       | 1             | 1          | 1          | 1.0          | 0.0         |
| synthetic            | 1             | 0          | 0          | 0.0          | 0.0         |
| key_point            | 1             | 0          | 0          | 0.0          | 0.0         |
| withheld             | 1             | 0          | 0          | 0.0          | 0.0         |
| scan_angle_rank      | 76            | -38        | 37         | -5.0         | 17.97       |
| user_data            | 1             | 0          | 0          | 0.0          | 0.0         |
| point_source_id      | 1             | 0          | 0          | 0.0          | 0.0         |
| red                  | 255           | 0          | 65278      | 23387.0      | 11288.85    |
| green                | 255           | 0          | 65278      | 21845.0      | 10113.28    |
| blue                 | 255           | 0          | 65278      | 8481.0       | 11418.01    |

|   | number_of_returns count   |
|------------|-----------|
| Ones    | 71,287,100 |
| Twos     | 51,686,608 |

|   | edge_of_flight_line count   |
|------------|----------|
| Ones    | 99,848    |
| Twos       | 122,873,860|

|   | return_number_count    |
|------------|-----------|
| Ones    | 91,552,970 |
| Twos     | 11,314,728   |
| Threes     | 20,106,010   |



### Used stack

- ML: Sklearn, Pandas, Laspy
- Experiment Tracking: Weights and Biases, Optuna
- Version Control: Git & GitHub
- Organization: Scrum

### License

This project is licensed under the [License Name](link).

### Neptun's Eye Team

- [Nikodem Przybyszewski](https://github.com/nexter0)
- [Michał Sztymelski](https://github.com/Stimm147)
- [Kacper Gutowski](https://github.com/Perunio)
- [Alan Ferenc](https://github.com/Zeusthegoddd)
- [Jan Karaś](https://github.com/KTFish)

