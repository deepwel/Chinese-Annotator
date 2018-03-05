from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import object
import simplejson
import os
import six

# Describes where to search for the config file if no location is specified
# global configure name
TASK_CENTER_GLOBAL_CONFIG_NAME = "task_center_config.json"
TASK_CENTER_GLOBAL_CONFIG = {
    "config_name": TASK_CENTER_GLOBAL_CONFIG_NAME,
    "max_process_number": 4,
    "max_task_in_queue": 100,
    "log_level": "INFO",
    "port": 5000,
    "language": "ZH",
    "db_name": "chinese_annotator",
    # cur path
    "save_path": os.path.dirname(os.path.abspath(__file__)) + "/../user_instance",
    # make sure user dir is created
    "user_instance_path_template": os.path.join("%s", "%s-%s")
}
# task configure
CLASSIFY_TASK_CONFIG = {
    "embedding_path": None,
    "embedding_type": "txt",
    "word_rep_path": None,
    "max_token_size": 150,
    "min_class_number": 2,
    "pipeline": [],
    "classifier_sklearn":{
        "C": [1, 2, 5, 10, 20, 100],
        "kernel": "linear",
        "num_threads": 3
    },
    "max_train_epoch": 5,
    "batch_num": 64,
    "online_learning": {"use": True, "max_sample_number": 50},
    "offline_max_sample_number": 1e7,
    "condition": None,
    "sort_limit": None,
    "model_type": None,
    "user_uuid": None,
    "dataset_uuid": None,
}

# ner configure, TODO
NER_TASK_CONFIG = {
    "embedding_path": None,
    "word_rep_path": None,
    "max_token_size": 150,
    "tagset": "BIESO",
    "ne_template_path": None,
    "pipeline": [],
    "max_train_epoch": 5,
    "batch_num": 64,
    "eval_type": "hard", # hard and soft, TODO
    "online_learning": {"use": True, "max_sample_number": 50},
    "offline_max_sample_number": 500000
}


class InvalidConfigError(ValueError):
    """Raised if an invalid configuration is encountered."""

    def __init__(self, message):
        # type: (Text) -> None
        super(InvalidConfigError, self).__init__(message)


class AnnotatorConfig(object):

    def __init__(self, task_config, global_config=None):
        """
        init taks config and global config
        Args:
            task_config:
            global_config:

        Returns:

        """
        if task_config is not None:
            self.override(task_config)
        if global_config is not None:
            self.override(global_config)
        else:
            self.override(TASK_CENTER_GLOBAL_CONFIG)
        if isinstance(self.__dict__['pipeline'], six.string_types):
            from chi_annotator.algo_factory import registry
            if self.__dict__['pipeline'] in registry.registered_pipeline_templates:
                self.__dict__['pipeline'] = registry.registered_pipeline_templates[self.__dict__['pipeline']]
            else:
                raise InvalidConfigError("No pipeline specified and unknown pipeline template " +
                                         "'{}' passed. Known pipeline templates: {}".format(
                                                 self.__dict__['pipeline'],
                                                 ", ".join(registry.registered_pipeline_templates.keys())))
        for key, value in self.items():
            setattr(self, key, value)

    def __getitem__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

    def update(self, kv):
        for key in kv:
            self[key] = kv[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __delitem__(self, key):
        del self.__dict__[key]

    def __contains__(self, key):
        return key in self.__dict__

    def __len__(self):
        return len(self.__dict__)

    def __getstate__(self):
        return self.as_dict()

    def __setstate__(self, state):
        self.override(state)

    def items(self):
        return list(self.__dict__.items())

    def as_dict(self):
        return dict(list(self.items()))

    def view(self):
        return simplejson.dumps(self.__dict__, indent=4)

    @staticmethod
    def make_paths_absolute(config, keys):
        """
        make all path in keys to abs path
        :param config: task config
        :param keys: be abs path
        :return:
        """
        abs_path_config = dict(config)
        for key in keys:
            if key in abs_path_config and abs_path_config[key] is not None and not os.path.isabs(abs_path_config[key]):
                abs_path_config[key] = os.path.join(os.getcwd(), abs_path_config[key])
        return abs_path_config

    def override(self, config):
        # abs_path_config = self.make_unicode(self.make_paths_absolute(config, ["path", "response_log"]))
        self.__dict__.update(config)

    def get_save_path_prefix(self):
        user_uuid = self.get("user_uuid", None)
        dataset_uuid = self.get("dataset_uuid", None)
        task_type = self.get("model_type", None)
        if user_uuid is None or dataset_uuid is None or task_type is None:
            return None
        log_suffix = self.get("user_instance_path_template") % (user_uuid, dataset_uuid, task_type)
        return os.path.join(self.get("save_path", "./chi_annotator/user_instance"), log_suffix)

if __name__ == "__main__":
    import os
    print(TASK_CENTER_GLOBAL_CONFIG)
    print(os.path.dirname(os.path.abspath(__file__)))