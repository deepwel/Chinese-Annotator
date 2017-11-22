#!/usr/bin/python  
# -*- coding: utf-8 -*-
"""
author: bookerbai
create:2017/11/22
"""

if __name__ == "__main__":
    from chi_annotator.algo_factory.components import ComponentBuilder
    from chi_annotator.algo_factory.common import Message
    from chi_annotator.config import AnnotatorConfig
    cb = ComponentBuilder()
    msg = Message(u"你好，我是一个demo!!!!")
    cb = ComponentBuilder()
    config = AnnotatorConfig()
    ct = cb.create_component("char_tokenizer", config)
    if ct is not None:
        ct.process(msg, **{})
        print msg.get("tokens")
