#!/usr/bin/python  
# -*- coding: utf-8 -*-

import os

# Describes where to search for the config file if no location is specified

DEFAULT_CONFIG_LOCATION = "config.json"

DEFAULT_CONFIG = {
    "project": None,
    "fixed_model_name": None,
    "config": DEFAULT_CONFIG_LOCATION,
    "data": None,
    "emulate": None,
    "language": "en",
    "log_file": None,
    "log_level": 'INFO',
    "mitie_file": os.path.join("data", "total_word_feature_extractor.dat"),
    "spacy_model_name": None,
    "num_threads": 1,
    "max_training_processes": 1,
    "path": "projects",
    "port": 5000,
    "token": None,
    "cors_origins": [],
    "max_number_of_ngrams": 7,
    "pipeline": [],
    "response_log": "logs",
    "aws_endpoint_url": None,
    "duckling_dimensions": None,
    "duckling_http_url": None,
    "ner_crf": {
        "BILOU_flag": True,
        "features": [
            ["low", "title", "upper", "pos", "pos2"],
            ["bias", "low", "word3", "word2", "upper", "title", "digit", "pos", "pos2", "pattern"],
            ["low", "title", "upper", "pos", "pos2"]],
        "max_iterations": 50,
        "L1_c": 1,
        "L2_c": 1e-3
    },
    "intent_classifier_sklearn": {
        "C": [1, 2, 5, 10, 20, 100],
        "kernel": "linear"
    }
}


class InvalidConfigError(ValueError):
    """Raised if an invalid configuration is encountered."""

    def __init__(self, message):
        # type: (Text) -> None
        super(InvalidConfigError, self).__init__(message)


class AnnotatorConfig(object):
    DEFAULT_PROJECT_NAME = "default"

    def __init__(self, filename=None):
        pass

    def __getitem__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __delitem__(self, key):
        del self.__dict__[key]

    def __contains__(self, key):
        return key in self.__dict__

    def __len__(self):
        return len(self.__dict__)

    def __getstate__(self):
        return self.as_dict()

    def __setstate__(self, state):
        self.override(state)

    def items(self):
        return list(self.__dict__.items())

    def as_dict(self):
        return dict(list(self.items()))
