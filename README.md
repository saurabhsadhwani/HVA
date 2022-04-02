# HVA
### Hindi Voice Assistant
<br>

## Installation procedure
1. Create virtual environment for rasa with python venv
```
python3 -m venv ./venv
source ./venv/bin/activate
```
or create environment with conda
```
conda create --name rasa_env
conda activate rasa_env
```

2. Install rasa into environment
```
pip install rasa
```

3. Install other needed things
```
pip install Flask pickle numpy pandas scikit-learn googletrans==4.0.0-rc1 git+https://github.com/siddharth17196/english-hindi-transliteration
```
<br>

## Running the model
It will need three terminals running in parallel.
- In first one, train and run rasa model
  ```
  rasa train
  rasa run --enable-api -vv --cors "*"
  ```
- In second one, run rasa actions
  ```
  rasa run actions
  ```
- In third one, start ui server with flask
  ```
  python3 app.py
  ```
  
Open port mentioned in third terminal in browser to have conversation with bot
