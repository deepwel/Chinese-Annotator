#! /usr/bin/env python
# -*- coding: utf8 -*-

from chi_annotator.algo_factory.components import Component


class CharTokenizer(Component):
    provides = ["tokens"]
    name = "char_tokenizer"

    def __init__(self, config=None):
        # type: (AnnotatorConfig) -> None
        self.config = config
        super(Component, self).__init__()

    def train(self, training_data, config, **kwargs):
        # type: (TrainingData, AnnotatorConfig, Any) -> None
        for sample in training_data.example_iter():
            words = CharTokenizer._tokenize(sample.text)
            sample.set("tokens", words)

    def process(self, message, **kwargs):
        # type: (Message, Any) -> None
        words = CharTokenizer._tokenize(message.text)
        message.set("tokens", words)

    @staticmethod
    def _tokenize(text):
        # type: (String) -> List[String]
        words = [word for word in text]
        return words
