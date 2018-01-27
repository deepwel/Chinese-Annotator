#!/bin/env python
#encoding=utf-8
"""
author burkun
time
"""

import datetime, pymongo
import simplejson
from chi_annotator.task_center.common import DBLinker
from chi_annotator.task_center.common import TaskManager
from chi_annotator.task_center.cmds import BatchTrainCmd


def test_db_linker():
    db_config = {"database_hostname":"localhost", "database_port" : 27017,
                 "database_type": "mongodb", "database_name": "chinese_annotator",
                 "user_name":"anno_admin", "password": "123"}
    linker = DBLinker(db_config)
    exec_args = {"condition": {"timestamp": {"$gt": datetime.datetime(2016, 1, 1)}},
                 "table_name": DBLinker.ANNO_DATA_TABLE,
                 "sort_limit": ([("timestamp", pymongo.DESCENDING)], 0)}
    res = linker.action(DBLinker.BATCH_FETCH, **exec_args)
    print(res)

def test_batch_train():
    db_config = {"database_hostname":"localhost", "database_port" : 27017,
                 "database_type": "mongodb", "database_name": "chinese_annotator",
                 "user_name":"anno_admin", "password": "123"}
    task_config = {"condition": {"timestamp": {"$gt": datetime.datetime(2016, 1, 1)}},
                    "sort_limit": ([("timestamp", pymongo.DESCENDING)], 0),
                   "model_name": "classifer_task"}
    # merge default config
    # task_config.update(simplejson.load(open("./tests/data/test_config/test_task_config.json")))
    # btc = BatchTrainCmd(db_config, task_config)
    # btc.exec()
    tm = TaskManager(4, 100)
    for idx in range(10):
        btc = BatchTrainCmd(db_config, task_config, "123", "123")
        ret = tm.exec_command(btc)
        if not ret:
            print("can not add task")
        else:
            print("add task done!")

if __name__ == "__main__":
    test_batch_train()
