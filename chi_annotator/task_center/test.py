#!/bin/env python
#encoding=utf-8
"""
author burkun
time
"""

import datetime, pymongo

from chi_annotator.task_center.common import DBLinker
from chi_annotator.task_center.common import TaskManager
from chi_annotator.task_center.cmds import BatchTrainCmd, BatchPredictCmd, BatchNoDbPredictCmd, StatusCmd
import chi_annotator.task_center.config as config
import time
import os


def abc_test_db_linker():
    db_config = {"database_hostname":"localhost", "database_port" : 27017,
                 "database_type": "mongodb", "database_name": "chinese_annotator",
                 "user_name":"anno_admin", "password": "123"}
    linker = DBLinker(db_config)
    exec_args = {"condition": {"timestamp": {"$gt": datetime.datetime(2016, 1, 1)}},
                 "table_name": DBLinker.ANNO_DATA_TABLE,
                 "sort_limit": ([("timestamp", pymongo.DESCENDING)], 0)}
    res = linker.action(DBLinker.BATCH_FETCH, **exec_args)
    print(res)


def create_cfgs():
    # task config
    task_config = dict(config.CLASSIFY_TASK_CONFIG)
    dir_name = os.path.realpath("../../")
    task_config["embedding_path"] = dir_name + "/tests/data/test_embedding/vec.txt"
    task_config["condition"] = {"timestamp": {"$gt": datetime.datetime(2016, 1, 1)}}
    task_config["sort_limit"] = ([("timestamp", pymongo.DESCENDING)], 0)
    task_config["model_type"] = "classify"
    task_config["model_version"] = time.time()
    task_config["pipeline"] = [
        "char_tokenizer",
        "sentence_embedding_extractor",
        "SVM_classifier"
    ]
    task_config["user_uuid"] = "5a683cadfe61a3fe9262a310"
    task_config["dataset_uuid"] = "5a6840b28831a3e06abbbcc9"
    global_config = dict(config.TASK_CENTER_GLOBAL_CONFIG)
    return global_config, task_config


def create_pred_cfgs():
    # task config
    task_config = dict(config.CLASSIFY_TASK_CONFIG)
    task_config["user_uuid"] = "5a683cadfe61a3fe9262a310"
    task_config["dataset_uuid"] = "5a6840b28831a3e06abbbcc9"
    task_config["model_type"] = "classify"
    global_config = dict(config.TASK_CENTER_GLOBAL_CONFIG)
    return global_config, task_config


def abc_test_batch_train():
    db_config = {"database_hostname":"localhost", "database_port" : 27017,
                 "database_type": "mongodb", "database_name": "chinese_annotator",
                 "user_name": "anno_admin", "password": "123"}
    global_config, task_config = create_cfgs()
    # TM = TaskManager(global_config["max_process_number"], global_cornfig["max_task_in_queue"])
    for idx in range(1):
        _, task_config = create_cfgs()
        merged_config = config.AnnotatorConfig(task_config, global_config)
        btc = BatchTrainCmd(db_config, merged_config)
        btc()
        ret = True
        # for test to comment
        # ret = TM.exec_command(btc)
        if ret:
            print("add task ok!")
        else:
            print("can not add task queue full!")


def abc_test_batch_predict():
    db_config = {"database_hostname":"localhost", "database_port" : 27017,
                 "database_type": "mongodb", "database_name": "chinese_annotator",
                 "user_name":"anno_admin", "password": "123"}
    global_config, task_config = create_pred_cfgs()
    merged_config = config.AnnotatorConfig(task_config, global_config)
    merged_config["model_path"] = merged_config.get_save_path_prefix()

    # TM = TaskManager(global_config["max_process_number"], global_config["max_task_in_queue"])
    btc = BatchPredictCmd(db_config, merged_config)
    preds = btc()
    print(preds)
    # ret = TM.exec_command(btc)
    # print(ret)
    # if ret:
    #     print("add task ok!")
    # else:
    #     print("can not add task queue full!")


def abc_test_batch_nodb_predict():
    db_config = {"database_hostname":"localhost", "database_port" : 27017,
                 "database_type": "mongodb", "database_name": "chinese_annotator",
                 "user_name":"anno_admin", "password": "123"}
    global_config, task_config = create_pred_cfgs()
    task_config["data"] = [{"text": u"荣耀王者"}, {"text": u"我是个垃圾"}]
    merged_config = config.AnnotatorConfig(task_config, global_config)
    merged_config["model_path"] = merged_config.get_save_path_prefix()

    # TM = TaskManager(global_config["max_process_number"], global_config["max_task_in_queue"])
    btc = BatchNoDbPredictCmd(db_config, merged_config)
    preds = btc()
    print(preds)
    # ret = TM.exec_command(btc)
    # print(ret)
    # if ret:
    #     print("add task ok!")
    # else:
    #     print("can not add task queue full!")


def abs_test_status():
    db_config = {"database_hostname":"localhost", "database_port" : 27017,
                 "database_type": "mongodb", "database_name": "chinese_annotator",
                 "user_name":"anno_admin", "password": "123"}
    global_config, task_config = create_pred_cfgs()
    merged_config = config.AnnotatorConfig(task_config, global_config)
    st_cmd = StatusCmd(db_config, merged_config)
    print(st_cmd())

if __name__ == "__main__":
    abs_test_status()

    # abc_test_batch_train()
    # abc_test_batch_train()
    # abc_test_batch_predict()
    # abc_test_batch_nodb_predict()

