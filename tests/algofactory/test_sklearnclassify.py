#test relation extration
#author shimin

from chi_annotator.algo_factory.components import ComponentBuilder
from chi_annotator.algo_factory.common import Message
from chi_annotator.task_center.config import AnnotatorConfig
from chi_annotator.algo_factory.common import TrainingData
import chi_annotator.task_center.config as config
import os


class TestClassify(object):
    pos_msg1 = Message(u"你好，我是一个demo!!!!", {"label": "good"})
    pos_msg2 = Message(u"你好,你好,你好", {"label": "good"})
    pos_msg3 = Message(u"好的呀，不错", {"label": "good"})
    neg_msg1 = Message(u"如果发现有文件漏提或注释有误", {"label": "bad"})
    neg_msg2 = Message(u"增加一个需要上传的文件", {"label": "bad"})
    neg_msg3 = Message(u"有一个上传的文件", {"label": "bad"})

    def test_svm_classify(self):
        task_config = dict(config.CLASSIFY_TASK_CONFIG)
        dir_name = os.path.dirname(os.path.abspath(__file__))
        task_config["embedding_path"] = dir_name + "/../data/test_embedding/vec.txt"
        task_config["embedding_type"] = "w2v"
        cfg = AnnotatorConfig(task_config)
        train_data = TrainingData([self.neg_msg1, self.neg_msg2, self.pos_msg1, self.pos_msg2])
        cb = ComponentBuilder()
        char_tokenize = cb.create_component("char_tokenizer", cfg)
        sent_embedding = cb.create_component("sentence_embedding_extractor", cfg)
        svm_classifer = cb.create_component("SVM_classifier", cfg)
        char_tokenize.train(train_data, cfg)
        sent_embedding.train(train_data, cfg)
        svm_classifer.train(train_data, cfg)
        # test
        test_msg = Message(u"增加一个需要上传的文件")
        char_tokenize.process(test_msg, **{})
        sent_embedding.process(test_msg, **{})
        svm_classifer.process(test_msg, **{})

        assert test_msg.get("classifylabel").get("name") == "bad"

    def test_sgd_classify(self):
        task_config = dict(config.CLASSIFY_TASK_CONFIG)
        dir_name = os.path.dirname(os.path.abspath(__file__))
        task_config["embedding_path"] = dir_name + "/../data/test_embedding/vec.txt"
        task_config["embedding_type"] = "w2v"
        cfg = AnnotatorConfig(task_config)
        train_data = TrainingData([self.neg_msg1, self.neg_msg2, self.pos_msg1, self.pos_msg2])
        cb = ComponentBuilder()
        char_tokenize = cb.create_component("char_tokenizer", cfg)
        sent_embedding = cb.create_component("sentence_embedding_extractor", cfg)
        SGD_Classifier = cb.create_component("SGD_Classifier", cfg)
        char_tokenize.train(train_data, cfg)
        sent_embedding.train(train_data, cfg)
        SGD_Classifier.train(train_data, cfg)
        # test
        test_msg = Message(u"增加一个需要上传的文件")
        char_tokenize.process(test_msg, **{})
        sent_embedding.process(test_msg, **{})
        SGD_Classifier.process(test_msg, **{})

        assert test_msg.get("classifylabel").get("name") == "bad"
    def test_knn_classify(self):
        task_config = dict(config.CLASSIFY_TASK_CONFIG)
        dir_name = os.path.dirname(os.path.abspath(__file__))
        task_config["embedding_path"] = dir_name + "/../data/test_embedding/vec.txt"
        task_config["embedding_type"] = "w2v"
        cfg = AnnotatorConfig(task_config)
        train_data = TrainingData([self.neg_msg1, self.neg_msg2, self.neg_msg3, self.pos_msg1, self.pos_msg2, self.pos_msg3])
        cb = ComponentBuilder()
        char_tokenize = cb.create_component("char_tokenizer", cfg)
        sent_embedding = cb.create_component("sentence_embedding_extractor", cfg)
        Knn_Classifier = cb.create_component("Knn_Classifier", cfg)
        char_tokenize.train(train_data, cfg)
        sent_embedding.train(train_data, cfg)
        Knn_Classifier.train(train_data, cfg)
        # test
        test_msg = Message(u"增加一个需要上传的文件")
        char_tokenize.process(test_msg, **{})
        sent_embedding.process(test_msg, **{})
        Knn_Classifier.process(test_msg, **{})

        assert test_msg.get("classifylabel").get("name") == "bad"

    def test_randomforest_classify(self):
        task_config = dict(config.CLASSIFY_TASK_CONFIG)
        dir_name = os.path.dirname(os.path.abspath(__file__))
        task_config["embedding_path"] = dir_name + "/../data/test_embedding/vec.txt"
        task_config["embedding_type"] = "w2v"
        cfg = AnnotatorConfig(task_config)
        train_data = TrainingData([self.neg_msg1, self.neg_msg2, self.pos_msg1, self.pos_msg2])
        cb = ComponentBuilder()
        char_tokenize = cb.create_component("char_tokenizer", cfg)
        sent_embedding = cb.create_component("sentence_embedding_extractor", cfg)
        RandomForest_Classifier = cb.create_component("RandomForest_Classifier", cfg)
        char_tokenize.train(train_data, cfg)
        sent_embedding.train(train_data, cfg)
        RandomForest_Classifier.train(train_data, cfg)
        # test
        test_msg = Message(u"增加一个需要上传的文件")
        char_tokenize.process(test_msg, **{})
        sent_embedding.process(test_msg, **{})
        RandomForest_Classifier.process(test_msg, **{})

        assert test_msg.get("classifylabel").get("name") == "bad"
    def test_adaboost_classify(self):
        task_config = dict(config.CLASSIFY_TASK_CONFIG)
        dir_name = os.path.dirname(os.path.abspath(__file__))
        task_config["embedding_path"] = dir_name + "/../data/test_embedding/vec.txt"
        task_config["embedding_type"] = "w2v"
        cfg = AnnotatorConfig(task_config)
        train_data = TrainingData([self.neg_msg1, self.neg_msg2, self.pos_msg1, self.pos_msg2])
        cb = ComponentBuilder()
        char_tokenize = cb.create_component("char_tokenizer", cfg)
        sent_embedding = cb.create_component("sentence_embedding_extractor", cfg)
        AdaBoost_Classifier = cb.create_component("AdaBoost_Classifier", cfg)
        char_tokenize.train(train_data, cfg)
        sent_embedding.train(train_data, cfg)
        AdaBoost_Classifier.train(train_data, cfg)
        # test
        test_msg = Message(u"增加一个需要上传的文件")
        char_tokenize.process(test_msg, **{})
        sent_embedding.process(test_msg, **{})
        AdaBoost_Classifier.process(test_msg, **{})

        assert test_msg.get("classifylabel").get("name") == "bad"
