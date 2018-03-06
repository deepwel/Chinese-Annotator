import chi_annotator.task_center.config as config
import os

class TestCluster(object):

    def test_kmeans(self):
        from chi_annotator.algo_factory.components import ComponentBuilder
        from chi_annotator.algo_factory.common import Message
        from chi_annotator.task_center.config import AnnotatorConfig
        from chi_annotator.algo_factory.common import TrainingData
        task_config = dict(config.CLASSIFY_TASK_CONFIG)
        dir_name = os.path.dirname(os.path.abspath(__file__))
        task_config["embedding_path"] = dir_name + "/../data/test_embedding/vec.txt"
        task_config["embedding_type"] = "w2v"
        cfg = AnnotatorConfig(task_config)
        pos_msg1 = Message(u"你好，我是一个demo!!!!")
        pos_msg2 = Message(u"你好,你好,你好")
        neg_msg1 = Message(u"如果发现有文件漏提或注释有误")
        neg_msg2 = Message(u"增加一个需要上传的文件")

        train_data = TrainingData([neg_msg1, neg_msg2, pos_msg1, pos_msg2])
        cb = ComponentBuilder()
        char_tokenize = cb.create_component("char_tokenizer", cfg)
        sent_embedding = cb.create_component("sentence_embedding_extractor", cfg)
        svm_classifer = cb.create_component("cluster_sklearn", cfg)
        char_tokenize.train(train_data, cfg)
        sent_embedding.train(train_data, cfg)
        svm_classifer.train(train_data, cfg)
        # test
        test_msg = Message(u"增加一个需要上传的文件")
        char_tokenize.process(test_msg, **{})
        sent_embedding.process(test_msg, **{})
        svm_classifer.process(test_msg, **{})
        assert test_msg.get("cluster_center").get("center") is not None
