#!/bin/env python
#encoding=utf-8
"""
author burkun
time 
"""
from common import Linker, Command, TaskManager
from linkers import DBLinker
import time
import random


class Printer(Linker):
    WRITE_666 = 1
    WRITE_233 = 2
    WRITE_ooo = 3

    def open(self):
        pass

    def close(self):
        pass

    def action(self, action_type, **args):
        if action_type == Printer.WRITE_666:
            print("666")
            time.sleep(1)
        elif action_type == Printer.WRITE_233:
            print("233")
            time.sleep(0.5)
        elif action_type == Printer.WRITE_ooo:
            print("ooo")
            time.sleep(0.5)
        else:
            raise Exception("can not find action type!")
        return True


class Command233(Command):

    def __init__(self, printer):
        super(Command233, self).__init__(printer)

    def exec(self):
        return self.linker.action(Printer.WRITE_233)


class Commandooo(Command):

    def __init__(self, printer):
        super(Commandooo, self).__init__(printer)

    def exec(self):
        return self.linker.action(Printer.WRITE_ooo)


class Command666(Command):

    def __init__(self, printer):
        super(Command666, self).__init__(printer)

    def exec(self):
        return self.linker.action(Printer.WRITE_666)


def create_command(printer):
    ret = random.randint(0, 2)
    if ret == 0:
        return Commandooo(printer)
    elif ret == 1:
        return Command233(printer)
    elif ret == 2:
        return Command666(printer)
    else:
        return Command666(printer)

def test_task_manager():
    tm = TaskManager(4, max_task_in_queue=100)
    printer = Printer()
    for idx in range(20):
        command = create_command(printer)
        tm.exec_command(command)
    time.sleep(10)
    print(tm.is_all_done())
    print(len(tm.task_map))

##------------------------------------------------------

class BatchTrainCmd(Command):

    def __init__(self, linker, condition):
        super(BatchTrainCmd, self).__init__(linker)
        self.condition = condition
        self.config = linker.config

    def exec(self):
        # get batch data
        condition = {"condition": self.condition, "tabel_name" :DBLinker.RAW_DATA_TABLE}
        result = self.linker.action(DBLinker.BATCH_FETCH, condition)
        # mark train status in db, self.timestamp = task id
        insert_data = {"item": {"user_uuid": self.uid, "dataset_uuid": self.dataset_id }}
        self.linker.action(DBLinker.INSERT_SINGLE, )
        # train process

        # mark train done in db


def test_db():
    config = {"database_hostname":"localhost", "database_port" : 27017, "database_type": "mongodb", "database_name": "chinese_annotator"}
    linker = DBLinker(config)
    tm = TaskManager(4, 100)
    btc = BatchTrainCmd(linker, {})
    ret = tm.exec_command(btc)
    if not ret:
        print("can not add task")
    else:
        print("add task done!")

if __name__ == "__main__":
    test_task_manager()