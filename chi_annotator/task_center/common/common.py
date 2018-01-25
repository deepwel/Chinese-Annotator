#!/bin/env python
#encoding=utf-8
"""
author booker
simple task manager
"""
from concurrent.futures import ProcessPoolExecutor
import time
import multiprocessing
import functools
import pymongo


class Linker(object):
    def open(self):
        """
        open database
        :return: true or false
        """
        raise NotImplementedError()

    def close(self):
        """
        close database
        :return: true or false
        """
        raise NotImplementedError()

    def action(self, action_type, **args):
        """
        do some action for database
        eg: get database; train a model
        :param action_type:
        :param args:
        :return: dataset or not
        """
        raise NotImplementedError()


class Command(object):
    STATUS_RUNNING = "running"
    STATUS_ERROR = "error"
    STATUS_DONE = "done"

    def __init__(self, linker, user_id=None, dataset_id=None):
        self.linker = linker
        self.timestamp = time.time()
        self.uid = user_id
        self.dataset_id = dataset_id

    def __call__(self, *args, **kwargs):
        return self.exec()

    def exec(self):
        raise NotImplementedError()


class TaskManager:

    def __init__(self, process_num, max_task_in_queue=100):
        self.process_num = process_num
        self.max_task_in_queue = max_task_in_queue
        self.pool = ProcessPoolExecutor(max_workers=process_num)
        self.task_map = {}
        self.lock = multiprocessing.Lock()

    def exec_command(self, command):
        """ simple process
        :param command: command
        :return: true or false, if sent success return True else return False
        """
        self.lock.acquire()
        if len(self.task_map) < self.max_task_in_queue:
            self.task_map[command.timestamp] = self.pool.submit(command)
            self.task_map[command.timestamp].add_done_callback(functools.partial(self.task_done, command))
            self.lock.release()
            return True
        else:
            self.lock.release()
            return False

    def task_done(self, command, future_obj):
        self.lock.acquire()
        self.task_map.pop(command.timestamp)
        self.lock.release()

    #def shutdown(self):
    #    self.pool.shutdown()

    def is_all_done(self):
        self.lock.acquire()
        for key in self.task_map:
            if self.task_map[key].running():
                self.lock.release()
                return False
        self.lock.release()
        return True


class DBManager(object):
    """
    manage database connections, TODO, if ORM needed?
    """

    def __init__(self, config):
        self.hostname = config.get("database_hostname", "127.0.0.1")
        self.port = config.get("database_port", 27017)
        self.type = config.get("database_type", "mongodb")
        self.database = config.get("database_name", "chinese_annotator")
        self.user_name = config.get("user_name", "anno_admin")
        self.pwd = config.get("password", "123")
        con_url = 'mongodb://' + self.user_name + ':' + self.pwd + '@' + self.hostname \
                  + ':' + str(self.port) + "/" + self.database
        self.client = pymongo.MongoClient(con_url)

    def insert_row(self, item, table, database_name=None):
        """
        insert one row into database
        :param item: json format data
        :param database_name:
        :param table:
        :return: row_num or row id
        """
        if database_name is None:
            database_name = self.database

        if self.type == "mongodb":
            if self.client[database_name][table].find_one(item) is None:
                xid = self.client[database_name][table].insert_one(item).inserted_id
                return True
        # TODO catch exception
        return False

    def insert_rows(self, item, table, database_name=None):
        """
        insert one row into database
        :param item: list of json format data
        :param database_name:
        :param table:
        :return: row_num or row id
        """
        if database_name is None:
            database_name = self.database

        if self.type == "mongodb":
            xids = self.client[database_name][table].insert(item).inserted_id
            return True
        # TODO catch exception
        return False

    def update_rows(self, condition, new_value, table, database_name=None):
        """
        insert one row into database
        :param new_value:
        :param condition:
        :param database_name:
        :param table:
        :return: row_num or row id
        """
        if database_name is None:
            database_name = self.database

        if self.type == "mongodb":
            xids = self.client[database_name][table].update_many(condition, {"$set": new_value})
            if xids.matched_count > 0:
                return True
        return False

    def get_rows(self, conditions, table, sort_limit=([("timestamp", pymongo.DESCENDING)], 0), database_name=None):
        """
        get rows according conditions
        :param table:
        :param database_name:
        :param conditions: json format data
        :param sort_limit sort = -1, limit =
        :return:
        """
        res = []
        if database_name is None:
            database_name = self.database

        if self.type == "mongodb":
            result = self.client[database_name][table].find(conditions).sort(sort_limit[0]).limit(sort_limit[1])
            for item in result:
                res.append(item)
        return res

    def get_row_by_ids(self, ids, table, col_name="uuid", database_name=None):
        """
        get rows according conditions
        :param col_name:
        :param table:
        :param database_name:
        :param conditions: json format data
        :return:
        """
        res = []
        if database_name is None:
            database_name = self.database

        if self.type == "mongodb":
            result = self.client[database_name][table].find({col_name: {"$in": ids}})
            for item in result:
                res.append(item)
        return res

    def get_row(self, condition, table, database_name=None):
        """
        get row according conditions
        :param table:
        :param database_name:
        :param conditions: json format data
        :return:
        """
        if database_name is None:
            database_name = self.database

        if self.type == "mongodb":
            result = self.client[database_name][table].find_one(condition)
            return result
        return None

    def close(self):
        """
        close connection from database
        :return:
        """
        if self.type == "mongodb":
            self.client.close()

    def drop_database(self, database=None):
        """
        drop dataset for test now.
        :param database:
        :return:
        """
        if database is None:
            database = self.database
        if self.type == "mongodb":
            self.client.drop_database(database)


