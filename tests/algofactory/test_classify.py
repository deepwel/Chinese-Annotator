#test relation extration

class TestClassify(object):
    def test_svm_classify(self):
        from chi_annotator.algo_factory.components import ComponentBuilder
        from chi_annotator.algo_factory.common import Message
        from chi_annotator.config import AnnotatorConfig
        from chi_annotator.algo_factory.common import TrainingData
        cfg = AnnotatorConfig()
        pos_msg1 = Message("你好，我是一个demo!!!!", {"classify": "good"})
        pos_msg2 = Message("你好,你好,你好", {"classify": "good"})
        neg_msg1 = Message(u"如果发现有文件漏提或注释有误", {"classify": "bad"})
        neg_msg2 = Message(u"增加一个需要上传的文件", {"classify": "bad"})

        train_data = TrainingData([neg_msg1, neg_msg2, pos_msg1, pos_msg2])
        cb = ComponentBuilder()
        char_tokenize = cb.create_component("char_tokenizer", cfg)
        sent_embedding = cb.create_component("sentence_embedding_extractor", cfg)
        svm_classifer = cb.create_component("classifier_sklearn", cfg)
        char_tokenize.train(train_data, cfg)
        sent_embedding.train(train_data, cfg)
        svm_classifer.train(train_data, cfg)
        # test
        test_msg = Message(u"增加一个需要上传的文件")
        char_tokenize.process(test_msg, **{})
        sent_embedding.process(test_msg, **{})
        svm_classifer.process(test_msg, **{})

        if test_msg.get("classifylabel").get("name") == "bad":
            return True
        return False
