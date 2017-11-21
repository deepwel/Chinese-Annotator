from chi_annotator.task_center.refactor.common import Component

class CharTokenizer(Component):
    provides = ["tokens"]

    def __init__(self):
        super.__init(Component, self)

    def train(self, samples):
        pass

    def process(self, samples):
        pass
