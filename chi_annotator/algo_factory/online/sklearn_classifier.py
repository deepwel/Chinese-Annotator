#Dummy example for using sklearn for classification

import logging
from builtins import zip
import os
import io
import numpy as np

from chi_annotator.algo_factory.components import Component

logger = logging.getLogger(__name__)

MAX_CV_FOLDS = 5
CLASSIFY_RANKING_LENGTH = 10


class SVMClassifier(Component):
    """Text classifier using the sklearn framework"""

    name = "SVM_classifier"

    provides = ["classifylabel", "classifylabel_ranking"]

    requires = ["sentence_embedding"]

    def __init__(self, config=None, clf=None, le=None):
        # type: (sklearn.model_selection.GridSearchCV, sklearn.preprocessing.LabelEncoder) -> None
        """Construct a new classifier using the sklearn framework."""
        from sklearn.preprocessing import LabelEncoder

        if le is not None:
            self.le = le
        else:
            self.le = LabelEncoder()
        self.clf = clf

    @classmethod
    def required_packages(cls):
        # type: () -> List[Text]
        return ["numpy", "sklearn"]

    def transform_labels_str2num(self, labels):
        # type: (List[Text]) -> np.ndarray
        """Transforms a list of strings into numeric label representation.
        :param labels: List of labels to convert to numeric representation"""

        return self.le.fit_transform(labels)

    def transform_labels_num2str(self, y):
        # type: (np.ndarray) -> np.ndarray
        """Transforms a list of strings into numeric label representation.
        :param y: List of labels to convert to numeric representation"""

        return self.le.inverse_transform(y)

    def train(self, training_data, config, **kwargs):
        # type: (TrainingData, RasaNLUConfig, **Any) -> None
        """Train the classifier on a data set.
        :param num_threads: number of threads used during training time"""
        from sklearn.model_selection import GridSearchCV
        from sklearn.svm import SVC
        labels = [e.get("label") for e in training_data.classify_examples]
        if len(set(labels)) < 2:
            logger.warning("Can not train an classifier. Need at least 2 different classes. " +
                        "Skipping training of classifier.")
        else:
            y = self.transform_labels_str2num(labels)
            # TODO fix it, in future sentence will replaced by "features"
            X = np.stack([example.get("sentence_embedding") for example in training_data.classify_examples])
            sklearn_config = config.get("classifier_sklearn")
            C = sklearn_config.get("C", [1, 2, 5, 10, 20, 100])
            kernel = sklearn_config.get("kernel", "linear")
            # dirty str fix because sklearn is expecting str not instance of basestr...
            tuned_parameters = [{"C": C, "kernel": [str(kernel)]}]
            cv_splits = max(2, min(MAX_CV_FOLDS, np.min(np.bincount(y)) // 5))  # aim for 5 examples in each fold

            self.clf = GridSearchCV(SVC(C=1, probability=True, class_weight='balanced'),
                                    param_grid=tuned_parameters, n_jobs=config["num_threads"],
                                    cv=cv_splits, scoring='f1_weighted', verbose=1)
            self.clf.fit(X, y)

    def process(self, message, **kwargs):
        # type: (Message, **Any) -> None
        """Returns the most likely label and its probability for the input text."""

        if not self.clf:
            # component is either not trained or didn't receive enough training data
            label = None
            label_ranking = []
        else:
            X = message.get("sentence_embedding").reshape(1, -1)
            label_ids, probabilities = self.predict(X)
            labels = self.transform_labels_num2str(label_ids)
            # `predict` returns a matrix as it is supposed
            # to work for multiple examples as well, hence we need to flatten
            labels, probabilities = labels.flatten(), probabilities.flatten()

            if labels.size > 0 and probabilities.size > 0:
                ranking = list(zip(list(labels), list(probabilities)))[:CLASSIFY_RANKING_LENGTH]
                label = {"name": labels[0], "confidence": probabilities[0]}
                label_ranking = [{"name": label_name, "confidence": score} for label_name, score in ranking]
            else:
                label = {"name": None, "confidence": 0.0}
                label_ranking = []

        message.set("classifylabel", label, add_to_output=True)
        message.set("classifylabel_ranking", label_ranking, add_to_output=True)

    def predict_prob(self, X):
        # type: (np.ndarray) -> np.ndarray
        """Given a bow vector of an input text, predict the classify label. Returns probabilities for all labels.
        :param X: bow of input text
        :return: vector of probabilities containing one entry for each label"""

        return self.clf.predict_proba(X)

    def predict(self, X):
        # type: (np.ndarray) -> Tuple[np.ndarray, np.ndarray]
        """Given a bow vector of an input text, predict most probable label. Returns only the most likely label.
        :param X: bow of input text
        :return: tuple of first, the most probable label and second, its probability"""

        pred_result = self.predict_prob(X)
        # sort the probabilities retrieving the indices of the elements in sorted order
        sorted_indices = np.fliplr(np.argsort(pred_result, axis=1))
        return sorted_indices, pred_result[:, sorted_indices]

    @classmethod
    def load(cls, model_dir=None, model_metadata=None, cached_component=None, **kwargs):
        # type: (Text, Metadata, Optional[Component], **Any) -> SklearnClassifier
        import cloudpickle

        if model_dir and model_metadata.get("classifier_sklearn"):
            classifier_file = os.path.join(model_dir, model_metadata.get("classifier_sklearn"))
            with io.open(classifier_file, 'rb') as f:  # pragma: no test
                return cloudpickle.load(f, encoding="latin-1")
        else:
            return SklearnClassifier()

    def persist(self, model_dir):
        # type: (Text) -> Dict[Text, Any]
        """Persist this model into the passed directory. Returns the metadata necessary to load the model again."""

        import cloudpickle

        classifier_file = os.path.join(model_dir, "label_classifier.pkl")
        with io.open(classifier_file, 'wb') as f:
            cloudpickle.dump(self, f)

        return {
            "classifier_sklearn": "label_classifier.pkl"
        }
        
class SGDClassifier(Component):
    """Text classifier using the sklearn framework"""

    name = "SGD_Classifier"

    provides = ["classifylabel", "classifylabel_ranking"]

    requires = ["sentence_embedding"]

    def __init__(self, config=None, clf=None, le=None):
        # type: (sklearn.model_selection.GridSearchCV, sklearn.preprocessing.LabelEncoder) -> None
        """Construct a new classifier using the sklearn framework."""
        from sklearn.preprocessing import LabelEncoder

        if le is not None:
            self.le = le
        else:
            self.le = LabelEncoder()
        self.clf = clf

    @classmethod
    def required_packages(cls):
        # type: () -> List[Text]
        return ["numpy", "sklearn"]

    def transform_labels_str2num(self, labels):
        # type: (List[Text]) -> np.ndarray
        """Transforms a list of strings into numeric label representation.
        :param labels: List of labels to convert to numeric representation"""

        return self.le.fit_transform(labels)

    def transform_labels_num2str(self, y):
        # type: (np.ndarray) -> np.ndarray
        """Transforms a list of strings into numeric label representation.
        :param y: List of labels to convert to numeric representation"""

        return self.le.inverse_transform(y)

    def train(self, training_data, config, **kwargs):
        # type: (TrainingData, RasaNLUConfig, **Any) -> None
        """Train the classifier on a data set.
        :param num_threads: number of threads used during training time"""
        from sklearn.model_selection import GridSearchCV
        from sklearn.linear_model import SGDClassifier
        labels = [e.get("label") for e in training_data.classify_examples]
        if len(set(labels)) < 2:
            logger.warning("Can not train an classifier. Need at least 2 different classes. " +
                        "Skipping training of classifier.")
        else:
            y = self.transform_labels_str2num(labels)
            # TODO fix it, in future sentence will replaced by "features"
            X = np.stack([example.get("sentence_embedding") for example in training_data.classify_examples])
            self.clf=SGDClassifier(loss="log")
#            sklearn_config = config.get("classifier_sklearn")
#            C = sklearn_config.get("C", [1, 2, 5, 10, 20, 100])
#            kernel = sklearn_config.get("kernel", "linear")
#            # dirty str fix because sklearn is expecting str not instance of basestr...
#            tuned_parameters = [{"C": C, "kernel": [str(kernel)]}]
#            cv_splits = max(2, min(MAX_CV_FOLDS, np.min(np.bincount(y)) // 5))  # aim for 5 examples in each fold
#
#            self.clf = GridSearchCV(SVC(C=1, probability=True, class_weight='balanced'),
#                                    param_grid=tuned_parameters, n_jobs=config["num_threads"],
#                                    cv=cv_splits, scoring='f1_weighted', verbose=1)
            self.clf.fit(X, y)

    def process(self, message, **kwargs):
        # type: (Message, **Any) -> None
        """Returns the most likely label and its probability for the input text."""

        if not self.clf:
            # component is either not trained or didn't receive enough training data
            label = None
            label_ranking = []
        else:
            X = message.get("sentence_embedding").reshape(1, -1)
            label_ids, probabilities = self.predict(X)
            labels = self.transform_labels_num2str(label_ids)
            # `predict` returns a matrix as it is supposed
            # to work for multiple examples as well, hence we need to flatten
            labels, probabilities = labels.flatten(), probabilities.flatten()

            if labels.size > 0 and probabilities.size > 0:
                ranking = list(zip(list(labels), list(probabilities)))[:CLASSIFY_RANKING_LENGTH]
                label = {"name": labels[0], "confidence": probabilities[0]}
                label_ranking = [{"name": label_name, "confidence": score} for label_name, score in ranking]
            else:
                label = {"name": None, "confidence": 0.0}
                label_ranking = []

        message.set("classifylabel", label, add_to_output=True)
        message.set("classifylabel_ranking", label_ranking, add_to_output=True)

    def predict_prob(self, X):
        # type: (np.ndarray) -> np.ndarray
        """Given a bow vector of an input text, predict the classify label. Returns probabilities for all labels.
        :param X: bow of input text
        :return: vector of probabilities containing one entry for each label"""

        return self.clf.predict_proba(X)

    def predict(self, X):
        # type: (np.ndarray) -> Tuple[np.ndarray, np.ndarray]
        """Given a bow vector of an input text, predict most probable label. Returns only the most likely label.
        :param X: bow of input text
        :return: tuple of first, the most probable label and second, its probability"""

        pred_result = self.predict_prob(X)
        # sort the probabilities retrieving the indices of the elements in sorted order
        sorted_indices = np.fliplr(np.argsort(pred_result, axis=1))
        return sorted_indices, pred_result[:, sorted_indices]

    @classmethod
    def load(cls, model_dir=None, model_metadata=None, cached_component=None, **kwargs):
        # type: (Text, Metadata, Optional[Component], **Any) -> SklearnClassifier
        import cloudpickle

        if model_dir and model_metadata.get("classifier_sklearn"):
            classifier_file = os.path.join(model_dir, model_metadata.get("classifier_sklearn"))
            with io.open(classifier_file, 'rb') as f:  # pragma: no test
                return cloudpickle.load(f, encoding="latin-1")
        else:
            return SklearnClassifier()

    def persist(self, model_dir):
        # type: (Text) -> Dict[Text, Any]
        """Persist this model into the passed directory. Returns the metadata necessary to load the model again."""

        import cloudpickle

        classifier_file = os.path.join(model_dir, "label_classifier.pkl")
        with io.open(classifier_file, 'wb') as f:
            cloudpickle.dump(self, f)

        return {
            "classifier_sklearn": "label_classifier.pkl"
        }
class KnnClassifier(Component):
    """Text classifier using the sklearn framework"""

    name = "Knn_Classifier"

    provides = ["classifylabel", "classifylabel_ranking"]

    requires = ["sentence_embedding"]

    def __init__(self, config=None, clf=None, le=None):
        # type: (sklearn.model_selection.GridSearchCV, sklearn.preprocessing.LabelEncoder) -> None
        """Construct a new classifier using the sklearn framework."""
        from sklearn.preprocessing import LabelEncoder

        if le is not None:
            self.le = le
        else:
            self.le = LabelEncoder()
        self.clf = clf

    @classmethod
    def required_packages(cls):
        # type: () -> List[Text]
        return ["numpy", "sklearn"]

    def transform_labels_str2num(self, labels):
        # type: (List[Text]) -> np.ndarray
        """Transforms a list of strings into numeric label representation.
        :param labels: List of labels to convert to numeric representation"""

        return self.le.fit_transform(labels)

    def transform_labels_num2str(self, y):
        # type: (np.ndarray) -> np.ndarray
        """Transforms a list of strings into numeric label representation.
        :param y: List of labels to convert to numeric representation"""

        return self.le.inverse_transform(y)

    def train(self, training_data, config, **kwargs):
        # type: (TrainingData, RasaNLUConfig, **Any) -> None
        """Train the classifier on a data set.
        :param num_threads: number of threads used during training time"""
        from sklearn.model_selection import GridSearchCV
        from sklearn.neighbors import KNeighborsClassifier
        labels = [e.get("label") for e in training_data.classify_examples]
        if len(set(labels)) < 2:
            logger.warning("Can not train an classifier. Need at least 2 different classes. " +
                        "Skipping training of classifier.")
        else:
            y = self.transform_labels_str2num(labels)
            # TODO fix it, in future sentence will replaced by "features"
            X = np.stack([example.get("sentence_embedding") for example in training_data.classify_examples])
            self.clf=KNeighborsClassifier()
#            sklearn_config = config.get("classifier_sklearn")
#            C = sklearn_config.get("C", [1, 2, 5, 10, 20, 100])
#            kernel = sklearn_config.get("kernel", "linear")
#            # dirty str fix because sklearn is expecting str not instance of basestr...
#            tuned_parameters = [{"C": C, "kernel": [str(kernel)]}]
#            cv_splits = max(2, min(MAX_CV_FOLDS, np.min(np.bincount(y)) // 5))  # aim for 5 examples in each fold
#
#            self.clf = GridSearchCV(SVC(C=1, probability=True, class_weight='balanced'),
#                                    param_grid=tuned_parameters, n_jobs=config["num_threads"],
#                                    cv=cv_splits, scoring='f1_weighted', verbose=1)
            self.clf.fit(X, y)

    def process(self, message, **kwargs):
        # type: (Message, **Any) -> None
        """Returns the most likely label and its probability for the input text."""

        if not self.clf:
            # component is either not trained or didn't receive enough training data
            label = None
            label_ranking = []
        else:
            X = message.get("sentence_embedding").reshape(1, -1)
            label_ids, probabilities = self.predict(X)
            labels = self.transform_labels_num2str(label_ids)
            # `predict` returns a matrix as it is supposed
            # to work for multiple examples as well, hence we need to flatten
            labels, probabilities = labels.flatten(), probabilities.flatten()

            if labels.size > 0 and probabilities.size > 0:
                ranking = list(zip(list(labels), list(probabilities)))[:CLASSIFY_RANKING_LENGTH]
                label = {"name": labels[0], "confidence": probabilities[0]}
                label_ranking = [{"name": label_name, "confidence": score} for label_name, score in ranking]
            else:
                label = {"name": None, "confidence": 0.0}
                label_ranking = []

        message.set("classifylabel", label, add_to_output=True)
        message.set("classifylabel_ranking", label_ranking, add_to_output=True)

    def predict_prob(self, X):
        # type: (np.ndarray) -> np.ndarray
        """Given a bow vector of an input text, predict the classify label. Returns probabilities for all labels.
        :param X: bow of input text
        :return: vector of probabilities containing one entry for each label"""

        return self.clf.predict_proba(X)

    def predict(self, X):
        # type: (np.ndarray) -> Tuple[np.ndarray, np.ndarray]
        """Given a bow vector of an input text, predict most probable label. Returns only the most likely label.
        :param X: bow of input text
        :return: tuple of first, the most probable label and second, its probability"""

        pred_result = self.predict_prob(X)
        # sort the probabilities retrieving the indices of the elements in sorted order
        sorted_indices = np.fliplr(np.argsort(pred_result, axis=1))
        return sorted_indices, pred_result[:, sorted_indices]

    @classmethod
    def load(cls, model_dir=None, model_metadata=None, cached_component=None, **kwargs):
        # type: (Text, Metadata, Optional[Component], **Any) -> SklearnClassifier
        import cloudpickle

        if model_dir and model_metadata.get("classifier_sklearn"):
            classifier_file = os.path.join(model_dir, model_metadata.get("classifier_sklearn"))
            with io.open(classifier_file, 'rb') as f:  # pragma: no test
                return cloudpickle.load(f, encoding="latin-1")
        else:
            return SklearnClassifier()

    def persist(self, model_dir):
        # type: (Text) -> Dict[Text, Any]
        """Persist this model into the passed directory. Returns the metadata necessary to load the model again."""

        import cloudpickle

        classifier_file = os.path.join(model_dir, "label_classifier.pkl")
        with io.open(classifier_file, 'wb') as f:
            cloudpickle.dump(self, f)

        return {
            "classifier_sklearn": "label_classifier.pkl"
        }
class RandomForestClassifier(Component):
    """Text classifier using the sklearn framework"""

    name = "RandomForest_Classifier"

    provides = ["classifylabel", "classifylabel_ranking"]

    requires = ["sentence_embedding"]

    def __init__(self, config=None, clf=None, le=None):
        # type: (sklearn.model_selection.GridSearchCV, sklearn.preprocessing.LabelEncoder) -> None
        """Construct a new classifier using the sklearn framework."""
        from sklearn.preprocessing import LabelEncoder

        if le is not None:
            self.le = le
        else:
            self.le = LabelEncoder()
        self.clf = clf

    @classmethod
    def required_packages(cls):
        # type: () -> List[Text]
        return ["numpy", "sklearn"]

    def transform_labels_str2num(self, labels):
        # type: (List[Text]) -> np.ndarray
        """Transforms a list of strings into numeric label representation.
        :param labels: List of labels to convert to numeric representation"""

        return self.le.fit_transform(labels)

    def transform_labels_num2str(self, y):
        # type: (np.ndarray) -> np.ndarray
        """Transforms a list of strings into numeric label representation.
        :param y: List of labels to convert to numeric representation"""

        return self.le.inverse_transform(y)

    def train(self, training_data, config, **kwargs):
        # type: (TrainingData, RasaNLUConfig, **Any) -> None
        """Train the classifier on a data set.
        :param num_threads: number of threads used during training time"""
        from sklearn.model_selection import GridSearchCV
        from sklearn.ensemble import RandomForestClassifier
        labels = [e.get("label") for e in training_data.classify_examples]
        if len(set(labels)) < 2:
            logger.warning("Can not train an classifier. Need at least 2 different classes. " +
                        "Skipping training of classifier.")
        else:
            y = self.transform_labels_str2num(labels)
            # TODO fix it, in future sentence will replaced by "features"
            X = np.stack([example.get("sentence_embedding") for example in training_data.classify_examples])
            self.clf=RandomForestClassifier()
#            sklearn_config = config.get("classifier_sklearn")
#            C = sklearn_config.get("C", [1, 2, 5, 10, 20, 100])
#            kernel = sklearn_config.get("kernel", "linear")
#            # dirty str fix because sklearn is expecting str not instance of basestr...
#            tuned_parameters = [{"C": C, "kernel": [str(kernel)]}]
#            cv_splits = max(2, min(MAX_CV_FOLDS, np.min(np.bincount(y)) // 5))  # aim for 5 examples in each fold
#
#            self.clf = GridSearchCV(SVC(C=1, probability=True, class_weight='balanced'),
#                                    param_grid=tuned_parameters, n_jobs=config["num_threads"],
#                                    cv=cv_splits, scoring='f1_weighted', verbose=1)
            self.clf.fit(X, y)

    def process(self, message, **kwargs):
        # type: (Message, **Any) -> None
        """Returns the most likely label and its probability for the input text."""

        if not self.clf:
            # component is either not trained or didn't receive enough training data
            label = None
            label_ranking = []
        else:
            X = message.get("sentence_embedding").reshape(1, -1)
            label_ids, probabilities = self.predict(X)
            labels = self.transform_labels_num2str(label_ids)
            # `predict` returns a matrix as it is supposed
            # to work for multiple examples as well, hence we need to flatten
            labels, probabilities = labels.flatten(), probabilities.flatten()

            if labels.size > 0 and probabilities.size > 0:
                ranking = list(zip(list(labels), list(probabilities)))[:CLASSIFY_RANKING_LENGTH]
                label = {"name": labels[0], "confidence": probabilities[0]}
                label_ranking = [{"name": label_name, "confidence": score} for label_name, score in ranking]
            else:
                label = {"name": None, "confidence": 0.0}
                label_ranking = []

        message.set("classifylabel", label, add_to_output=True)
        message.set("classifylabel_ranking", label_ranking, add_to_output=True)

    def predict_prob(self, X):
        # type: (np.ndarray) -> np.ndarray
        """Given a bow vector of an input text, predict the classify label. Returns probabilities for all labels.
        :param X: bow of input text
        :return: vector of probabilities containing one entry for each label"""

        return self.clf.predict_proba(X)

    def predict(self, X):
        # type: (np.ndarray) -> Tuple[np.ndarray, np.ndarray]
        """Given a bow vector of an input text, predict most probable label. Returns only the most likely label.
        :param X: bow of input text
        :return: tuple of first, the most probable label and second, its probability"""

        pred_result = self.predict_prob(X)
        # sort the probabilities retrieving the indices of the elements in sorted order
        sorted_indices = np.fliplr(np.argsort(pred_result, axis=1))
        return sorted_indices, pred_result[:, sorted_indices]

    @classmethod
    def load(cls, model_dir=None, model_metadata=None, cached_component=None, **kwargs):
        # type: (Text, Metadata, Optional[Component], **Any) -> SklearnClassifier
        import cloudpickle

        if model_dir and model_metadata.get("classifier_sklearn"):
            classifier_file = os.path.join(model_dir, model_metadata.get("classifier_sklearn"))
            with io.open(classifier_file, 'rb') as f:  # pragma: no test
                return cloudpickle.load(f, encoding="latin-1")
        else:
            return SklearnClassifier()

    def persist(self, model_dir):
        # type: (Text) -> Dict[Text, Any]
        """Persist this model into the passed directory. Returns the metadata necessary to load the model again."""

        import cloudpickle

        classifier_file = os.path.join(model_dir, "label_classifier.pkl")
        with io.open(classifier_file, 'wb') as f:
            cloudpickle.dump(self, f)

        return {
            "classifier_sklearn": "label_classifier.pkl"
        }
class AdaBoostClassifier(Component):
    """Text classifier using the sklearn framework"""

    name = "AdaBoost_Classifier"

    provides = ["classifylabel", "classifylabel_ranking"]

    requires = ["sentence_embedding"]

    def __init__(self, config=None, clf=None, le=None):
        # type: (sklearn.model_selection.GridSearchCV, sklearn.preprocessing.LabelEncoder) -> None
        """Construct a new classifier using the sklearn framework."""
        from sklearn.preprocessing import LabelEncoder

        if le is not None:
            self.le = le
        else:
            self.le = LabelEncoder()
        self.clf = clf

    @classmethod
    def required_packages(cls):
        # type: () -> List[Text]
        return ["numpy", "sklearn"]

    def transform_labels_str2num(self, labels):
        # type: (List[Text]) -> np.ndarray
        """Transforms a list of strings into numeric label representation.
        :param labels: List of labels to convert to numeric representation"""

        return self.le.fit_transform(labels)

    def transform_labels_num2str(self, y):
        # type: (np.ndarray) -> np.ndarray
        """Transforms a list of strings into numeric label representation.
        :param y: List of labels to convert to numeric representation"""

        return self.le.inverse_transform(y)

    def train(self, training_data, config, **kwargs):
        # type: (TrainingData, RasaNLUConfig, **Any) -> None
        """Train the classifier on a data set.
        :param num_threads: number of threads used during training time"""
        from sklearn.model_selection import GridSearchCV
        from sklearn.ensemble import AdaBoostClassifier
        labels = [e.get("label") for e in training_data.classify_examples]
        if len(set(labels)) < 2:
            logger.warning("Can not train an classifier. Need at least 2 different classes. " +
                        "Skipping training of classifier.")
        else:
            y = self.transform_labels_str2num(labels)
            # TODO fix it, in future sentence will replaced by "features"
            X = np.stack([example.get("sentence_embedding") for example in training_data.classify_examples])
            self.clf=AdaBoostClassifier()
#            sklearn_config = config.get("classifier_sklearn")
#            C = sklearn_config.get("C", [1, 2, 5, 10, 20, 100])
#            kernel = sklearn_config.get("kernel", "linear")
#            # dirty str fix because sklearn is expecting str not instance of basestr...
#            tuned_parameters = [{"C": C, "kernel": [str(kernel)]}]
#            cv_splits = max(2, min(MAX_CV_FOLDS, np.min(np.bincount(y)) // 5))  # aim for 5 examples in each fold
#
#            self.clf = GridSearchCV(SVC(C=1, probability=True, class_weight='balanced'),
#                                    param_grid=tuned_parameters, n_jobs=config["num_threads"],
#                                    cv=cv_splits, scoring='f1_weighted', verbose=1)
            self.clf.fit(X, y)

    def process(self, message, **kwargs):
        # type: (Message, **Any) -> None
        """Returns the most likely label and its probability for the input text."""

        if not self.clf:
            # component is either not trained or didn't receive enough training data
            label = None
            label_ranking = []
        else:
            X = message.get("sentence_embedding").reshape(1, -1)
            label_ids, probabilities = self.predict(X)
            labels = self.transform_labels_num2str(label_ids)
            # `predict` returns a matrix as it is supposed
            # to work for multiple examples as well, hence we need to flatten
            labels, probabilities = labels.flatten(), probabilities.flatten()

            if labels.size > 0 and probabilities.size > 0:
                ranking = list(zip(list(labels), list(probabilities)))[:CLASSIFY_RANKING_LENGTH]
                label = {"name": labels[0], "confidence": probabilities[0]}
                label_ranking = [{"name": label_name, "confidence": score} for label_name, score in ranking]
            else:
                label = {"name": None, "confidence": 0.0}
                label_ranking = []

        message.set("classifylabel", label, add_to_output=True)
        message.set("classifylabel_ranking", label_ranking, add_to_output=True)

    def predict_prob(self, X):
        # type: (np.ndarray) -> np.ndarray
        """Given a bow vector of an input text, predict the classify label. Returns probabilities for all labels.
        :param X: bow of input text
        :return: vector of probabilities containing one entry for each label"""

        return self.clf.predict_proba(X)

    def predict(self, X):
        # type: (np.ndarray) -> Tuple[np.ndarray, np.ndarray]
        """Given a bow vector of an input text, predict most probable label. Returns only the most likely label.
        :param X: bow of input text
        :return: tuple of first, the most probable label and second, its probability"""

        pred_result = self.predict_prob(X)
        # sort the probabilities retrieving the indices of the elements in sorted order
        sorted_indices = np.fliplr(np.argsort(pred_result, axis=1))
        return sorted_indices, pred_result[:, sorted_indices]

    @classmethod
    def load(cls, model_dir=None, model_metadata=None, cached_component=None, **kwargs):
        # type: (Text, Metadata, Optional[Component], **Any) -> SklearnClassifier
        import cloudpickle

        if model_dir and model_metadata.get("classifier_sklearn"):
            classifier_file = os.path.join(model_dir, model_metadata.get("classifier_sklearn"))
            with io.open(classifier_file, 'rb') as f:  # pragma: no test
                return cloudpickle.load(f, encoding="latin-1")
        else:
            return SklearnClassifier()

    def persist(self, model_dir):
        # type: (Text) -> Dict[Text, Any]
        """Persist this model into the passed directory. Returns the metadata necessary to load the model again."""

        import cloudpickle

        classifier_file = os.path.join(model_dir, "label_classifier.pkl")
        with io.open(classifier_file, 'wb') as f:
            cloudpickle.dump(self, f)

        return {
            "classifier_sklearn": "label_classifier.pkl"
        }