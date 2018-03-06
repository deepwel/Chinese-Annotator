import datetime

from chi_annotator.task_center.common import Command
from chi_annotator.task_center.common import DBLinker
from chi_annotator.algo_factory.common import Message, TrainingData
from chi_annotator.task_center.model import Trainer, Interpreter


class BatchTrainCmd(Command):

    def __init__(self, db_config, task_config):
        super(BatchTrainCmd, self).__init__(db_config)
        self.db_config = db_config
        self.task_config = task_config
        self.uid = self.task_config.get("user_uuid")
        self.dataset_id = self.task_config.get("dataset_uuid")
        if "model_version" in task_config:
            # override timestamp
            self.timestamp = task_config["model_version"]

    def __create_insert(self):
        return {
            "user_uuid": self.uid,
            "dataset_uuid": self.dataset_id,
            "model_type": self.task_config["model_type"],
            "model_version": self.timestamp,
            "is_full_train": False,
            "status": Command.STATUS_RUNNING,
            "start_timestamp": datetime.datetime.now(),
            "end_timestamp": None
        }

    def __create_update(self, status):
        return {"model_version": self.timestamp}, {"status": status, "end_timestamp": datetime.datetime.now()}

    def exec(self):
        # mark train status in db, self.timestamp = task id
        self.linker.action(DBLinker.INSERT_SINGLE, **{"table_name": DBLinker.TRAIN_STATUS_TABLE,
                                                    "item": self.__create_insert()})
        # get batch data
        batch_exec_args = {"condition": self.task_config["condition"],
                           "table_name": DBLinker.ANNO_DATA_TABLE,
                           "sort_limit": self.task_config.get("sort_limit", None)}
        batch_result = self.linker.action(DBLinker.BATCH_FETCH, **batch_exec_args)
        # train process
        self._train_batch(batch_result)
        # mark train done in db
        condition, item = self.__create_update(Command.STATUS_DONE)
        self.linker.action(DBLinker.UPDATE,
                           **{"table_name": DBLinker.TRAIN_STATUS_TABLE, "item": item, "condition": condition})

    def _train_batch(self, batch_result):
        # from result to train_data, create train data
        msg = []
        for item in batch_result:
            msg.append(Message(item["text"], {"label": item["label"]}))
        train_data = TrainingData(msg)
        # create interpreter
        trainer = Trainer(self.task_config)
        trainer.train(train_data)
        # save model meta for config
        trainer.persist(self.task_config.get_save_path_prefix())
        return True


class BatchNoDbPredictCmd(Command):
    """
    predict from json data not from db
    """
    def __init__(self, db_config, task_config):
        super(BatchNoDbPredictCmd, self).__init__(db_config)
        self.db_config = db_config
        self.task_config = task_config
        self.uid = self.task_config.get("user_uuid")
        self.dataset_id = self.task_config.get("dataset_uuid")
        if "model_version" in task_config:
            self.timestamp = task_config["model_version"]

    def exec(self):
        # from result to train_data, create train data
        # load interpreter # todo model can be load from cache later.
        filter_condition = {'user_uuid': self.uid,
                            "dataset_uuid": self.dataset_id,
                            "model_type": self.task_config["model_type"],
                            "status": Command.STATUS_DONE}

        batch_exec_args = {"condition": filter_condition,
                           "table_name": DBLinker.TRAIN_STATUS_TABLE,
                           "sort_limit": ([("end_timestamp", -1)], 1)}
        status_result = self.linker.action(DBLinker.BATCH_FETCH, **batch_exec_args)
        # print(status_result)
        if len(status_result) < 1:
            print("no model trained now, please train model first or wait model train done.")
            return None
        model_version = str(status_result[0]["model_version"])
        print("now model version is : ", model_version)
        # get newest model version according user_id, dataset_id, and model_type.
        # only need task config to generate saved path
        # Interpreter can load model meta by itself
        interpreter = Interpreter.load(self.task_config.get_save_path_prefix(), model_version)
        preds = []
        items = self.task_config["data"]
        for item in items:
            pred = interpreter.parse(item["text"])
            preds.append(pred)
        return preds


class BatchPredictCmd(Command):
    """
    batch predicted command, this command using certain ${model_version} predict ${batch_num} samples, which
     have not been labeled.
    """
    def __init__(self, db_config, task_config):
        super(BatchPredictCmd, self).__init__(db_config)
        self.db_config = db_config
        self.task_config = task_config
        self.uid = self.task_config.get("user_uuid")
        self.dataset_id = self.task_config.get("dataset_uuid")
        if "model_version" in task_config:
            # override timestamp
            self.timestamp = task_config["model_version"]

    def exec(self):
        # get batch data
        batch_exec_args = {"condition": self.task_config["condition"],
                           "table_name": DBLinker.RAW_DATA_TABLE,
                           "limit": self.task_config.get("batch_num", 100)}
        batch_result = self.linker.action(DBLinker.LIMIT_BATCH_FETCH, **batch_exec_args)
        # predict
        return self._predict_batch(batch_result)

    def _predict_batch(self, batch_result):
        # from result to train_data, create train data
        # load interpreter # todo model can be load from cache later.
        filter_condition = {'user_uuid': self.uid,
                            "dataset_uuid": self.dataset_id,
                            "model_type": self.task_config["model_type"],
                            "status": Command.STATUS_DONE}

        batch_exec_args = {"condition": filter_condition,
                           "table_name": DBLinker.TRAIN_STATUS_TABLE,
                           "sort_limit": ([("end_timestamp", -1)], 1)}
        status_result = self.linker.action(DBLinker.BATCH_FETCH, **batch_exec_args)
        # print(status_result)
        if len(status_result) < 1:
            print("no model trained now, please train model first or wait model train done.")
            return None
        model_version = str(status_result[0]["model_version"])
        print("now model version is : ", model_version)
        # get newest model version according user_id, dataset_id, and model_type.

        interpreter = Interpreter.load(self.task_config.get_save_path_prefix(), model_version)
        preds = []
        for item in batch_result:
            pred = interpreter.parse(item["text"])
            preds.append(pred)
        return preds


class StatusCmd(Command):
    """
    query task status by user id && dataset id && task type
    """
    def __init__(self, db_config, task_config):
        super(StatusCmd, self).__init__(db_config)
        self.db_config = db_config
        self.task_config = task_config
        self.uid = self.task_config.get("user_uuid")
        self.dataset_id = self.task_config.get("dataset_uuid")
        if "model_version" in task_config:
            # override timestamp
            self.timestamp = task_config["model_version"]

    def exec(self):
        filter_condition = {'user_uuid': self.uid,
                            "dataset_uuid": self.dataset_id,
                            "model_type": self.task_config["model_type"]}
        batch_exec_args = {"condition": filter_condition,
                           "table_name": DBLinker.TRAIN_STATUS_TABLE,
                           "sort_limit": ([("start_timestamp", -1)], 1)}
        batch_result = self.linker.action(DBLinker.BATCH_FETCH, **batch_exec_args)
        # predict
        if len(batch_result) == 1:
            return batch_result[0]["status"], batch_result[0]["end_timestamp"]
        else:
            return "not found!", None
