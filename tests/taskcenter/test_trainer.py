# -*- coding: utf-8 -*-
import json
import os
import io
import shutil

import pytest

from chi_annotator.algo_factory.common import TrainingData
from chi_annotator.task_center.config import AnnotatorConfig
from chi_annotator.task_center.data_loader import load_local_data
from chi_annotator.task_center.model import Interpreter
from chi_annotator.task_center.model import Trainer
from tests.utils.txt_to_json import create_tmp_test_jsonfile, rm_tmp_file


class TestTrainer(object):

    @classmethod
    def setup_class(cls):
        """ setup any state specific to the execution of the given class (which
        usually contains tests).
        """
        pass

    @classmethod
    def teardown_class(cls):
        """ teardown any state that was previously setup with a call to
        setup_class.
        """
        pass

    """
    test Trainer and Interpreter
    """
    def ignore_test_load_local_data(self):
        """
        test load local json format data
        :return:
        """
        tmp_path = create_tmp_test_jsonfile("tmp.json")
        train_data = load_local_data(tmp_path)
        rm_tmp_file("tmp.json")
        assert train_data is not None
        assert len(train_data.training_examples) == 1000
        assert "text" not in train_data.training_examples[0].data
        assert "label" in train_data.training_examples[0].data

    def ignore_test_load_config(self):
        """
        test load config
        :return:
        """
        config = AnnotatorConfig(\
            filename="chi_annotator/user_instance/examples/classify/spam_email_classify_config.json")
        assert config["name"] == "email_spam_classification"

    def ignor_test_load_default_config(self):
        """
        test load default config
        :return:
        """
        config = AnnotatorConfig()
        assert config["config"] == "config.json"

    def ignore_test_trainer_init(self):
        """
        test trainer
        :return:
        """
        test_config = "tests/data/test_config/test_config.json"
        config = AnnotatorConfig(test_config)

        trainer = Trainer(config)
        assert len(trainer.pipeline) > 0

    def ignore_test_pipeline_flow(self):
        """
        test trainer's train func for pipeline
        :return:
        """
        test_config = "tests/data/test_config/test_config.json"
        config = AnnotatorConfig(test_config)

        trainer = Trainer(config)
        assert len(trainer.pipeline) > 0
        # create tmp train set
        tmp_path = create_tmp_test_jsonfile("tmp.json")
        train_data = load_local_data(tmp_path)
        # rm tmp train set
        rm_tmp_file("tmp.json")

        interpreter = trainer.train(train_data)
        assert interpreter is not None
        out1 = interpreter.parse(("点连接拿红包啦"))

        # test persist and load
        persisted_path = trainer.persist(config['path'],
                                         config['project'],
                                         config['fixed_model_name'])

        interpreter_loaded = Interpreter.load(persisted_path, config)
        out2 = interpreter_loaded.parse("点连接拿红包啦")
        assert out1.get("classifylabel").get("name") == out2.get("classifylabel").get("name")

        # remove tmp models
        shutil.rmtree(config['path'], ignore_errors=True)

    def ignore_test_trainer_persist(self):
        """
        test pipeline persist, metadata will be saved
        :return:
        """
        test_config = "tests/data/test_config/test_config.json"
        config = AnnotatorConfig(test_config)

        trainer = Trainer(config)
        assert len(trainer.pipeline) > 0
        # char_tokenizer component should been created
        assert trainer.pipeline[0] is not None
        # create tmp train set
        tmp_path = create_tmp_test_jsonfile("tmp.json")
        train_data = load_local_data(tmp_path)
        # rm tmp train set
        rm_tmp_file("tmp.json")

        trainer.train(train_data)
        persisted_path = trainer.persist(config['path'],
                                         config['project'],
                                         config['fixed_model_name'])
        # load persisted metadata
        metadata_path = os.path.join(persisted_path, 'metadata.json')
        with io.open(metadata_path) as f:
            metadata = json.load(f)
        assert 'trained_at' in metadata
        # rm tmp files and dirs
        shutil.rmtree(config['path'], ignore_errors=False)

    def ignore_test_train_model_empty_pipeline(self):
        """
        train model with no component
        :return:
        """
        test_config = "tests/data/test_config/test_config.json"
        config = AnnotatorConfig(test_config)
        config['pipeline'] = []

        tmp_path = create_tmp_test_jsonfile("tmp.json")
        train_data = load_local_data(tmp_path)
        rm_tmp_file("tmp.json")

        with pytest.raises(ValueError):
            trainer = Trainer(config)
            trainer.train(train_data)

    def ignore_test_handles_pipeline_with_non_existing_component(self):
        """
        handle no exist component in pipeline
        :return:
        """
        test_config = "tests/data/test_config/test_config.json"
        config = AnnotatorConfig(test_config)
        config['pipeline'].append("unknown_component")

        tmp_path = create_tmp_test_jsonfile("tmp.json")
        train_data = load_local_data(tmp_path)
        rm_tmp_file("tmp.json")

        with pytest.raises(Exception) as execinfo:
            trainer = Trainer(config)
            trainer.train(train_data)
        assert "Failed to find component" in str(execinfo.value)

    def ignore_test_load_and_persist_without_train(self):
        """
        test save and load model without train
        :return:
        """
        test_config = "tests/data/test_config/test_config.json"
        config = AnnotatorConfig(test_config)

        trainer = Trainer(config)
        assert len(trainer.pipeline) > 0
        # create tmp train set
        tmp_path = create_tmp_test_jsonfile("tmp.json")
        train_data = load_local_data(tmp_path)
        # rm tmp train set
        rm_tmp_file("tmp.json")

        # interpreter = trainer.train(train_data)
        # test persist and load
        persisted_path = trainer.persist(config['path'],
                                         config['project'],
                                         config['fixed_model_name'])

        interpreter_loaded = Interpreter.load(persisted_path, config)
        assert interpreter_loaded.pipeline
        assert interpreter_loaded.parse("hello") is not None
        assert interpreter_loaded.parse("Hello today is Monday, again!") is not None
        # remove tmp models
        shutil.rmtree(config['path'], ignore_errors=False)

    def ignore_test_train_with_empty_data(self):
        """
        test train with empty train data
        :return:
        """
        test_config = "tests/data/test_config/test_config.json"
        config = AnnotatorConfig(test_config)

        trainer = Trainer(config)
        assert len(trainer.pipeline) > 0
        # create tmp train set

        train_data = TrainingData([])
        # rm tmp train set

        trainer.train(train_data)
        # test persist and load
        persisted_path = trainer.persist(config['path'],
                                         config['project'],
                                         config['fixed_model_name'])

        interpreter_loaded = Interpreter.load(persisted_path, config)
        
        assert interpreter_loaded.pipeline
        assert interpreter_loaded.parse("hello") is not None
        assert interpreter_loaded.parse("Hello today is Monday, again!") is not None
        
        # remove tmp models
        shutil.rmtree(config['path'], ignore_errors=False)



