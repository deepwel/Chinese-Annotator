#!/usr/bin/python  
# -*- coding: utf-8 -*-
"""
author: bookerbai
create:2017/11/22
"""


def test_tokenizer_main():
    from chi_annotator.algo_factory.components import ComponentBuilder
    from chi_annotator.algo_factory.common import Message
    from chi_annotator.task_center.config import AnnotatorConfig
    msg = Message(u"你好，我是一个demo!!!!")
    cb = ComponentBuilder()
    config = AnnotatorConfig()
    ct = cb.create_component("char_tokenizer", config)
    if ct is not None:
        ct.process(msg, **{})
        print(msg.get("tokens"))
