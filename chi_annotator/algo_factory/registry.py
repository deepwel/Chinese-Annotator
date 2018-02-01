#! /usr/bin/env python
# -*- coding: utf8 -*-
"""This is a somewhat delicate package. It contains all registered components
and preconfigured templates.

Hence, it imports all of the components. To avoid cycles, no component should
import this in module scope."""

from chi_annotator.algo_factory import utils
from chi_annotator.algo_factory.online.sklearn_cluster import SklearnCluster
from chi_annotator.algo_factory.preprocess.char_tokenizer import CharTokenizer
# from chi_annotator.algo_factory.preprocess.jieba_tokenizer import JiebaTokenizer
from chi_annotator.algo_factory.preprocess.sentence_embed_extractor import SentenceEmbeddingExtractor
from chi_annotator.algo_factory.preprocess.embedding import Embedding
from chi_annotator.algo_factory.preprocess.embedding import EmbeddingExtractor
from chi_annotator.algo_factory.online.sklearn_classifier import SVMClassifier
from chi_annotator.algo_factory.online.sklearn_classifier import SGDClassifier
from chi_annotator.algo_factory.online.sklearn_classifier import KnnClassifier
from chi_annotator.algo_factory.online.sklearn_classifier import RandomForestClassifier
from chi_annotator.algo_factory.online.sklearn_classifier import AdaBoostClassifier
# Classes of all known components. If a new component should be added,
# its class name should be listed here.
component_classes = [
    CharTokenizer,
#   JiebaTokenizer,
    SentenceEmbeddingExtractor,
    Embedding,
    EmbeddingExtractor,
    SklearnCluster,
    SVMClassifier,
    SGDClassifier,
    KnnClassifier,
    RandomForestClassifier,
    AdaBoostClassifier
]

# Mapping from a components name to its class to allow name based lookup.
registered_components = {c.name: c for c in component_classes}

# To simplify usage, there are a couple of model templates, that already add
# necessary components in the right order. They also implement
# the preexisting `backends`.
registered_pipeline_templates = {
    # this is tmp default templates copy from config for pipeline in string mode.
    "word2vec_sklearn": [
        "nlp_word2vec",
        "linesplit_preprocess",
        "feature_extractor",
        "online_svm_classifier_sklearn",
        "offline_svm_classifier_sklearn"
    ]
}


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
    # type: (Text, Config) -> Optional[Component]
    """Resolves a component and calls it's create method to init it based on a
    previously persisted model."""

    component_clz = get_component_class(component_name)
    return component_clz.create(config)
