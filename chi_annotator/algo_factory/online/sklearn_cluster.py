
import logging
import os
import io
import numpy as np

from chi_annotator.algo_factory.components import Component

logger = logging.getLogger(__name__)


class SklearnCluster(Component):
    """Text classifier using the sklearn framework"""

    name = "cluster_sklearn"
    provides = ["cluster_center"]
    requires = ["sentence_embedding"]

    def __init__(self, config=None, clf=None):
        # type: (sklearn.model_selection.GridSearchCV, sklearn.preprocessing.LabelEncoder) -> None
        """Construct a new classifier using the sklearn framework."""
        self.clf = clf

    @classmethod
    def required_packages(cls):
        # type: () -> List[Text]
        return ["numpy", "sklearn"]

    def train(self, training_data, config, **kwargs):
        # type: (TrainingData, RasaNLUConfig, **Any) -> None
        """Train the classifier on a data set.
        :param num_threads: number of threads used during training time"""
        from sklearn.cluster import KMeans
        # TODO fix it, in future sentence will replaced by "features"
        X = np.stack([example.get("sentence_embedding")
                      for example in training_data.cluster_examples
                      if example.get("sentence_embedding") is not None])
        self.clf = KMeans(n_clusters=2, random_state=0)
        self.clf.fit(X)

    def process(self, message, **kwargs):
        # type: (Message, **Any) -> None
        """Returns the most likely label and its probability for the input text."""

        if not self.clf:
            # component is either not trained or didn't receive enough training data
            label = None
        else:
            if message.get("sentence_embedding") is None:
                logger.warning("text has no embedding, this may because text word not in vocab dict, skipped.")
                message.set("cluster_center", {"center": None}, add_to_output=True)
                return
            X = message.get("sentence_embedding").reshape(1, -1)
            label_ids = self.clf.predict(X)
            # `predict` returns a matrix as it is supposed
            # to work for multiple examples as well, hence we need to flatten
            labels = label_ids.flatten()
            label = {"center": labels[0]}

        message.set("cluster_center", label, add_to_output=True)


    @classmethod
    def load(cls, model_dir=None, model_metadata=None, cached_component=None, **kwargs):
        # type: (Text, Metadata, Optional[Component], **Any) -> SklearnClassifier
        import cloudpickle

        if model_dir and model_metadata.get("cluster_sklearn"):
            classifier_file = os.path.join(model_dir, model_metadata.get("cluster_sklearn"))
            with io.open(classifier_file, 'rb') as f:  # pragma: no test
                return cloudpickle.load(f, encoding="latin-1")
        else:
            return SklearnCluster()

    def persist(self, model_dir):
        # type: (Text) -> Dict[Text, Any]
        """Persist this model into the passed directory. Returns the metadata necessary to load the model again."""

        import cloudpickle

        classifier_file = os.path.join(model_dir, "label_cluster.pkl")
        with io.open(classifier_file, 'wb') as f:
            cloudpickle.dump(self, f)

        return {
            "cluster_sklearn": "label_cluster.pkl"
        }
