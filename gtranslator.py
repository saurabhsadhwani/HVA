from __future__ import annotations
from typing import Dict, Text, Any, List

from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData

# pip install googletrans
from googletrans import Translator

# pip install git+https://github.com/siddharth17196/english-hindi-transliteration
from elt import translit

translator = Translator()
print('GTrans initialized')

to_hindi = translit('hindi')

@DefaultV1Recipe.register(
    [DefaultV1Recipe.ComponentType.MESSAGE_FEATURIZER], is_trainable=False
)
class Hi2Eng(GraphComponent):

    @staticmethod
    def required_packages() -> List[Text]:
        """Any extra python dependencies required for this component to run."""
        return ["googletrans", "elt"]

    @classmethod
    def create(
        cls,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext,
    ) -> GraphComponent:
        # TODO: Implement this
        pass
    
    def train(self, training_data: TrainingData) -> Resource:
        # TODO: Implement this if your component requires training
        pass
    
    def process_training_data(self, training_data: TrainingData) -> TrainingData:
        # TODO: Implement this if your component augments the training data with
        #       tokens or message features which are used by other components
        #       during training.
        # components during training.

        return training_data
    
    def process(self, messages: List[Message]) -> List[Message]:
        # TODO: This is the method which Rasa Open Source will call during inference.
        for message in messages:
            txt = message.data['text']
            print(txt)

            addn, count = 0,0
            for letter in txt:
                if ord(letter) == '32':
                    continue
                addn += ord(letter)
            avg = addn/len(txt)
            if avg < 200:
                txt = to_hindi.convert([txt])[0]
                print(txt, ' : ', avg)
            
            txt_new = translator.translate(txt, src='hi', dest='en').text
            message.set(prop='text', info=txt_new)

            print(message.data)

        return messages
