from utils import ordered
from utils import lazyproperty

class Message(object):
    """basic moudule for data"""
    def __init__(self, text, data=None, output_properties=None, time=None):
        self.text = text
        self.time = time
        self.data = data if data else {}
        self.output_properties = output_properties if output_properties else set()

    def set(self, prop, info, add_to_output=False):
        self.data[prop] = info
        if add_to_output:
            self.output_properties.add(prop)

    def update(self, prop, info, add_to_output=False):
        if prop in self.data:
            if type(info) != type(self.data[prop]):
                return False
            if isinstance(self.data[prop], list):
                self.data[prop].extend(info)
            elif isinstance(self.data[prop], dict) or isinstance(self.data[prop], set):
                self.data[prop].update(info)
            else:
                return False
        else:
            self.data[prop] = info
        if add_to_output:
            self.output_properties.add(prop)
        return True

    def get(self, prop, default=None):
        return self.data.get(prop, default)

    def as_dict(self, only_output_properties=False):
        if only_output_properties:
            d = {key: value for key, value in self.data.items() if key in self.output_properties}
        else:
            d = self.data
        return dict(d, text=self.text)

    def __eq__(self, other):
        if not isinstance(other, Message):
            return False
        else:
            return (other.text, ordered(other.data)) == (self.text, ordered(self.data))

    def __hash__(self):
        return hash((self.text, str(ordered(self.data))))


class TrainingData(object):
    """Holds loaded intent and entity training data."""

    # Validation will ensure and warn if these lower limits are not met
    MIN_EXAMPLES_PER_INTENT = 2
    MIN_EXAMPLES_PER_ENTITY = 2

    def __init__(self, training_examples=None):
        # type: (Optional[List[Message]], Optional[Dict[Text, Text]]) -> None

        self.training_examples = self.sanitice_examples(training_examples) if training_examples else []
        self.validate()

    def sanitice_examples(self, examples):
        # type: (List[Message]) -> List[Message]
        """Makes sure the training data is cleaned, e.q. removes trailing whitespaces from intent annotations."""

        for e in examples:
            if e.get("intent") is not None:
                e.set("intent", e.get("intent").strip())
        return examples

    @lazyproperty
    def intent_examples(self):
        # type: () -> List[Message]
        return [e for e in self.training_examples if e.get("intent") is not None]

    @lazyproperty
    def entity_examples(self):
        # type: () -> List[Message]
        return [e for e in self.training_examples if e.get("entities") is not None]

    @lazyproperty
    def num_entity_examples(self):
        # type: () -> int
        """Returns the number of proper entity training examples (containing at least one annotated entity)."""

        return len([e for e in self.training_examples if len(e.get("entities", [])) > 0])

    @lazyproperty
    def num_intent_examples(self):
        # type: () -> int
        """Returns the number of intent examples."""

        return len(self.intent_examples)

    def as_json(self, **kwargs):
        # type: (**Any) -> str
        """Represent this set of training examples as json adding the passed meta information."""
        pass

    def as_markdown(self, **kwargs):
        # type: (**Any) -> str
        """Represent this set of training examples as markdown adding the passed meta information."""
        pass

    def persist(self, dir_name):
        # type: (Text) -> Dict[Text, Any]
        """Persists this training data to disk and returns necessary information to load it again."""
        pass

    def sorted_entity_examples(self):
        # type: () -> List[Message]
        """Sorts the entity examples by the annotated entity."""

        return sorted([entity for ex in self.entity_examples for entity in ex.get("entities")],
                      key=lambda e: e["entity"])

    def sorted_intent_examples(self):
        # type: () -> List[Message]
        """Sorts the intent examples by the name of the intent."""

        return sorted(self.intent_examples, key=lambda e: e.get("intent"))

    def validate(self):
        # type: () -> None
        """Ensures that the loaded training data is valid, e.g. has a minimum of certain training examples."""
        pass

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

    def __init__(self):
        pass

    def __getstate__(self):
        d = self.__dict__.copy()

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
        return cls()

    def provide_context(self):
        # type: () -> Optional[Dict[Text, Any]]
        """Initialize this component for a new pipeline

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

    def persist(self, model_dir):
        # type: (Text) -> Optional[Dict[Text, Any]]
        """Persist this component to disk for future loading."""
        pass

    @classmethod
    def cache_key(cls, model_metadata):
        # type: (Metadata) -> Optional[Text]
        """This key is used to cache components.

        If a component is unique to a model it should return None. Otherwise, an instantiation of the
        component will be reused for all models where the metadata creates the same key."""
        from rasa_nlu.model import Metadata

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
        from rasa_nlu import registry
        from rasa_nlu.model import Metadata

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

    def load_component(self, component_name, model_dir, model_metadata, **context):
        # type: (Text, Text, Metadata, **Any) -> Component
        """Tries to retrieve a component from the cache, calls `load` to create a new component."""
        from rasa_nlu import registry
        from rasa_nlu.model import Metadata

        try:
            cached_component, cache_key = self.__get_cached_component(component_name, model_metadata)
            component = registry.load_component_by_name(component_name, model_dir,
                                                        model_metadata, cached_component, **context)
            if not cached_component:
                # If the component wasn't in the cache, let us add it if possible
                self.__add_to_cache(component, cache_key)
            return component
        except MissingArgumentError as e:  # pragma: no cover
            raise Exception("Failed to load component '{}'. {}".format(component_name, e))

    def create_component(self, component_name, config):
        # type: (Text, RasaNLUConfig) -> Component
        """Tries to retrieve a component from the cache, calls `create` to create a new component."""
        from rasa_nlu import registry
        from rasa_nlu.model import Metadata

        try:
            component, cache_key = self.__get_cached_component(component_name, Metadata(config.as_dict(), None))
            if component is None:
                component = registry.create_component_by_name(component_name, config)
                self.__add_to_cache(component, cache_key)
            return component
        except MissingArgumentError as e:  # pragma: no cover
            raise Exception("Failed to create component '{}'. {}".format(component_name, e))
