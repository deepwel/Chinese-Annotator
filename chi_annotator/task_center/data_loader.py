import io
import simplejson
import logging

from chi_annotator.algo_factory.common import Message, TrainingData

logger = logging.getLogger(__name__)

# Different supported file formats and their identifier
# TODO


def local_data_schema():

    return {
        "type": "object",
        "properties": {
            "data_set": {
                "type": "array",
                "items": {
                    "text": "string",
                    "label": "string"
                }
            }
        }
    }


def validate_local_data(data):
    # type: (Dict[Text, Any]) -> None
    """Validate rasa training data format to ensure proper training. Raises exception on failure."""
    from jsonschema import validate
    from jsonschema import ValidationError

    try:
        validate(data, local_data_schema())
    except ValidationError as e:
        e.message += \
            ". Failed to validate training data, make sure your data is valid. " + \
            "For more information about the format visit " + \
            "https://github.com/crownpku/Chinese-Annotator"
        raise e


def load_local_data(filename):
    # type: (Text) -> TrainingData
    """Loads training data stored in the rasa NLU data format."""

    with io.open(filename, encoding="utf-8-sig") as f:
        data = simplejson.loads(f.read())
    validate_local_data(data)

    data_set = data.get("data_set", list())

    training_examples = []
    for e in data_set:
        data = e.copy()
        if "text" in data:
            del data["text"]
        training_examples.append(Message(e["text"], data))

    return TrainingData(training_examples)
