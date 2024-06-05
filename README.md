![logo-400px](./neptunseye/resources/neptuns-eye-logo.ico)

# Neptun's Eye

Neptun's Eye is a ML-powered Point Cloud segmentation tool. The project have been realised by students
from [Czarna Magia Student Artificial Intelligence Society](https://github.com/knsiczarnamagia) and students from UWM
with mentorship from [Visimind](https://visimind.com/pl/).

# Latest build
Neptun's eye v0.1.2
Download [**here**](https://github.com)
### Requirements
- Windows 10 or newer OS
- [**Optional**] Python 3.7.9 for `pptk` support
> [!NOTE]
> The app requires OpenGL 3.3 or newer and might not work correctly on virtual machines or old computers.
<!-- TUTAJ WSTAWIĆ LINK DO POBRANIA BUILDA !-->

# Installation
We packed our app into easy to run executable. You can download and run it right away or dowload some additional tools for more functionalities.
## Ready-to-run build
- Download latest build above.
- Extract the files into a single folder in any location you want.
- Find and run `main.exe` file in the `dist` folder.

That's it! You're good to go!
> [!IMPORTANT]
> Verify if there are models you are using inside `dist\main\_internal\resources\models` folder.

## More options
### Visualisation with pptk
Our app uses a fast an efficient point cloud visualisation tool in Python called `pptk`.
This tool requires you to install Python 3.7.9 on your computer and download `pandas` and `pptk` for this version using any package-management system.
- You can download Python 3.7.9 from the official website [here](https://www.python.org/downloads/release/python-379/)
> [!IMPORTANT]
> After you install python you must change the Python 3.7.9 path in the app settings. See how to do that below.
<!-- TUTAJ BĘDZIE ZWIJANY AKAPIT, KTÓRY NIE WIEM JAK SIĘ ROBI NA TEMAT INSTALACJI O KTÓREJ MOWA WYŻEJ !-->

<!-- TO CO PONIŻEJ TRZEBA SCHOWAĆ !-->
### Run with Poetry

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

### Data dependencies

#### Corelation matrix of wmii.las with empty columns removed
<img src="images/image1.png" alt="corelation_matrix_wmii" width="750" height="600">

### Searching for the most significant columns 

#### The impact of given columns on the accuracy of the RandomForestClassifier model
*stride for validation dataset = 30, stride for training dataset = 30, n_estimators = 100*

<img src="images/feature_sets.png" alt="feature_sets" width="800" height="500">

| Feature             | Set 1 | Set 2 | Set 3 | Set 4 | Set 5 |
|---------------------|-------|-------|-------|-------|-------|
| X                   | ✓     | ✓     |       |       |       |
| Y                   | ✓     | ✓     |       |       |       |
| Z                   | ✓     | ✓     | ✓     | ✓     | ✓     |
| red                 | ✓     | ✓     | ✓     | ✓     | ✓     |
| green               | ✓     | ✓     | ✓     | ✓     | ✓     |
| blue                | ✓     | ✓     | ✓     | ✓     | ✓     |
| intensity           |       | ✓     | ✓     | ✓     |       |
| return_number       |       | ✓     |       | ✓     | ✓     |
| edge_of_flight_line |       | ✓     | ✓     | ✓     |       |
| scan_angle_rank     |       | ✓     |       | ✓     | ✓     |
| number_of_returns   |       |       | ✓     | ✓     | ✓     |

#### the influence of R, G and B columns on the accuracy of the RandomForestClassifier model
*feature_columns = ['Z', 'red', 'green', 'blue', 'intensity','number_of_returns', 'return_number','edge_of_flight_line', 'scan_angle_rank'], training dataset stride = 720, validation dataset stride = 30, n_estimators = 100*

<img src="images/rgb.png" alt="rgb" width="800" height="420">

### Searching for dataset minimization

#### The influence of the stride parameter on the accuracy of the RandomForestClassifier model on the training dataset

Note: Stride means that every stride record will be used, it's basically like a step. Stride = 2 means every other record will be selected.

| Stride       | Validation Accuracy |
|--------------|---------------------|
| No stride    | 0.7037              |
| stride = 2   | 0.7039              |
| stride = 5   | 0.7037              |
| stride = 10  | 0.7038              |
| stride = 30  | 0.7035              |
| stride = 60  | 0.7024              |
| stride = 120 | 0.7015              |

Note: Stride higher than 120 will rarely be used.

#### The influence of the stride parameter on the accuracy of the RandomForestClassifier model on the training and validation dataset

<img src="images/stride.png" alt="stride" width="800" height="700">

### The effect of data scaling on the accuracy of the RandomForestClassifier model
*stride on training dataset = 720, stride on validation dataset = 30, n_estimators = 100*
|                  | Test Accuracy | Validation Accuracy |
|------------------|---------------|---------------------|
| Raw Data         | 0.931131809   | 0.709942897         |
| MinMaxScaler     | 0.930849562   | 0.709571228         |
| Difference       | 0.000282247   | 0.000371669         |

### Impact of normalization of R, G and B columns (divide by 65025) on the accuracy of the RandomForestClassifier model

|                  | Test Accuracy | Validation Accuracy |
|------------------|---------------|---------------------|
| Raw RGB          | 0.931131809   | 0.709942898         |
| Normalized RGB   | 0.859441152   | 0.577975895         |
| Difference       | 0.071690657   | 0.131966998         |

### Comparison of classifiers

| Classifier                      | Test Accuracy | Validation Accuracy | Validation Accuracy from Optuna |
|---------------------------------|---------------|---------------------|---------------------------------|
| AdaBoostClassifier              | 0.8944        | 0.6352              | 0.7681                   |
| BaggingClassifier               | 0.9252        | 0.6893              | 0.7183                          |
| ExtraTreesClassifier            | 0.9303        | **0.7446**          | 0.7655                               |
| GradientBoostingClassifier      | 0.9325        | 0.7183              | 0.7402                               |
| HistGradientBoostingClassifier  | **0.9390**    | 0.7094              | **0.7995**                               |
| KNeighborsClassifier            | 0.8913        | 0.7044              | 0.6992                               |
| RandomForestClassifier          | 0.9311        | 0.7099              | 0.7205                               |
| StackingClassifier              | 0.9385        | 0.7021              | -                               |
| VotingClassifier                | 0.9359        | 0.7205              | -                               |


# Used stack

- ML: Sklearn, Pandas, Laspy
- Experiment Tracking: Weights and Biases, Optuna
- GUI: customtkinter
- Point cloud visualisation: pptk, polyscope, plotly
- Version Control: Git & GitHub
- Organization: GitHub Projects

# License

This project is licensed under the [MIT License](LICENSE).

# Neptun's Eye Team

**GUI & App:**
- [Nikodem Przybyszewski](https://github.com/nexter0)
  
**ML team:**
- [Michał Sztymelski](https://github.com/Stimm147)
- [Kacper Gutowski](https://github.com/Perunio)
- [Jan Karaś](https://github.com/KTFish)
  
**Assistant**
- [Alan Ferenc](https://github.com/Zeusthegoddd)

