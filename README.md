## Setup Environment

To run this project, you will need to set up the environment. You can choose to use Anaconda or a Python virtual environment using `pipenv`.

### Anaconda Environment

1. Create and activate a new conda environment:

    ```bash
    conda create --name main-ds python=3.9
    conda activate main-ds
    ```

2. Install the necessary dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### Shell/Terminal

1. Create and navigate to the project directory:

    ```bash
    mkdir proyek_analisis_data
    cd proyek_analisis_data
    ```

2. Install the virtual environment and dependencies using pipenv:

    ```bash
    pipenv install
    pipenv shell
    pip install -r requirements.txt
    ```

## Running the Streamlit App

To start the dashboard, navigate to the root directory of the project and run the following command:

```bash
streamlit run dashboard.py
```


## Requirements
To run this project, you need to install the following Python packages:

```bash
streamlit
pandas
matplotlib
seaborn
numpy
```

You can install the dependencies by running:
```bash
pip install -r requirements.txt
```
