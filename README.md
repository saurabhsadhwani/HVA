
# Procedure

## Installation of Rasa

<br>

### Conda Users

```
conda create -n {yourenvname} python=3.x anaconda
cd ../Hindi-Voice-Assistant
pip install rasa
rasa --version
```

<br>

### Other Users

```
pip install virtualenv
python3 -m venv path/to/new/virtualenv/
source <path/to/new/virtualenv>/bin/activate
cd ../Hindi-Voice-Assistant
pip install rasa
rasa --version
```

Currently, Rasa only supports 3.7 and 3.8 version of python.

Please make sure rasa installed have version greater than 3.0.

<br>

## Initialization of Nominal Rasa Model

```
cd ../Hindi-Voice-Assistant
mkdir chatbot
cd chatbot
rasa init -y
```

This will initialize and train basic rasa model.

For more query or issue please check the official rasa [documentation](https://rasa.com/docs/rasa/).

<br>

## Run Rasa chatbot model on terminal

```
cd ../Hindi-Voice-Assistant/chatbot
rasa shell
```

This lines code can be used to run rasa model locally and interact with model on terminal.

<br>

## Run Rasa chatbot model on localhost

```
cd ../Hindi-Voice-Assistant/chatbot
rasa run -m models --enable-api --cors "*"
```

This lines code can be used to run rasa model locally on port 5005 and communicate with user interface.

<br>

## Run Rasa action server on localhost

```
cd ../Hindi-Voice-Assistant/chatbot
rasa run actions
```

This lines code can be used to run rasa action server locally on port 5055 and communicate with rasa model.

<br>

**Note : For seamless experience keep running rasa model and rasa action server simultaneously.**
