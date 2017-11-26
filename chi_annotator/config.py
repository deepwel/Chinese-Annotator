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
    "language": "zh",
    "log_file": None,
    "log_level": 'INFO',
    "num_threads": 1,
    "max_training_processes": 1,
    "path": "/",
    "pipeline": [],
    "embedding_path": "tests/data/vec.txt",
    "embedding_type": "text",
    "classifier_sklearn": {
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
        self.override(DEFAULT_CONFIG)

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

    def override(self, config):
        self.__dict__.update(config)
