#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
author: bookerbai
create:2017/11/22
"""
import chi_annotator.task_center.config as config

class TestTokenizer(object):
    """
    test tokenizer components
    """

    def test_char_tokenizer(self):
        from chi_annotator.algo_factory.components import ComponentBuilder
        from chi_annotator.algo_factory.common import Message
        from chi_annotator.task_center.config import AnnotatorConfig
        msg = Message(u"你好，我是一个demo!!!!")
        cb = ComponentBuilder()
        cfg = AnnotatorConfig(config.CLASSIFY_TASK_CONFIG)
        ct = cb.create_component("char_tokenizer", cfg)
        assert ct is not None
        ct.process(msg, **{})
        assert len(msg.get("tokens")) > 0

    def ignor_test_words_jieba_tokenizer(self):
        """
        #TODO: jieba will add later
        test word tokenizer using jieba
        :return:
        """
        from chi_annotator.algo_factory.components import ComponentBuilder
        from chi_annotator.algo_factory.common import Message
        from chi_annotator.task_center.config import AnnotatorConfig
        msg = Message(u"你好，我是一个demo!!!!")
        cb = ComponentBuilder()
        cfg = AnnotatorConfig(config.CLASSIFY_TASK_CONFIG)
        ct = cb.create_component("tokenizer_jieba", cfg)
        assert ct is not None
        ct.process(msg, **{})
        assert len(msg.get("tokens")) > 0
