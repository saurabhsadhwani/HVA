import pandas as pd
from spacy.lang.hi import Hindi
from os.path import abspath, dirname, join
from sklearn.neighbors import KNeighborsClassifier
import pickle
from numpy import where, array

response_variable = 'बीमारी'

BASE_DIR = abspath(dirname(__file__))


class SymptomsDiagnosis:

    def __init__(self):
        # Reading the dataset from csv file
        self.dataset = pd.read_excel(join(BASE_DIR, "dataset.xlsx"))

        # Unpickle the trained Decision Tree model 
        with open('decisionTree.pkl', 'rb') as f:
            self.mlmodel = pickle.load(f)

        # Unpickle the diseases dictionary
        with open('disease.pkl', 'rb') as f:
            self.diseases = pickle.load(f)

        # Unpickle the dimensions list
        with open('dimensions.pkl', 'rb') as f:
            self.dimensions = pickle.load(f)

        # Spacy instance for stemming hindi words
        self.stemmer = Hindi()

        # Split the dataset in Independent Variable (X) and Dependent Variable (Y)
        self.Y = self.dataset[response_variable]
        self.X = self.dataset.drop(response_variable, axis=1)

        # Getting all symptoms 
        self.all_symptoms = self.X.columns

        # Stemming all the symptoms
        # self.stemmed_symptoms = [self.stemmer.pipe(symptoms).text for symptoms in self.all_symptoms]
        self.stemmed_symptoms = list(self.stemmer.pipe(self.all_symptoms))

    def __symptoms_vectorizer(self, symptoms):
        """
        Vectorize all the user symptoms accoring to sequence of self.stemmed_symptoms
        """

        # vectorize user symtoms for testing data
        vector = []
        for symptom in self.dimensions:
            if str(symptom) in symptoms:
                vector.append(1)
            else:
                vector.append(0)

        return vector


    def __suggest_symptoms(self, user_symptoms, suggested_so_far):
        """
        Private method for symptoms suggester
        """
        # method 1: but not working 
        # next_symptom = list(set(self.stemmed_symptoms) - set(user_symptoms))
        
        next_symptom = []
        for symp in self.stemmed_symptoms:
            symp = str(symp)
            if symp not in user_symptoms and symp not in suggested_so_far:
                next_symptom.append(symp)
        
        return next_symptom


    def symptoms_suggester(self, symptoms_from_user, suggested_so_far):
        """
        Public method for symptoms suggester
        """
        return self.__suggest_symptoms(symptoms_from_user, suggested_so_far)


    def vectorizer(self,  user_symptoms):
        """
        Public method to vectorize your symptoms
        """
        return self.__symptoms_vectorizer(user_symptoms)


    def __disease_prediction(self, user_symptoms):
        """
        Private method of disease predictions
        """
        
        # convert all the symptoms user stated to vector
        test_data = self.__symptoms_vectorizer(user_symptoms)

        # perform predict on test_data on ml model
        prediction = self.mlmodel.predict_proba([test_data])

        # find index of our prediction and returned array by model is 2d array
        index = where(prediction[0]==max(prediction[0]))[0][0]
        
        # find the key where value matches our index and return it
        for disease, values in self.diseases.items():
            if values == index:
                return disease

        return None

    def predict_proba(self, user_symptoms):
        return self.__disease_prediction(user_symptoms)


    # Method for debugging purpose
    def printer(self):
        print("I'm working fine...")

if __name__ == "__main__":
    obj = SymptomsDiagnosis()
    obj.printer()