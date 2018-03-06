import io
import shutil

import simplejson

from chi_annotator.algo_factory.common import TrainingData, Message
from chi_annotator.task_center.active_learner import ActiveLearner
from chi_annotator.task_center.config import AnnotatorConfig
from chi_annotator.task_center.data_loader import load_local_data, validate_local_data
from chi_annotator.task_center.model import Trainer
from tests.utils.txt_to_json import rm_tmp_file, create_tmp_test_jsonfile


class TestOnlineTraining(object):
    @classmethod
    def setup_class(cls):
        """ setup any state specific to the execution of the given class (which
        usually contains tests).
        """
        # create test data for test case
        create_tmp_test_jsonfile("test_data.json")

    @classmethod
    def teardown_class(cls):
        """ teardown any state that was previously setup with a call to
        setup_class.
        """
        # remove tmp files and dirs created in test case
        test_config = "tests/data/test_config/test_config.json"
        config = AnnotatorConfig(test_config)

        rm_tmp_file("test_data.json")
        shutil.rmtree(config['path'], ignore_errors=True)

    def ignor_test_online_training(self):
        """
        test online training.
        """
        test_config = "tests/data/test_config/test_config.json"
        config = AnnotatorConfig(test_config)
        # init trainer first
        trainer = Trainer(config)

        # load all data for test, in actual data should get from user label
        with io.open(config["org_data"], encoding="utf-8-sig") as f:
            data = simplejson.loads(f.read())
        validate_local_data(data)

        data_set = data.get("data_set", list())

        # faker user labeled data, user has labeled 50 texts.
        faker_user_labeled_data = data_set[:50]
        # 950 text to predict and rank
        unlabeled_data = data_set[50:]

        # now test online training
        examples = []
        for e in faker_user_labeled_data:
            data = e.copy()
            if "text" in data:
                del data["text"]
            examples.append(Message(e["text"], data))

        new_labeled_data = TrainingData(examples)

        # full amount train and persist model
        interpreter = trainer.train(new_labeled_data)
        trainer.persist(config['path'],
                        config['project'],
                        config['fixed_model_name'])

        # predict unlabeled dataset and ranking
        predicted_results = []
        for unlabeled_data in unlabeled_data:
            predict = interpreter.parse(unlabeled_data["text"])
            predicted_results.append(predict)

        # sort predict result
        # predicted result format as
        # {
        #   'classifylabel': {'name': 'spam', 'confidence': 0.5701943777626447},
        #   'classifylabel_ranking': [{'name': 'spam', 'confidence': 0.5701943777626447},
        #                             {'name': 'notspam', 'confidence': 0.42980562223735524}],
        #   'text': '我是一个垃圾邮件'
        # }
        confidence_threshold = config["confidence_threshold"]
        ranking_candidates = [text for text in predicted_results \
                              if text.get("classifylabel").get("confidence") < confidence_threshold]
        for candidate in ranking_candidates:
            assert candidate.get("classifylabel").get("confidence") < confidence_threshold

        # TODO sort ranking_candidates data and push to user.

    def ignor_test_active_leaner_process_texts(self):
        """
        test active_leaner process raw texts
        :return:
        """
        test_config = "tests/data/test_config/test_config.json"
        config = AnnotatorConfig(test_config)
        # init trainer first

        # load all data for test, in actual data should get from user label
        with io.open(config["org_data"], encoding="utf-8-sig") as f:
            data = simplejson.loads(f.read())
        validate_local_data(data)

        data_set = data.get("data_set", list())

        # faker user labeled data, user has labeled 50 texts.
        faker_user_labeled_data = data_set[:50]

        # text to be predict
        texts = [{"uuid": 1, "text": "我是测试"}, {"uuid": 2, "text": "我是测试2"}]

        active_learner = ActiveLearner(config)
        active_learner.train(faker_user_labeled_data)
        predicted = active_learner.process_texts(texts)
        assert len(predicted) == 2
        assert "classifylabel" in predicted[0]
