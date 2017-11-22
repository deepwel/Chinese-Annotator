from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys

import typing
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Text

from rasa_nlu.components import Component
from rasa_nlu.model import Metadata

if typing.TYPE_CHECKING:
    from gensim.models.keyedvectors import KeyedVectors

reload(sys)
sys.setdefaultencoding('utf-8')


class Word2VecNLP(Component):
    name = "nlp_word2vec"

    provides = ["word2vec_feature_extractor"]

    def __init__(self, word2vec_file, extractor=None):
        self.extractor = extractor
        self.word2vec_file = word2vec_file
        Word2VecNLP.ensure_proper_language_model(self.extractor)

    @classmethod
    def required_packages(cls):
        # type: () -> List[Text]
        return ["gensim"]

    @classmethod
    def create(cls, config):
        from gensim.models.keyedvectors import KeyedVectors
        is_binary = True if config["word2vec_format"] == "bin" else False
        return Word2VecNLP(config["word2vec_file"], KeyedVectors.load_word2vec_format(config["word2vec_file"], binary=is_binary))

    @classmethod
    def cache_key(cls, model_metadata):
        # type: (Metadata) -> Optional[Text]

        word2vec_file = model_metadata.metadata.get("word2vec_file", None)
        if word2vec_file is not None:
            return cls.name + "-" + str(os.path.abspath(word2vec_file))
        else:
            return None

    def provide_context(self):
        # type: () -> Dict[Text, Any]

        return {"word2vec_feature_extractor": self.extractor}

    @staticmethod
    def ensure_proper_language_model(extractor):
        # type: (Optional[KeyedVectors.load_word2vec_format]) -> None

        if extractor is None:
            raise Exception("Failed to load Word2vec feature extractor. Loading the model returned 'None'.")

    @classmethod
    def load(cls, model_dir=None, model_metadata=None, cached_component=None, **kwargs):
        # type: (Text, Metadata, Optional[Word2VecNLP], **Any) -> Word2VecNLP
        from gensim.models.keyedvectors import KeyedVectors

        if cached_component:
            return cached_component

        word2vec_file = model_metadata.get("word2vec_file")
        is_binary = True if model_metadata["word2vec_format"] == "bin" else False
        return Word2VecNLP(word2vec_file, KeyedVectors.load_word2vec_format(word2vec_file, binary=is_binary))

    def persist(self, model_dir):
        # type: (Text) -> Dict[Text, Any]
        # more meta data TODO
        return {
            # "mitie_feature_extractor_fingerprint": self.extractor.fingerprint,
            "word2vec_file": self.word2vec_file
        }
