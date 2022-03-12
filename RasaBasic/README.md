
# Procedure

## Installation of Rasa for Linux

<br>

### Conda Users

```
conda create -n {yourenvname} python=3.x anaconda
cd ../HVA
pip install rasa
rasa --version
```

<br>

### Other Users

```
pip install virtualenv
python3 -m venv path/to/new/virtualenv/
source <path/to/new/virtualenv>/bin/activate
cd ../HVA
pip install rasa
rasa --version
```

Currently, Rasa only supports 3.7 and 3.8 version of python.

Please make sure the rasa installed have version greater than 3.0.

<br>

## Initialization of Basic Rasa

```
cd ../HVA
mkdir RasaBasic
cd RasaBasic
rasa init -y
```

This will initialize and train basic rasa model.

For more query or issue please check the official rasa [documentation](https://rasa.com/docs/rasa/).

<br>

## Run Basic Rasa Model on terminal

```
cd ../HVA/RasaBasic
rasa shell
```

This lines code can be used to run rasa model locally and interact with model on terminal.

<br>

## Run Basic Rasa Model on localhost

```
cd ../HVA/RasaBasic
rasa run -m models --enable-api --cors "*"
```

This lines code can be used to run rasa model locally on port 5005 and communicate with user interface.

<br>