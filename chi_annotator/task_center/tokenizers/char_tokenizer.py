from chi_annotator.task_center.components import Component

class CharTokenizer(Component):
    provides = ["tokens"]

    def __init__(self):
        super(Component, self).__init__()

    def train(self, samples):
        pass

    def process(self, samples):
        pass

import sys
sys.path.append("E:\Git\Chinese-Annotator")
if __name__ == "__main__":
    ct = CharTokenizer()
