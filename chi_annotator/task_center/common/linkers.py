#!/bin/env python
#encoding=utf-8
"""
author burkun
time 
"""
from common import Linker, DBManager
import pymongo


class DBLinker(Linker):

    BATCH_FETCH = 1
    SINGLE_FETCH = 2
    INSERT_BATCH = 3
    INSERT_SINGLE = 4
    UPDATE = 5

    RAW_DATA_TABLE = "annotation_raw_data"
    ANNO_DATA_TABLE = "annotation_data"
    USER_TABLE = "user"
    DATASET_TABlE = "dataset"
    TRAIN_STATUS_TABLE = "train_status"

    def __init__(self, config):
        self.db_manager = DBManager(config)
        self.config = config

    def open(self):
        return True

    def close(self):
        self.db_manager.close()

    def action(self, action_type, **args):
        if action_type == DBLinker.BATCH_FETCH:
            sort_limit = args.get("sort_limit", ([("timestamp", pymongo.DESCENDING)], 0))
            return self.db_manager.get_rows(args["condition"], args["table_name"], sort_limit)
        elif action_type == DBLinker.SINGLE_FETCH:
            return self.db_manager.get_row(args["condition"], args["table_name"])
        elif action_type == DBLinker.INSERT_BATCH:
            return self.db_manager.insert_rows(args["items"], args["table_name"])
        elif action_type == DBLinker.INSERT_SINGLE:
            return self.db_manager.insert_row(args["item"], args["table_name"])
        elif action_type == DBLinker.UPDATE:
            return self.db_manager.update_rows(args["condition"], args["item"], args["table_name"])
        else:
            return None
