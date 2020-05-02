---
urlcolor: blue
geometry: margin=1in
papersize: A4
---

# Soil water balance and penetration resistance modeling


## Description

The main code for simulating soil water balance and soil penetration resistance under water-controlled environments.
The details about the models and the results, as well as other important references are found in [Souza et al. (2020)](https://www.journals.elsevier.com/soil-and-tillage-research).

This code was written using [Python 3.7](https://www.python.org/) and requires the fellow libraries:

- [numpy](https://numpy.org/)
- [pandas](https://pandas.pydata.org/)
- [matplotlib](https://matplotlib.org/)
- [tqdm](https://pypi.org/project/tqdm/)

In order to have a better performance, make sure that the latest version of these libraries are installed.
This project is structured as the following:

|Folder or file                          |Description                                                             |
|----------------------------------------|------------------------------------------------------------------------|
|data                                    | folder with input data and parameters                                  |
|results                                 | folder the model outputs will be saved                                 |
|[requirements.txt](requirements.txt)    | list of packages need to install|
|[run\_simulation.py](run_simulation.py) | python code to run the simulations                                     |
|[spr\_models.py](spr_models.py)         | python code with the models (module) to be imported during the running |


# Instrunctions

1. Install [Python 3.7](https://www.python.org/) or higher;
2. Install the required libraries listed in [requirements.txt](requirements.txt);
    - Optionally, you can install Python and the libraries through [Anaconda](https://www.anaconda.com/products/individual);
3. You may need a IDE to open and edit the code before run it. If you do not know any, try [IDLE](https://www.poftut.com/download-install-and-use-python-idle-editor/);
4. Put the daily rainfall data and the parameters into the folder **data** different in two csv files;
5. Try to run the example data before using your data (optional);
6. Open the file [run_simulation.py](run_simulation.py) and change the name of your file with data and parameters and save the file;
7. Run [run_simulation.py](run_simulation.py) and the results will appear in the folder results.

You can change the initial value of soil moisture to compute the dryness time based on the starting point and the soil parameters.

We do not recommend you to edit [spr_models.py](spr_models.py) unless you want to change the equations.
In any case, it is recommend to backup the project before edit the files.


## Contact

Rodolfo Souza - rodolfosouza@usp.br

André Ferraz - andrepfferraz@gmail.com

---
# CHANGELOG



## v 1.0.0, 2020-05-01
- Project created;
- Documentation;
- Plot sample of the results;
- requirements file.