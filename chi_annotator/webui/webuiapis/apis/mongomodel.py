import datetime


class AnnotationRawData(object):
    def __init__(self, text='', labeled=False, uuid=0, dataset_id=0, time_stamp=datetime.datetime.now()):
        self.text = text
        self.label = labeled
        self.uuid = uuid
        self.dataset_id = dataset_id
        self.time_stamp = time_stamp


class AnnotationData(object):
    def __init__(self, text='', label='', uuid=0, dataset_id=0, time_stamp=datetime.datetime.now()):
        self.text = text
        self.label = label
        self.uuid = uuid
        self.dataset_id = dataset_id
        self.time_stamp = time_stamp