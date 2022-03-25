import pandas as pd
import numpy as np
from sklearn.svm import SVC
import pickle

class Diagnosis:
    def __init__(self) -> None:
        self.df_symp_map = pd.read_csv('symptom_map.csv')
        self.model = pickle.load(open('svc_model.pkl', 'rb'))
        self.df_precautions = pd.read_csv('symptom_precaution.csv')
        print('diagnosis initiated')
    
    def predict(self, symps):
        print('in prediction')
        X = []
        for symptom in symps:
            symptom = symptom.strip(' /n')
            symptom.replace(' ', '_')
            if symptom in self.df_symp_map['symptom'].values:
                n = self.df_symp_map.loc[self.df_symp_map['symptom'] == symptom,'num'].values[0]
                X.append(n)
            else:
                X.append(0)
        while len(X) < 17:
            X.append(0)
        
        X = np.array([X])
        predicted_disease = self.model.predict(X)
        predicted_disease = predicted_disease[0]
        precautions = self.df_precautions.loc[self.df_precautions['Disease'] == predicted_disease].values
        
        print(predicted_disease)
        print(precautions)
        
        return (predicted_disease, precautions[1:])
    
    def suggest_symptoms(self, symptom_list):
        all_symps = self.df_symp_map['symptom'].values
        print('suggested all')
        return all_symps

if __name__=='__main__':
    obd = Diagnosis()
    disease = obd.predict(['headache', 'cough', 'nausea'])
    print(disease)
