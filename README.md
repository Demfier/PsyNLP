# PsyNLP

> Program SYnthesis for NLP

PsyNLP is a Python library, that intends to handle morphological inflections for any language in the form of an interpretable program. :tada:

### Table of Contents

1. [Installation Guidelines](#installation-guidelines)
2. [Running the scripts](#running-the-scripts)
3. [Visualizing a formal concept](#visualizing-a-formal-concept)
4. [Repository structure](#repository-structure)
5. [Running the tests](#running-the-tests)
6. [Contribution Guidelines](#contribution-guidelines)
7. [License](#license)

### Installation Guidelines

[(Back to ToC)](#table-of-contents)

- Installing from PIP

```sh
$ pip3 install psynlp
```

- Setting up locally

1. Clone the repository

```sh
$ git clone git@github.com:Demfier/PsyNLP.git
```

2. Go to the cloned repository

```sh
$ cd PsyNLP
```

3. Install the dependencies

```sh
$ pip3 install -r requirements.txt
```

Alternatively, you can also install the module from pip directly using the command:

`pip3 install psynlp`

### Running the scripts

[(Back to ToC)](#table-of-contents)

With the power of `argparse`, the [main.py](https://github.com/Demfier/PsyNLP/blob/master/main.py) acts as the central script to run any of the pipelines, for any language and training data quality.


- Help menu, for more details:

```sh
$ python3 main.py -h
```

```
usage: main.py [-h] [-p PIPELINE] [-l LANGUAGE] [-q QUALITY] [-v]

Runs one of the pipeline scripts, for a given language and quality.

optional arguments:
  -h, --help            show this help message and exit
  -p PIPELINE, --pipeline PIPELINE
                        Name of the pipeline file (Default: deterministic)
  -l LANGUAGE, --language LANGUAGE
                        Name of the language (Default: english)
  -q QUALITY, --quality QUALITY
                        Size of the training data (Default: low)
  -v, --verbose         Prints verbose output if specified
```


- Running a pipeline (say, ostia) for a language (say, polish) and training data quality (say, high):

```sh
$ python3 main.py -p ostia -l polish -q high
```

- Get more output debug-like details with verbose flags (max. 3)

```sh
# No verbose, just print the exact word-match accuracy
$ python3 main.py

# Verbose 1, print the expected and actual words
$ python3 main.py -v

# Verbose 2, print the paths responsible for computing an inflection
$ python3 main.py -vv

# Verbose 3, print debug details for PAC and OSTIA
$ python3 main.py -vvv
```

### Visualizing a formal concept

[(Back to ToC)](#table-of-contents)

![image](https://user-images.githubusercontent.com/17109060/38651955-79bc24ac-3e21-11e8-8db3-6b87314a7129.png)

The `cytoscape` library has been used to visualize a formal concept. A sample notebook showing the visualization can be [seen here](visualize.ipynb).

```sh
# Show files in the visual/ directory
$ ls visual/
```

```
|
|_ cytoscape.tmpl (The html template file)
|_ style.cycss (The cytoscape css file)

```

- Before running the notebook:

```sh
# Go to visual/ directory
$ cd visual/

# Start the HTTP server on port 8000, from the visual/ directory
$ python3 -m http.server -p 8000

```


- Now, run the notebook from the root directory (Do a `cd ~/..` if required):

```sh
# Open the jupyter notebook
$ jupyter notebook
```

An interactive plot with zoom, search and filter features should appear on your `visualize.ipynb` notebook. If you'd like a html file, you'll also be able to see a `sample.html` and `sample.json` generated in the `visual/` directory.

### Repository structure

[(Back to ToC)](#table-of-contents)

- Base classes:

  The code for base classes can be found in the `psynlp/core` directory.

  - `fca.py`: Contains implementations of PAC and other methods related to Formal Concept Analysis
  - `fst.py`: Contains generic Transducer methods, like states and arcs
  - `oracle.py`: Contains the oracles that're used while computing the PAC basis in `fca.py`
  - `ostia.py`: Implementation of the well-known OSTIA algorithm, that uses `fst.py`

- Pipelines:

  The code for the different pipelines can be found in the `psynlp/pipelines` directory.

  - `deterministic.py` : Prediction based on Pandas' `group_by` (deterministic clustering) and OSTIA RegExp matching
  - `ostia.py`: Prediction based on just the input-output tapes of OSTIA
  - `pac_ostia.py`: Prediction based on PAC clusters and OSTIA RegExp matching

- Helpers:

  The code for the different helpers can be found in the `psynlp/helpers` directory.

  - `builtins.py`: Monkey-patches some required verbose-related builtin functions
  - `importers.py`: Includes functions that imports training and testing data into different structures
  - `misc.py`: Miscellaneous functions
  - `text.py`: Text-related functions such as inflecting, prefix, suffix, edit distance, etc.

- Data:

  The `psynlp/data` directory contains all the training and testing data. The files are of the form:

  - {language}-train-{quality}
  - {language}-dev

### Running the tests

1. Basic run to check the results:

```sh
py.test
```

2. For debugging:

```sh
py.test -s --fulltrace
```

### Contribution Guidelines

[(Back to ToC)](#table-of-contents)

Your contributions are always welcome! Please have a look at the [contribution guidelines](CONTRIBUTING.md) first. :tada:

### License

[(Back to ToC)](#table-of-contents)

MIT License 2018 - [Gaurav Sahu](https://github.com/Demfier/) and [Athitya Kumar](https://github.com/athityakumar/).
