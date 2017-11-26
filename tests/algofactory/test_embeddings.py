import os
from tests.utils.txt_to_json import create_tmp_test_textfile, rm_tmp_file

class TestEmbeddings(object):
    """
    test embedding functions
    """
    def test_char2vec_standalone(self):
        """
        test char2vec_standalone training
        """
        create_tmp_test_textfile("spam_email_text_1000")
        os.system("python -m chi_annotator.algo_factory.preprocess.char2vec_standalone -train tests/data/spam_email_text_1000 -output tests/data/test_vec.txt -size 200 -sample 1e-4 -binary 0 -iter 3")
        os.path.isfile("tests/data/test_vec.txt")
        rm_tmp_file("spam_email_text_1000")
        rm_tmp_file("test_vec.txt")

    def test_senten_embedding_extractor(self):
        from chi_annotator.algo_factory.components import ComponentBuilder
        from chi_annotator.algo_factory.common import Message
        from chi_annotator.config import AnnotatorConfig
        cfg = AnnotatorConfig()
        msg = Message("你好，我是一个demo!!!!")
        cb = ComponentBuilder()
        char_tokenize = cb.create_component("char_tokenizer", cfg)
        sent_embedding = cb.create_component("sentence_embedding_extractor", cfg)
        char_tokenize.process(msg)
        sent_embedding.process(msg, **{})
        if msg.get("sentence_embedding").sum() + 7.30032945834 < 1e-6:
            return True
        return False
