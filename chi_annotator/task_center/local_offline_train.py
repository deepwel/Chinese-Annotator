"""
This is a script for run pipeline in command line, just for test data flow, it will be
 modified in future.

The features of ths script as follow:
1、load config file from args of command line.
2、train pipeline and save model according config.
3、predict is to be added.

You can run shell command below at root dir of project:
   python -m chi_annotator.task_center.local_offline_train -c ./tests/data/test_config.json

You can modify config file dir follow -c argument. you can refer test_config.json for your
own target.

Note:
    It only support load local json format train data for now. you can generate tmp train use
    command as follow in root dir of project:
        python -m tests.utils.txt_to_json

    More data load way will be supported in future.
"""
import argparse
import logging
import os

from chi_annotator.algo_factory.components import ComponentBuilder
from chi_annotator.task_center.data_loader import load_local_data
from chi_annotator.task_center.model import Interpreter
from chi_annotator.task_center.model import Trainer

from chi_annotator.task_center.config import AnnotatorConfig

logger = logging.getLogger(__name__)


def create_argparser():
    parser = argparse.ArgumentParser(
            description='train a custom language parser')
    parser.add_argument('-c', '--config', required=True,
                        help="configuration file")
    return parser


class TrainingException(Exception):
    """Exception wrapping lower level exceptions that may happen while training

      Attributes:
          failed_target_project -- name of the failed project
          message -- explanation of why the request is invalid
      """

    def __init__(self, failed_target_project=None, exception=None):
        self.failed_target_project = failed_target_project
        if exception:
            self.message = exception.args[0]

    def __str__(self):
        return self.message


def init():  # pragma: no cover
    # type: () -> AnnotatorConfig
    """Combines passed arguments to create Annotator config."""

    parser = create_argparser()
    args = parser.parse_args()
    config = AnnotatorConfig(args.config, os.environ, vars(args))
    return config


def do_train_in_worker(config):
    # type: (AnnotatorConfig) -> Text
    """Loads the trainer and the data and runs the training in a worker."""

    try:
        _, _, persisted_path = do_train(config)
        return persisted_path
    except Exception as e:
        raise TrainingException(config.get("project"), e)


def do_train(config,  # type: AnnotatorConfig
             component_builder=None  # type: Optional[ComponentBuilder]
             ):
    # type: (...) -> Tuple[Trainer, Interpreter, Text]
    """Loads the trainer and the data and runs the training of the model."""

    # Ensure we are training a model that we can save in the end
    # WARN: there is still a race condition if a model with the same name is
    # trained in another subprocess
    trainer = Trainer(config, component_builder)
    training_data = load_local_data(config['org_data'])
    interpreter = trainer.train(training_data)
    persisted_path = trainer.persist(config['path'],
                                     config['project'],
                                     config['fixed_model_name'])
    return trainer, interpreter, persisted_path


if __name__ == '__main__':
    config = init()
    log_filename = config["log_file"] if config["log_file"] is not None else "task_center.log"
    logging.basicConfig(level=config['log_level'], filename=log_filename)

    do_train(config)
    logger.info("Finished training")
