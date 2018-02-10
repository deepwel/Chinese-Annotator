#!/bin/env python
#encoding=utf-8
"""
author burkun
time
"""

import datetime, pymongo
from glob import glob

from chi_annotator.task_center.common import DBLinker
from chi_annotator.task_center.common import TaskManager
from chi_annotator.task_center.cmds import BatchTrainCmd, BatchPredictCmd
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
    dir_name = os.path.realpath("../../")
    task_config["embedding_path"] = dir_name + "/tests/data/test_embedding/vec.txt"
    task_config["condition"] = {"labeled": False}
    task_config["batch_num"] = 5
    task_config["model_type"] = "classify"
    # task_config["model_version"] = "1517845125.5345774"
    task_config["pipeline"] = [
        "char_tokenizer",
        "sentence_embedding_extractor",
        "SVM_classifier"
    ]
    task_config["user_uuid"] = "5a683cadfe61a3fe9262a310"
    task_config["dataset_uuid"] = "5a6840b28831a3e06abbbcc9"
    global_config = dict(config.TASK_CENTER_GLOBAL_CONFIG)
    return global_config, task_config


def abc_test_batch_train():
    db_config = {"database_hostname":"localhost", "database_port" : 27017,
                 "database_type": "mongodb", "database_name": "chinese_annotator",
                 "user_name":"anno_admin", "password": "123"}
    global_config, task_config = create_cfgs()
    # merged_config = config.AnnotatorConfig(task_config, global_config)
    TM = TaskManager(global_config["max_process_number"], global_config["max_task_in_queue"])
    for idx in range(1):
        _, task_config = create_cfgs()
        merged_config = config.AnnotatorConfig(task_config, global_config)
        btc = BatchTrainCmd(db_config, merged_config)
        ret = TM.exec_command(btc)
        if ret:
            print("add task ok!")
        else:
            print("can not add task queue full!")


def test_batch_predict():
    db_config = {"database_hostname":"localhost", "database_port" : 27017,
                 "database_type": "mongodb", "database_name": "chinese_annotator",
                 "user_name":"anno_admin", "password": "123"}
    global_config, task_config = create_pred_cfgs()
    merged_config = config.AnnotatorConfig(task_config, global_config)
    merged_config["model_path"] = merged_config.get_save_path_prefix()
    # get newest model version
    # model_lists = sorted(glob(merged_config["model_path"] + "/*"), reverse=True)
    # merged_config["model_version"] = model_lists[0].split("/")[-1].split("_")[0]

    TM = TaskManager(global_config["max_process_number"], global_config["max_task_in_queue"])
    btc = BatchPredictCmd(db_config, merged_config)
    ret = TM.exec_command(btc)
    if ret:
        print("add task ok!")
    else:
        print("can not add task queue full!")

if __name__ == "__main__":
    # test_batch_train()
    # abc_test_batch_train()
    test_batch_predict()

