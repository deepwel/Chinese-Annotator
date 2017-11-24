from chi_annotator.task_center.config import AnnotatorConfig
from chi_annotator.task_center.data_loader import load_local_data


class TestTrainer(object):
    """
    test Trainer and Interpreter
    """
    def test_load_local_data(self):
        """
        test load local json format data
        :return:
        """
        local_json_file = "chi_annotator/data/files/spam_classify_chi_shuf_top1000.json"
        train_data = load_local_data(local_json_file)
        assert train_data is not None
        assert len(train_data.training_examples) == 1000
        assert "text" not in train_data.training_examples[0].data
        assert "label" in train_data.training_examples[0].data

    def test_load_config(self):
        """
        test load config
        :return:
        """
        config = AnnotatorConfig(\
            filename="chi_annotator/user_instance/examples/classify/spam_email_classify_config.json")
        assert config["name"] == "email_spam_classification"

    def test_load_default_config(self):
        """
        test load default config
        :return:
        """
        config = AnnotatorConfig()
        assert config["config"] == "config.json"
