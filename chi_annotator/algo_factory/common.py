#! /usr/bin/env python
# -*- coding: utf8 -*-

from chi_annotator.algo_factory.utils import ordered
from chi_annotator.algo_factory.utils import lazyproperty
from chi_annotator.algo_factory.utils import list_to_str
from itertools import groupby

import os
import json
import io
import datetime
import logging
import warnings

import chi_annotator

logger = logging.getLogger(__name__)


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return json.JSONEncoder.default(self, obj)


class InvalidProjectError(Exception):
    """Raised when a model failed to load.

    Attributes:
        message -- explanation of why the model is invalid
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class MissingArgumentError(Exception):
    """Raised when a args missing.

    Attributes:
        message -- explanation of why the model is invalid
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class Metadata(object):
    """
    Captures all information about a model to load and prepare it.
    Interpreter or Components will load  model according metadata file which saved by Trainer.
    """

    @staticmethod
    def load(model_meta_path, timestamp):
        # type: (Text) -> 'Metadata'
        """Loads the metadata from a models directory."""
        try:
            metadata_file = os.path.join(model_meta_path, str(timestamp) + "_meta.json")
            with io.open(metadata_file, encoding="utf-8") as f:
                data = json.loads(f.read())
            return Metadata(data, model_meta_path)
        except Exception as e:
            abspath = os.path.abspath(model_meta_path)
            raise InvalidProjectError("Failed to load model metadata "
                                      "from '{}'. {}".format(abspath, e))

    def __init__(self, metadata, model_meta_path):
        # type: (Dict[Text, Any], Optional[Text]) -> None
        self.metadata = metadata
        self.model_meta_path = model_meta_path

    def get(self, property_name, default=None):
        return self.metadata.get(property_name, default)

    @property
    def language(self):
        # type: () -> Optional[Text]
        """Language of the underlying model"""
        return self.get('language')

    @property
    def pipeline(self):
        # type: () -> List[Text]
        """Names of the processing pipeline elements."""

        return self.get('pipeline', [])

    def persist(self, model_meta_path=None):
        # type: (Text) -> None
        """Persists the metadata of a model to a given directory."""
        metadata = self.metadata.as_dict()
        metadata.update({
            "trained_at": datetime.datetime.now().strftime('%Y%m%d-%H%M%S'),
            "algo_version": chi_annotator.algo_factory.__version__,
        })
        if model_meta_path is None:
            model_meta_path = self.model_meta_path
        metadata_file = os.path.join(model_meta_path, str(self.get("model_version")) + "_meta.json")
        with io.open(metadata_file, 'w') as f:
            f.write(json.dumps(metadata, ensure_ascii=False, indent=4, cls=DateTimeEncoder))


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
        """更新message的参数，如果message对应的key已经存在，那么在key->value后面调用extend"""
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
            d = {key: value for key, value in list(self.data.items()) if key in self.output_properties}
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
    MIN_EXAMPLES_PER_CLASSIFY = 2
    MIN_EXAMPLES_PER_ENTITY = 2

    def __init__(self, training_examples=None):
        # type: (Optional[List[Message]], Optional[Dict[Text, Text]]) -> None
        self.training_examples = training_examples
        self.validate()

    @lazyproperty
    def classify_examples(self):
        # type: () -> List[Message]
        return [e for e in self.training_examples if e.get("label") is not None]

    @lazyproperty
    def cluster_examples(self):
        # type: () -> List[Message]
        return [e for e in self.training_examples]

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
    def num_classify_examples(self):
        # type: () -> int
        """Returns the number of intent examples."""
        return len([e for e in self.training_examples if e.get("label") is not None])

    def example_iter(self):
        """
        iterator for all samples
        :return: message
        """
        for example in self.training_examples:
            yield example

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

    def sorted_classify_examples(self):
        # type: () -> List[Message]
        """Sorts the classify examples by the name of the intent."""

        return sorted(self.classify_examples, key=lambda e: e.get("label"))

    def validate(self):
        # type: () -> None
        """Ensures that the loaded training data is valid, e.g. has a minimum of certain training examples."""
        logger.debug("Validating training data...")
        examples = self.sorted_classify_examples()
        different_intents = []
        for intent, group in groupby(examples, lambda e: e.get("label")):
            size = len(list(group))
            different_intents.append(intent)
            if size < self.MIN_EXAMPLES_PER_CLASSIFY:
                template = "classify '{}' has only {} training examples! minimum is {}, training may fail."
                warnings.warn(template.format(intent, size, self.MIN_EXAMPLES_PER_CLASSIFY))

        different_entities = []
        for entity, group in groupby(self.sorted_entity_examples(), lambda e: e["entity"]):
            size = len(list(group))
            different_entities.append(entity)
            if size < self.MIN_EXAMPLES_PER_ENTITY:
                template = "Entity '{}' has only {} training examples! minimum is {}, training may fail."
                warnings.warn(template.format(entity, size, self.MIN_EXAMPLES_PER_ENTITY))
        if len(different_intents) > 0:
            logger.info("Training data stats: \n" +
                        "\t- classify examples: {} ({} distinct intents)\n".format(
                                self.num_classify_examples, len(different_intents)) +
                        "\t- found class: {}\n".format(list_to_str(different_intents)))
        if len(different_entities) > 0:
            logger.info("Training data stats: \n" +
                        "\t- entity examples: {} ({} distinct entities)\n".format(
                                self.num_entity_examples, len(different_entities)) +
                        "\t- found entities: {}\n".format(list_to_str(different_entities)))
