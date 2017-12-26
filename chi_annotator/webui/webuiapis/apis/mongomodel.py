import datetime


class DataSet(object):
    def __init__(self, name="", uuid=0, user_uuid="00000000-0000-0000-0000-000000000000"):
        self.name = name
        self.uuid = uuid
        self.user_uuid = user_uuid


class AnnotationRawData(object):
    def __init__(self, text='', labeled=False, uuid=0, dataset_uuid="00000000-0000-0000-0000-000000000000",
                 time_stamp=datetime.datetime.now()):
        self.text = text
        self.labeled = labeled
        self.uuid = uuid
        self.dataset_uuid = dataset_uuid
        self.time_stamp = time_stamp


class AnnotationData(object):
    def __init__(self, text='', label='', uuid=0, dataset_uuid=0, time_stamp=datetime.datetime.now()):
        self.text = text
        self.label = label
        self.uuid = uuid
        self.dataset_uuid = dataset_uuid
        self.time_stamp = time_stamp
