#! /usr/bin/env python
# -*- coding: utf8 -*-
"""This is a somewhat delicate package. It contains all registered components
and preconfigured templates.

Hence, it imports all of the components. To avoid cycles, no component should
import this in module scope."""

from chi_annotator.algo_factory import utils
from chi_annotator.algo_factory.preprocess.char_tokenizer import CharTokenizer

# Classes of all known components. If a new component should be added,
# its class name should be listed here.
component_classes = [
    CharTokenizer,
]

# Mapping from a components name to its class to allow name based lookup.
registered_components = {c.name: c for c in component_classes}

# To simplify usage, there are a couple of model templates, that already add
# necessary components in the right order. They also implement
# the preexisting `backends`.
'''
registered_pipeline_templates = {
    "spacy_sklearn": [
        "nlp_spacy",
        "tokenizer_spacy",
        "intent_featurizer_spacy",
        "intent_entity_featurizer_regex",
        "ner_crf",
        "ner_synonyms",
        "intent_classifier_sklearn",
    ],
    "mitie": [
        "nlp_mitie",
        "tokenizer_mitie",
        "ner_mitie",
        "ner_synonyms",
        "intent_entity_featurizer_regex",
        "intent_classifier_mitie",
    ],
    "mitie_sklearn": [
        "nlp_mitie",
        "tokenizer_mitie",
        "ner_mitie",
        "ner_synonyms",
        "intent_entity_featurizer_regex",
        "intent_featurizer_mitie",
        "intent_classifier_sklearn",
    ],
    "keyword": [
        "intent_classifier_keyword",
    ],
    # this template really is just for testing
    # every component should be in here so train-persist-load-use cycle can be
    # tested they still need to be in a useful order - hence we can not simply
    # generate this automatically.
    "all_components": [
        "nlp_spacy",
        "nlp_mitie",
        "tokenizer_whitespace",
        "tokenizer_jieba",
        "tokenizer_mitie",
        "tokenizer_spacy",
        "intent_featurizer_mitie",
        "intent_featurizer_spacy",
        "intent_featurizer_ngrams",
        "intent_entity_featurizer_regex",
        "ner_mitie",
        "ner_crf",
        "ner_spacy",
        "ner_duckling",
        "ner_duckling_http",
        "ner_synonyms",
        "intent_classifier_keyword",
        "intent_classifier_sklearn",
        "intent_classifier_mitie",
    ]
}
'''


def get_component_class(component_name):
    # type: (Text) -> Optional[Type[Component]]
    """Resolve component name to a registered components class."""

    if component_name not in registered_components:
        try:
            return utils.class_from_module_path(component_name)
        except Exception:
            raise Exception(
                    "Failed to find component class for '{}'. Unknown "
                    "component name. Check your configured pipeline and make "
                    "sure the mentioned component is not misspelled. If you "
                    "are creating your own component, make sure it is either "
                    "listed as part of the `component_classes` in "
                    "`rasa_nlu.registry.py` or is a proper name of a class "
                    "in a module.".format(component_name))
    return registered_components[component_name]


def load_component_by_name(component_name,
                           model_dir,
                           metadata,
                           cached_component,
                           **kwargs
                           ):
    # type: (...) -> Optional[Component]
    """Resolves a component and calls it's load method to init it based on a
    previously persisted model."""

    component_clz = get_component_class(component_name)
    return component_clz.load(model_dir, metadata, cached_component, **kwargs)


def create_component_by_name(component_name, config):
    # type: (Text, RasaNLUConfig) -> Optional[Component]
    """Resolves a component and calls it's create method to init it based on a
    previously persisted model."""

    component_clz = get_component_class(component_name)
    return component_clz.create(config)
