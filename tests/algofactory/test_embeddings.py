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

