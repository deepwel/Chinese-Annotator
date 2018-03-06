import os
import re
from tests.utils.txt_to_json import create_tmp_test_textfile, rm_tmp_file


class TestEmbeddings(object):
    """
    test embedding functions
    """
    def ingor_test_char2vec_standalone(self):
        """
        test char2vec_standalone training
        """
        abs_path = os.path.dirname(os.path.abspath(__file__))
        create_tmp_test_textfile(os.path.join(abs_path, "spam_email_text_1000"))
        os.system("python -m chi_annotator.algo_factory.preprocess.char2vec_standalone -train " +
                  os.path.join(abs_path, "/../data/spam_email_text_1000") +
                  " -output " +
                  os.path.join(abs_path, "/../data/test_vec.txt") +
                  " -size 200 -sample 1e-4 -binary 0 -iter 3")
        assert os.path.isfile(os.path.join(abs_path, "/../data/test_vec.txt")) is not None
        rm_tmp_file(os.path.join(abs_path, "spam_email_text_1000"))
        rm_tmp_file(os.path.join(abs_path, "/../data/test_vec.txt"))

    def ignor_test_senten_embedding_extractor(self):
        from chi_annotator.algo_factory.components import ComponentBuilder
        from chi_annotator.algo_factory.common import Message
        from chi_annotator.task_center.config import AnnotatorConfig
        cfg = AnnotatorConfig()
        msg = Message("你好，我是一个demo!!!!")
        cb = ComponentBuilder()
        char_tokenize = cb.create_component("char_tokenizer", cfg)
        sent_embedding = cb.create_component("sentence_embedding_extractor", cfg)
        char_tokenize.process(msg)
        sent_embedding.process(msg, **{})
        assert msg.get("sentence_embedding").sum() + 7.30032945834 < 1e-6

    def ignor_test_embedding(self):
        from chi_annotator.algo_factory.components import ComponentBuilder
        from chi_annotator.algo_factory.common import Message
        from chi_annotator.task_center.config import AnnotatorConfig
        from chi_annotator.algo_factory.common import TrainingData
        from gensim.models.word2vec import LineSentence
        text_dir = create_tmp_test_textfile("spam_email_text_1000")

        # 将数据放入TrainingData
        with open(text_dir, 'r') as f:
            res = []
            for line in f.readlines():
                line.strip('\n')
                line = Message(re.sub('\s', '', line))
                res.append(line)
        res = TrainingData(res)

        cfg = AnnotatorConfig(filename="tests/data/test_config/test_config_embedding.json")
        cb = ComponentBuilder()

        # char_tokenize, embedding的训练暂时不用用到
        char_tokenize = cb.create_component("char_tokenizer", cfg)
        char_tokenize.train(res, cfg)

        # 加载embedding, 训练模型, 传入数据为LinSentence(data_path)
        embedding = cb.create_component("embedding", cfg)
        embedding.train(LineSentence(text_dir), cfg)
        embedding.persist(cfg.wv_model_path)

        # 加载sent_embedding, 从embedding训练完是model中, 获得sentence_vec
        sent_embedding = cb.create_component("embedding_extractor", cfg)
        msg = Message("你好，我是一个demo!!!!")
        char_tokenize.process(msg)
        sent_embedding.sentence_process(msg, **{})
        assert msg.get("sentence_embedding").sum() != 0

        # 加载base model, 加入新的corpus, 在base_model的基础上进行增量学习
        embedding = embedding.load(model_metadata=cfg)
        embedding.train(LineSentence(text_dir), cfg)
        embedding.persist(cfg.wv_model_path)

        # 增量学习后生成的新model, 进行EmbeddingExtractor测验
        sent_embedding = cb.create_component("embedding_extractor", cfg)
        msg = Message("你好，我是一个demo!!!!")
        char_tokenize.process(msg)
        sent_embedding.sentence_process(msg, **{})
        assert msg.get("sentence_embedding").sum() != 0

        rm_tmp_file("word2vec.model")
        rm_tmp_file("word2vec.model.vector")
        rm_tmp_file("spam_email_text_1000")

