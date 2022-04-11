# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from SymptomsDiagnosis import SymptomsDiagnosis
import pickle 
from numpy import array
from time import sleep

# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


diagnosis_object = SymptomsDiagnosis()
symptoms_suggested_so_far = []

class ActionSymptomsTracker(Action):

    def name(self) -> Text:
        return "action_symptoms_tracker"
        
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # get the latest entity
        latest_entity = tracker.latest_message['entities']
        entity_traced = False

        print(latest_entity)

        # get users symptoms
        symptoms = tracker.get_slot("symptom_list")

        # check for symptoms 
        if symptoms is None:
            symptoms = []

        # add current sypmtom to symptoms list or state already noted
        if (not entity_traced) and latest_entity:
            combined_entity = ""
            for i in range (len(latest_entity)):
                combined_entity += latest_entity[i]['value'] + " "
            
            combined_entity = combined_entity.strip()
            print(combined_entity)
            if combined_entity in symptoms:
                dispatcher.utter_message("आपने पहले से ही इस " + combined_entity + " लक्षण ों का उल्लेख किया है")
            else:
                symptoms.append(combined_entity)
                entity_traced = True

        # if latest_entity:
        #     symptoms.append(latest_entity[0]['value'])
        #     entity_traced = True

        # update slot for future use
        SlotSet("symptom_list", symptoms)

        # get suggestion of next symptom 
        suggested_symptoms = diagnosis_object.symptoms_suggester(symptoms, symptoms_suggested_so_far)

        # list for suggested symptoms
        already_suggested = []
                
        # if no suggestion are made so far
        if suggested_symptoms is None:
            dispatcher.utter_template('utter_alternative', tracker)
            return [SlotSet("symptom_list", symptoms)]

        # append suggested symptom to already_suggested
        if suggested_symptoms in symptoms_suggested_so_far:
            already_suggested.append(suggested_symptoms)

        # Reason : we want to update user for highest confidence symptoms already_suggested

        symptoms_suggested_so_far.append(suggested_symptoms)

        # Create response buttons
        buttons = [{"title": "जी हाँ " + suggested_symptoms +" भी है", "payload": suggested_symptoms},{"title":"जी नहीं", "payload": ""}]

        # Send response to ui
        # dispatcher.utter_message("आपने कहा था कि आपको : " + symptoms[-1] + " है |")
        dispatcher.utter_button_message("क्या आपको "+ suggested_symptoms + " के लक्षण भी है?", buttons)

        print("symptoms", symptoms)

        return [SlotSet("symptom_list", symptoms)]
        

    

class ActionDiagnosis(Action):

    def name(self) -> Text:
        return "action_diagnosis"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # get users symptoms
        symptoms = tracker.get_slot("symptom_list")

        # Get diagnosis
        diag = diagnosis_object.predict_proba(symptoms)

        # Send message
        dispatcher.utter_message("हमारे मॉडल ने " + diag + " रोग की भविष्यवाणी की है |" )

        SlotSet("symptom_list", [])

        # debugging 
        # print("Slot updated", tracker.get_slot("symptom_list"))

        return [SlotSet("symptom_list", [])]