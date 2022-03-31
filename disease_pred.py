import pandas as pd
import numpy as np
from sklearn.naive_bayes import MultinomialNB
import pickle

class Diagnosis:
    def __init__(self) -> None:
        self.model = pickle.load(open('pred_files/nb_model.pkl', 'rb'))
        self.df_precautions = pd.read_csv('pred_files/symptom_precaution.csv')
        
        self.unique_symptoms = []
        with open('pred_files/unq_symptoms.txt','r') as f1:
            self.unique_symptoms = f1.readline().split(':')
            self.classes = f1.readline().split(':')
    
        self.df_symp_freq = pd.read_csv('pred_files/Symptom_frequencies.csv', index_col=0)
        

        print('diagnosis initiated')
    
    def predict(self, symps):
        print('in prediction')

        row_inp = np.zeros(len(self.unique_symptoms))
        for symptom in symps:
            idx = np.where(self.unique_symptoms == symptom.strip(' '))[0]
            row_inp[idx] = 1

        probas = self.model.predict_proba([row_inp])
        predicted_disease = self.model.predict([row_inp])[0]
        
        precautions = self.df_precautions.loc[self.df_precautions['Disease'] == predicted_disease].values[0]
        return (predicted_disease, precautions[1:])
    
    def suggest_symptoms(self, symptom_list):
        latest_symptom = symptom_list[len(symptom_list)-1].strip(' ')
        symp_freq = dict(self.df_symp_freq.loc[latest_symptom])
        suggestions = [k for k, v in sorted(symp_freq.items(), key=lambda item: item[1], reverse=True)][:10]
        suggestions = [item for item in suggestions if item not in symptom_list]
        return suggestions

if __name__=='__main__':
    obd = Diagnosis()
    # disease = obd.predict(['headache', 'cough', 'nausea'])
    # print(disease)
    suggestions = obd.suggest_symptoms(['headache', 'cough', 'nausea'])
    print(suggestions)