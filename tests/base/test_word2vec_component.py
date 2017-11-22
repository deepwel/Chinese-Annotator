# -*- coding:utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import numpy
import pytest
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from chi_annotator.task_center.utils.word2vec_utils import Word2VecNLP


class TestWord2Vec:
    """
    test Word2Vec component
    """
    def test_create(self):
        """
        test create
        :return:
        """
        config = {
            "word2vec_file": "../data/model_ai.vec",
            "word2vec_format": "text"
            }
        assert Word2VecNLP.create(config=config) is not None

    def test_load(self):
        """
        test load
        :return:
        """
        metadata = {
            "word2vec_file": "../data/model_ai.vec",
            "word2vec_format": "text"
            }
        assert Word2VecNLP.load(model_dir=None, model_metadata=metadata, cached_component=None) is not None

    def test_bin_format(self):
        """
        test create
        :return:
        """
        config = {
            "word2vec_file": "../data/GoogleNews-vectors-negative300.bin",
            "word2vec_format": "bin"
            }
        assert Word2VecNLP.create(config=config) is not None

    def test_illegal_format(self):
        """
        test create
        :return:
        """
        config = {
            "word2vec_file": "../data/model_ai.vec",
            "word2vec_format": "bin"
            }
        with pytest.raises(UnicodeDecodeError):  # test exception
            Word2VecNLP.create(config=config)

    def test_word2vec_feature_extractor(self):
        """
        test word2vec can be use
        :return:
        """
        metadata = {
            "word2vec_file": "../data/model_ai.vec",
            "word2vec_format": "text"
        }
        word2vec = Word2VecNLP.load(model_dir=None, model_metadata=metadata, cached_component=None)
        assert word2vec is not None
        assert type(word2vec.extractor.similarity(u'的', u'六')) is numpy.float64