#!/usr/bin/python  
# -*- coding: utf-8 -*-
"""
author: bookerbai
create:2017/11/22
"""
import os
import io
import json
import typing
import numpy as np

from chi_annotator.algo_factory.components import Component

if typing.TYPE_CHECKING:
    from gensim.models.keyedvectors import KeyedVectors


class SentenceEmbeddingExtractor(Component):

    name = "sentence_embedding_extractor"

    requires = ["tokens"]
    provides = ["sentence_embedding"]

    def __init__(self, embedding_cfg):
        super(SentenceEmbeddingExtractor, self).__init__()
        is_binary = True if embedding_cfg["type"] == "bin" else False
        from gensim.models.keyedvectors import KeyedVectors
        self.embedding = KeyedVectors.load_word2vec_format(embedding_cfg["path"], binary=is_binary)
        self.embedding_cfg = embedding_cfg

    @classmethod
    def required_packages(cls):
        # type: () -> List[Text]
        return ["gensim"]

    @classmethod
    def cache_key(cls, model_metadata):
        # type: (Metadata) -> Optional[Text]
        # unique
        return cls.name + "-" + str(os.path.abspath(cls.embedding_cfg["path"] + cls.embedding_cfg["type"]))

    @classmethod
    def create(cls, config):
        embedding_cfg = config.get("embedding", None)
        if embedding_cfg is None:
            return None
        return SentenceEmbeddingExtractor(embedding_cfg)

    def provide_context(self):
        # type: () -> Dict[Text, Any]
        return {"embedding": self.embedding}

    def train(self, training_data, config, **kwargs):
        for sample in training_data:
            self.process(sample, **kwargs)

    def process(self, message, **kwargs):
        embeddings = []
        tokens = message["tokens"]
        if tokens is not None:
            for token in tokens:
                # if word in vocab then add into list
                if token in self.embedding:
                    embeddings.append(self.embedding[token])
        words_len = len(embeddings)
        if words_len > 0:
            sentence_embeds = np.asarray(embeddings, dtype=float).sum(axis=1)
            sentence_embeds /= words_len
            message.set("sentence_embedding", sentence_embeds)
        else:
            message.set("sentence_embedding", None)

    @classmethod
    def load(cls, model_dir=None, model_metadata=None, cached_component=None, **kwargs):
        # type: (Text, Metadata, Optional[Word2VecNLP], **Any) -> Word2VecNLP
        if cached_component:
            return cached_component
        return SentenceEmbeddingExtractor(model_metadata)

    def persist(self, model_dir):
        # type: (Text) -> Dict[Text, Any]
        full_name = os.path.join(model_dir, self.name + ".json")
        with io.open(full_name, 'w') as f:
            f.write(str(json.dumps(self.embedding_cfg)))
        return self.embedding_cfg
