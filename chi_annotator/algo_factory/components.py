#! /usr/bin/env python
# -*- coding: utf-8 -*-
# coding=utf-8

from chi_annotator.algo_factory.common import MissingArgumentError
from chi_annotator.algo_factory.common import Metadata

import logging

logger = logging.getLogger(__name__)


def validate_arguments(pipeline, context, allow_empty_pipeline=False):
    # type: (List[Component], Dict[Text, Any], bool) -> None
    """Validates a pipeline before it is run. Ensures, that all arguments are present to train the pipeline."""

    # Ensure the pipeline is not empty
    if not allow_empty_pipeline and len(pipeline) == 0:
        raise ValueError("Can not train an empty pipeline. " +
                         "Make sure to specify a proper pipeline in the configuration using the `pipeline` key." +
                         "The `backend` configuration key is NOT supported anymore.")

    provided_properties = set(context.keys())

    for component in pipeline:
        for r in component.requires:
            if r not in provided_properties:
                raise Exception("Failed to validate at component '{}'. Missing property: '{}'".format(
                    component.name, r))
        provided_properties.update(component.provides)


class Component(object):
    """A component is a message processing unit in a pipeline.

    Components are collected sequentially in a pipeline. Each component is called one after another. This holds for
     initialization, training, persisting and loading the components. If a component comes first in a pipeline, its
     methods will be called first.

    E.g. to process an incoming message, the `process` method of each component will be called. During the processing
     (as well as the training, persisting and initialization) components can pass information to other components.
     The information is passed to other components by providing attributes to the so called pipeline context. The
     pipeline context contains all the information of the previous components a component can use to do its own
     processing. For example, a featurizer component can provide features that are used by another component down
     the pipeline to do intent classification."""

    # Name of the component to be used when integrating it in a pipeline. E.g. `[ComponentA, ComponentB]`
    # will be a proper pipeline definition where `ComponentA` is the name of the first component of the pipeline.
    name = ""

    # Defines what attributes the pipeline component will provide when called. The listed attributes
    # should be set by the component on the message object during test and train, e.g.
    # ```message.set("entities", [...])```
    provides = []

    # Which attributes on a message are required by this component. e.g. if requires contains "tokens", than a
    # previous component in the pipeline needs to have "tokens" within the above described `provides` property.
    requires = []

    def __getstate__(self):
        # get all class funcions and variables
        return self.__dict__.copy()

    @classmethod
    def required_packages(cls):
        # type: () -> List[Text]
        """Specify which python packages need to be installed to use this component, e.g. `["spacy", "numpy"]`.

        This list of requirements allows us to fail early during training if a required package is not installed."""
        return []

    @classmethod
    def load(cls, model_dir=None, model_metadata=None, cached_component=None, **kwargs):
        # type: (Text, Metadata, Optional[Component], **Any) -> Component
        """Load this component from file.

        After a component got trained, it will be persisted by calling `persist`. When the pipeline gets loaded again,
         this component needs to be able to restore itself. Components can rely on any context attributes that are
         created by `pipeline_init` calls to components previous to this one."""
        return cached_component if cached_component else cls()

    @classmethod
    def create(cls, config):
        # type: (RasaNLUConfig) -> Component
        """Creates this component (e.g. before a training is started).

        Method can access all configuration parameters."""
        return cls(config)

    def provide_context(self):
        # type: () -> Optional[Dict[Text, Any]]
        """Initialize this component for a new pipeline
        init embedding or tf-idf
        This function will be called before the training is started and before the first message is processed using
        the interpreter. The component gets the opportunity to add information to the context that is passed through
        the pipeline during training and message parsing. Most components do not need to implement this method.
        It's mostly used to initialize framework environments like MITIE and spacy
        (e.g. loading word vectors for the pipeline)."""

        pass

    def train(self, training_data, config, **kwargs):
        # type: (TrainingData, RasaNLUConfig, **Any) -> None
        """Train this component.

        This is the components chance to train itself provided with the training data. The component can rely on
        any context attribute to be present, that gets created by a call to `pipeline_init` of ANY component and
        on any context attributes created by a call to `train` of components previous to this one."""
        pass

    def process(self, message, **kwargs):
        # type: (Message, **Any) -> None
        """Process an incomming message.

        This is the components chance to process an incommng message. The component can rely on
        any context attribute to be present, that gets created by a call to `pipeline_init` of ANY component and
        on any context attributes created by a call to `process` of components previous to this one."""
        pass

    def persist(self, model_dir, **args):
        # type: (Text) -> Optional[Dict[Text, Any]]
        """Persist this component to disk for future loading."""
        pass

    @classmethod
    def cache_key(cls, model_metadata):
        # type: (Metadata) -> Optional[Text]
        """This key is used to cache components.
        if component is singleton, then get the cache key
        If a component is unique to a model it should return None. Otherwise, an instantiation of the
        component will be reused for all models where the metadata creates the same key."""

        return None

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class ComponentBuilder(object):
    """Creates trainers and interpreters based on configurations. Caches components for reuse."""

    def __init__(self, use_cache=True):
        self.use_cache = use_cache
        # Reuse nlp and featurizers where possible to save memory,
        # every component that implements a cache-key will be cached
        self.component_cache = {}

    def __get_cached_component(self, component_name, model_metadata):
        # type: (Text, Metadata) -> Tuple[Optional[Component], Optional[Text]]
        """Load a component from the cache, if it exists. Returns the component, if found, and the cache key."""
        from chi_annotator.algo_factory import registry
        component_class = registry.get_component_class(component_name)
        cache_key = component_class.cache_key(model_metadata)
        if cache_key is not None and self.use_cache and cache_key in self.component_cache:
            return self.component_cache[cache_key], cache_key
        else:
            return None, cache_key

    def __add_to_cache(self, component, cache_key):
        # type: (Component, Text) -> None
        """Add a component to the cache."""

        if cache_key is not None and self.use_cache:
            self.component_cache[cache_key] = component
            logger.info("Added '{}' to component cache. Key '{}'.".format(component.name, cache_key))

    def load_component(self, component_name, model_dir, model_metadata, config = None, **context):
        """
        # TODO config is no use
        """
        # type: (Text, Text, Metadata, **Any) -> Component
        """Tries to retrieve a component from the cache, calls `load` to create a new component."""
        from chi_annotator.algo_factory import registry
        try:
            # reuse cached key
            cached_component, cache_key = self.__get_cached_component(component_name, model_metadata)
            # load component, call component.load() method
            component = registry.load_component_by_name(component_name, model_dir,
                                                        model_metadata, cached_component, **context)
            if not cached_component:
                # If the component wasn't in the cache, let us add it if possible
                self.__add_to_cache(component, cache_key)
            return component
        except MissingArgumentError as e:  # pragma: no cover
            raise Exception("Failed to load component '{}'. {}".format(component_name, e))

    def create_component(self, component_name, config):
        # type: (Text, AnnotatorConfig) -> Component
        """Tries to retrieve a component from the cache, calls `create` to create a new component."""
        from chi_annotator.algo_factory import registry
        try:
            component, cache_key = self.__get_cached_component(component_name, Metadata(config.as_dict(), None))
            if component is None:
                component = registry.create_component_by_name(component_name, config)
                self.__add_to_cache(component, cache_key)
            return component
        except MissingArgumentError as e:  # pragma: no cover
            raise Exception("Failed to create component '{}'. {}".format(component_name, e))
