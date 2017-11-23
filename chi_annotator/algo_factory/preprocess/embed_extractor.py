#!/usr/bin/python  
# -*- coding: utf-8 -*-
"""
author: bookerbai
create:2017/11/22
"""
from chi_annotator.algo_factory.components import Component
import typing

if typing.TYPE_CHECKING:
    from gensim.models.keyedvectors import KeyedVectors


class EmbeddingExtractor(Component):
    name = "embedding_extractor"

    requires = ["tokens"]
    provides = ["word_embedding"]

    def __init__(self, config):
        super(EmbeddingExtractor, self).__init__()
        self.config = config

    @classmethod
    def required_packages(cls):
        # type: () -> List[Text]
        return ["gensim"]

    @classmethod
    def cache_key(cls, model_metadata):
        # type: (Metadata) -> Optional[Text]
        return None

    @classmethod
    def create(cls):
        from gensim.models.keyedvectors import KeyedVectors
        is_binary = True if cls.config["word2vec_format"] == "bin" else False
        # TODO 这个地方需要重写，返回的是embedding数据
        return EmbeddingExtractor(cls.word2vec_file, KeyedVectors.load_word2vec_format(cls.config["word2vec_file"], binary=is_binary))

    def provide_context(self):
        # type: () -> Dict[Text, Any]
        return {"embedding" : self.create()}

    def train(self, training_data, config, **kwargs):
        for sample in training_data:
            tokens = sample.get("tokens")
            embedding = []
            if tokens is not None:
                # TODO 根据token取embedding
                pass
            sample.set("word_embedding", embedding)

    def process(self, message, **kwargs):
        tokens = message.get("tokens")
        embedding = []
        if tokens is not None:
            # TODO 根据token取embedding
            pass
        message.set("word_embedding", embedding)

    @classmethod
    def load(cls, model_dir=None, model_metadata=None, cached_component=None, **kwargs):
        # type: (Text, Metadata, Optional[Word2VecNLP], **Any) -> Word2VecNLP
        from gensim.models.keyedvectors import KeyedVectors

        if cached_component:
            return cached_component

        word2vec_file = model_metadata.get("word2vec_file")
        is_binary = True if model_metadata["word2vec_format"] == "bin" else False
        return EmbeddingExtractor(word2vec_file, KeyedVectors.load_word2vec_format(word2vec_file, binary=is_binary))

    def persist(self, model_dir):
        # type: (Text) -> Dict[Text, Any]
        # more meta data TODO
        return {
            # "mitie_feature_extractor_fingerprint": self.extractor.fingerprint,
            "word2vec_file": self.word2vec_file
        }
