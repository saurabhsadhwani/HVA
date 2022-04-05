from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

import pickle

import random
from disease_pred import Diagnosis
from googletrans import Translator

import nltk
from nltk.tokenize import word_tokenize 
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

# will need these downloads for first time run :
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')

print('In actions')

# Global variables and objects for actions
translator = Translator()
dObj = Diagnosis()
suggested_so_far = []
lemmatizer= WordNetLemmatizer()

pickled_data = pickle.load(open('pred_files/pickled_data.pkl', 'rb'))
symptom_synonyms = pickled_data['symptom_synonyms']


class ActionHandleSymptom(Action):

    def name(self) -> Text:
        return "action_handle_symptom"
    
    def get_wordnet_pos(self, treebank_tag):
        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            return None

    def lemmatize_detected_entity(self, symptom):
        nltk_tokenlist = word_tokenize(symptom)
        tagged = nltk.pos_tag(nltk_tokenlist)

        nltk_lemmas = []
        for word, tag in tagged:
            wntag = self.get_wordnet_pos(tag)
            word = word.lower()
            if wntag is None: # not supply tag in case of None
                lemma = lemmatizer.lemmatize(word) 
            else:
                lemma = lemmatizer.lemmatize(word, pos=wntag)
            nltk_lemmas.append(lemma)
        
        # convert them back to string of words
        nltk_lemmas = ' '.join(nltk_lemmas)

        return nltk_lemmas

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entities = tracker.latest_message.get('entities')
        print(entities)

        # Get symptoms slot
        syms = tracker.get_slot("symptom_list")
        if syms is None:
            syms = []

        symptoms_detected = []
        for entity in entities:
            sympt = self.lemmatize_detected_entity(entity['value'])

            for main_symptom, synonyms in symptom_synonyms.items():
                for synonym in synonyms:
                    if sympt==synonym.strip(' '):
                        sympt = main_symptom

            # Check if symptom in list
            if sympt not in syms:
                syms.append(sympt)
                symptoms_detected.append(sympt)
            else:
                dispatcher.utter_message("पहले ही नोट कर लिया है कि आपको ये लक्षण है: "+translator.translate(sympt, src='en', dest='hi').text)
                return []
        
        # Update slot
        SlotSet("symptom_list", syms)

        # Get suggested symptom based on input
        suggested_symptom = dObj.suggest_symptoms(syms)
        
        # Check if symptom not already suggested
        clean_syms=[]

        for symp in suggested_symptom:
            if symp not in syms and symp not in suggested_so_far:
                clean_syms.append(symp)
            else:
                suggested_so_far.append(symp)

        if(len(clean_syms)>0):
            num = random.randrange(0,len(clean_syms))
        else:
            dispatcher.utter_template('utter_alternative')
            return [SlotSet("symptom_list", syms)]

        # Create response buttons
        buttons = [{"title": "हां", "payload": translator.translate(clean_syms[num], src='en', dest='hi').text}, {"title":"नहीं", "payload": "नहीं"}]

        # Translate back into hindi
        for i,detected_symptom in enumerate(symptoms_detected):
            symptoms_detected[i] = translator.translate(detected_symptom, src='en', dest='hi').text

        # Send message
        dispatcher.utter_message("आपने कहा कि आपको " + "और".join(symptoms_detected) + "है")
        dispatcher.utter_button_message("क्या आपको " + translator.translate(clean_syms[num], src='en', dest='hi').text + "भी है?", buttons)

        print('suggested ',clean_syms[num])
        
        return [SlotSet("symptom_list", syms)]

class ActionDiagnosis(Action):

    def name(self) -> Text:
        return "action_diagnosis"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get symptoms slot
        syms = tracker.get_slot("symptom_list")

        # Get diagnosis
        diag = dObj.predict(syms)
        print('Predicted disease : ', diag[0])
        # Send message
        dispatcher.utter_message("हमारा निदान: " + translator.translate(str(diag[0]), src='en', dest='hi').text)
        dispatcher.utter_message("सुझाई गई सावधानियां: ")
        for d in diag[1]:
            msg = translator.translate(str(d), src='en', dest='hi').text
            dispatcher.utter_message(str(msg))

        dispatcher.utter_message("क्या इससे आपको मदद मिली?")

        return []