## Bloomon - Code Challenge

This is a project based on an assignment given by [Bloomon](https://www.bloomon.nl).
The assignment description can be found [here](./docs/challenge-description.pdf).

### Table of contents:
- [Prerequisites](#prerequisites)
- [Usage](#usage)
    - [Usage: Docker](#usage-docker)
    - [Usage: Manual](#usage-manual)
- [Run Tests](#run-tests)

### Prerequisites
* [Docker](https://docs.docker.com/engine/installation/)

**Optional:**
* [Python 3.8](https://www.python.org/downloads/)

### Usage
#### Usage: Docker

1. Make sure `Docker` is installed and running properly.
1. Open the terminal and go to the directory of this project.
1. In case necessary, you can add additional `input files` in the directory `inputs`.
   The application will process all the `input files` in the directory.
   **Note**: Make sure the files are in the correct format!
1. Run the following command to build the docker image:
    ```commandline
    $ docker build -t cirx-bloomon .
    ```
1. Run the following command to run the docker image:
    ```commandline
    $ docker run -v $PWD/outputs:/usr/src/app/outputs cirx-bloomon
    ```
1. The results of the input files are placed in the directory `outputs` after a successful run.

#### Usage: Manual
1. Make sure `Python` is installed and running properly.
1. Open the terminal and go to the directory of this project.
1. Run the following command to run the application.
    ```
    $ python3 main.py
    ```

### Run Tests
1. Make sure `Python` is installed and running properly.
1. In case necessary, activate a virtual environment for this project.
1. Run the following command to install the required packages for this project.
    ```
    $ pip install -r requirements.txt
    ```
1. Run the following command to run the tests.
    ```
    $ pytest
    ```
