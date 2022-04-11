from __future__ import annotations

from typing import Dict, Text, Any, List
import typing
import stanza
from rasa.nlu.tokenizers.tokenizer import Token, Tokenizer
from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData

if typing.TYPE_CHECKING:
    from spacy.tokens.doc import Doc

# TODO: Correctly register your component with its type
@DefaultV1Recipe.register(
    [DefaultV1Recipe.ComponentType.INTENT_CLASSIFIER], is_trainable=False
)
class Lemmatizer(GraphComponent):
    @classmethod
    def create(
        cls,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext,
    ) -> GraphComponent:
        # TODO: Implement this
        ...

    def train(self, training_data: TrainingData) -> Resource:
        pass

    def process_training_data(self, training_data: TrainingData) -> TrainingData:
        ...

    def process(self, messages: List[Message]) -> List[Message]:
        hi_nlp = stanza.Pipeline('hi')
        
        latest_message = messages[-1].data['text']

        hindi_doc = hi_nlp(latest_message)

        text_tokens = []

        #print(latest_message)

        for sentence in hindi_doc.sentences:
            for current_token in sentence.tokens:
                current_token_dict = current_token.to_dict()[0]
                #print(current_token_dict)
                text_tokens.append(Token(  text = current_token_dict['text'],
                                                                start = current_token_dict['start_char'],
                                                                end = current_token_dict['end_char'],
                                                                data = { 'pos' : current_token_dict['upos'] },
                                                                lemma = current_token_dict['lemma']))
            
        messages[-1].data["text_tokens"] = text_tokens

        return messages