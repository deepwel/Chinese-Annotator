import datetime

from chi_annotator.task_center.common import Command
from chi_annotator.task_center.common import DBLinker


class BatchTrainCmd(Command):

    def __init__(self, db_config, task_config, user_id = None, dataset_id = None):
        super(BatchTrainCmd, self).__init__(db_config, user_id, dataset_id)
        self.db_config = db_config
        self.task_config = task_config

    def __create_insert(self):
        return {
            "user_uuid" : self.uid,
            "dataset_uuid": self.dataset_id,
            "model_name": self.task_config["model_name"],
            "model_version": self.timestamp,
            "is_full_train": False,
            "status": Command.STATUS_RUNNING,
            "start_timestamp": datetime.datetime.now(),
            "end_timestamp": None
        }

    def __create_update(self, status):
        return {"model_version": self.timestamp}, {"status": status}

    def exec(self):
        # mark train status in db, self.timestamp = task id
        self.linker.action(DBLinker.INSERT_SINGLE, **{"table_name": DBLinker.TRAIN_STATUS_TABLE,
                                                    "item": self.__create_insert()})
        # get batch data
        batch_exec_args = {"condition": self.task_config["condition"],
                           "table_name": DBLinker.ANNO_DATA_TABLE,
                           "sort_limit": self.task_config["sort_limit"]}
        batch_result = self.linker.action(DBLinker.BATCH_FETCH, **batch_exec_args)
        # train process
        ret = self._train_batch(batch_result)
        # mark train done in db
        condition, item = self.__create_update(Command.STATUS_DONE)
        self.linker.action(DBLinker.UPDATE,
                           **{"table_name": DBLinker.TRAIN_STATUS_TABLE, "item": item, "condition": condition})

    def _train_batch(self, batch_result):
        # from result to train_data
        # step1 create train_data
        # create interpreter
        # save model
        return True
