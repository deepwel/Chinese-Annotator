#!/bin/env python
#encoding=utf-8
"""
author burkun
time 
"""
from common import Command, TaskManager
from linkers import DBLinker
import datetime
import pymongo


class BatchTrainCmd(Command):

    def __init__(self, db_linker, task_config):
        super(BatchTrainCmd, self).__init__(db_linker)
        self.liner_config = db_linker.config
        self.task_config = task_config

    def __create_insert(self):
        return {
            "user_uuid" : self.uid,
            "dataset_uuid": self.dataset_id,
            "model_name": self.task_config["model_name"],
            "model_version": self.timestamp,
            "is_full_train": False,
            "status": Command.STATUS_RUNNING,
            "start_timestamp": datetime.datetime(),
            "end_timestamp": None
        }

    def __create_update(self, status):
        return {"model_version": self.timestamp}, {"$set": {"status": status}}

    def exec(self):
        # mark train status in db, self.timestamp = task id
        self.linker.action(DBLinker.INSERT_SINGLE, {"table_name": DBLinker.TRAIN_STATUS_TABLE,
                                                    "item": self.__create_insert()})

        # get batch data
        batch_exec_args = {"condition": self.task_config["condition"],
                           "table_name": DBLinker.ANNO_DATA_TABLE,
                           "sort_limit": self.task_config["sort_limit"]}
        batch_result = self.linker.action(DBLinker.BATCH_FETCH, **batch_exec_args)
        # train process

        # mark train done in db
        condition, item = self.__create_update(Command.STATUS_DONE)
        self.linker.action(DBLinker.UPDATE,
                           {"table_name": DBLinker.TRAIN_STATUS_TABLE, "item": item, "condition": condition})


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

def test_db():
    db_config = {"database_hostname":"localhost", "database_port" : 27017,
                 "database_type": "mongodb", "database_name": "chinese_annotator",
                 "user_name":"anno_admin", "password": "123"}
    linker = DBLinker(db_config)
    task_config = {"condition": {"timestamp": {"$gt": datetime.datetime(2016, 1, 1)}},
                    "sort_limit": ([("timestamp", pymongo.DESCENDING)], 0)}

    tm = TaskManager(4, 100)
    btc = BatchTrainCmd(linker, task_config)
    ret = tm.exec_command(btc)
    if not ret:
        print("can not add task")
    else:
        print("add task done!")

if __name__ == "__main__":
    test_db()