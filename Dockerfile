FROM python:3.8.13-buster AS BASE

RUN apt-get update \
    && apt-get --assume-yes --no-install-recommends install \
        build-essential \
        curl \
        git \
        jq \
        libgomp1 \
        vim

WORKDIR /app

# upgrade pip version
RUN pip install --no-cache-dir --upgrade pip

RUN pip install rasa==3.0.7
RUN pip install pandas spacy openpyxl stanza
RUN python -c "stanza.download('hi')"

ADD config.yml config.yml
ADD domain.yml domain.yml
ADD credentials.yml credentials.yml
ADD endpoints.yml endpoints.yml
ADD dataset.xlsx dataset.xlsx
ADD dimensionsRandomForest.pkl dimensionsRandomForest.pkl
ADD disease.pkl disease.pkl
ADD printer.py printer.py
ADD randomForest.pkl randomForest.pkl
ADD SymptomsDiagnosis.py SymptomsDiagnosis.py
