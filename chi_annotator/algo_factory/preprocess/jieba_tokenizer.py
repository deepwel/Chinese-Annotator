import glob
import jieba
# Add jieba userdict file
from chi_annotator.algo_factory.components import Component

jieba_userdicts = glob.glob("./jieba_userdict/*")
for jieba_userdict in jieba_userdicts:
    jieba.load_userdict(jieba_userdict)


class JiebaTokenizer(Component):

    name = "tokenizer_jieba"
    provides = ["tokens"]
    
    def __init__(self, config=None):
        # type: (AnnotatorConfig) -> None
        self.config = config
        super(Component, self).__init__()

    @classmethod
    def required_packages(cls):
        # type: () -> List[Text]
        return ["jieba"]

    def train(self, training_data, config, **kwargs):
        # type: (TrainingData, RasaNLUConfig, **Any) -> None
        if config['language'] != 'zh':
            raise Exception("tokenizer_jieba is only used for Chinese. Check your configure json file.")
            
        for example in training_data.training_examples:
            example.set("tokens", self.tokenize(example.text))

    def process(self, message, **kwargs):
        # type: (Message, **Any) -> None

        message.set("tokens", self.tokenize(message.text))

    def tokenize(self, text):
        # type: (Text) -> List[Token]
        words = jieba.cut(text)
        tokens = [word for word in words]
        return tokens

