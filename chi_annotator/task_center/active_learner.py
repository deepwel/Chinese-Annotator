import logging

from chi_annotator.algo_factory.common import TrainingData, Message
from chi_annotator.task_center.common import DBManager
from chi_annotator.task_center.model import Trainer, Interpreter

logger = logging.getLogger(__name__)


class ActiveLearner(object):
    """
    implement of active learning core, this class is mainly the wrapper of trainer and interpreter.
    you can use ActiveLearner as follow:
        active_leaner = ActiveLearner(config)
        data_to_train = get_data_from_user_label()
        active_leaner.train(data_to_train)

        data_to_rank = get_data_from_db()
        low_confidence_data = active_leaner.process_batch(data_to_rank)
    """

    def __init__(self, config):
        """
        init of ActiveLearner
        """
        self.config = config
        self.trainer = Trainer(config)
        self.train_data = TrainingData([])
        self.new_data_count = 0
        self.batch_num = config.get("batch_num", 20)
        self.db = DBManager(config)
        self.interpreter = None

    def train(self, data_set):
        """
        train data set
        :param data_set: format as [{"id": 1, "text": "我是测试", "label": "spam"}, .....]
        :return:
        """
        config = self.config

        examples = []
        for e in data_set:
            data = e.copy()
            if "text" in data:
                del data["text"]
            examples.append(Message(e["text"], data))
        train_data = TrainingData(examples)

        self.interpreter = self.trainer.train(train_data)
        # overwrite save model TODO
        self.trainer.persist(config['path'],
                        config['project'],
                        config['fixed_model_name'])

    def process_one(self, id):
        """
        predict one according id
        :param id:
        :return:
        """
        data = self.db.get_row({"id": id})
        predict = self.interpreter.parse(data["text"])
        return predict

    def process_batch(self, ids):
        """
        process batch text according ids
        :param ids:
        :return:
        """
        datas = self.db.get_row_by_ids(ids)
        predicted_results = []
        for unlabeled_data in datas:
            predict = self.interpreter.parse(unlabeled_data["text"])
            if predict:
                unlabeled_data.update(predict)
            predicted_results.append(unlabeled_data)
        return predicted_results

    def process_texts(self, texts):
        """
        process texts
        :param texts: format as [{"id": 1, "text": "我是测试"}, {"id": 2, "text": "我是测试2"}, ...]
        :return: format as [{'id':-, 'text':-, 'classifylabel':-, 'classifylabel_ranking':-}, ...]
        """
        if self.interpreter is None:
            logger.warning("model has not been trained, nothing will be predicted.")
            return []
        predicted_results = []
        for unlabeled_data in texts:
            predict = self.interpreter.parse(unlabeled_data["text"])
            if predict:
                unlabeled_data.update(predict)
            predicted_results.append(unlabeled_data)
        return predicted_results
