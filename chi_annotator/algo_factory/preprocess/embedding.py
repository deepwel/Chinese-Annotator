#!/usr/bin/python
# -*- coding: utf-8 -*-

from chi_annotator.algo_factory.components import Component
import typing
import numpy as np

MAX_WORDS_IN_BATCH = 10000

if typing.TYPE_CHECKING:
    from gensim.models.keyedvectors import KeyedVectors


class EmbeddingExtractor(object):
    """
    embedding extractor, 含char2vec/sen2vec等
    目前实现了char2vec extractor/sen2vec extractor
    """

    name = "embedding_extractor"

    requires = ["tokens"]
    provides = ["word embedding"]

    def __init__(self, config=None):
        super().__init__()
        self.embedding_path = config.get("embedding_path")
        self.embedding_type = config.get("embedding_type")
        if self.embedding_path is None or self.embedding_path == "":
            raise ValueError("Embedding_path is expected.")
        is_binary = True if self.embedding_type == "bin" else False
        from gensim.models.keyedvectors import KeyedVectors
        self.embedding = KeyedVectors.load_word2vec_format(self.embedding_path, binary=is_binary)
        # from gensim.models import Word2Vec
        # self.embedding = Word2Vec.load(self.embedding_path)

    @classmethod
    def cache_key(cls, model_metadata):
        # type: (Metadata) -> Optional[Text]
        return None

    @classmethod
    def create(cls, config):
        # 在training之前加载config
        return EmbeddingExtractor(config=config)

    def _char_process(self, token, **kwargs):
        """
        Args:
            token: char

        Return:
            char embedding
        """
        return self.embedding[token]

    def sentence_process(self, message, **kwargs):
        """
        one sentence embedding extractor
        Args:
            message: instance of message, the data must be tokenized, and stored in message.tokens

        Return:
            the average embedding of all words in sentence, and stored in message.sentence_embedding
        """
        embeddings = []
        tokens = message.get("tokens")
        if tokens is not None:
            for token in tokens:
                # if word in vocab then add into list
                if token in self.embedding:
                    embeddings.append(self._char_process(token))
        if len(embeddings) > 0:
            sentence_embeds = np.asarray(embeddings, dtype=float).mean(axis=0)
            message.set("sentence_embedding", sentence_embeds)
        else:
            message.set("sentence_embedding", None)

    def sentences_batch_process(self, training_data, **kwargs):
        """
        more than one sentence embedding extractor
        Args:
            training_data: list of instances of message, the data must be tokenized, and stored in message.tokens

        Return:
            所有句子的sentence embedding
        """
        if len(training_data) >= 1:
            for message in training_data:
                self.sentence_process(message, **kwargs)


class Embedding(Component):
    name = "embedding"

    requires = ["sentences"]
    provides = ["word2vec_model"]

    def __init__(self, config, wv_model=None, corpus=None):
        """
        Initialize EmbeddingExtractor model.

        Args:
        config: a Class of task_center.config
        wv_model: a instance of gensim.model.Word2vec, use for incremental training

        Returns:
          None.

        Raises:
          None.
        """
        super().__init__()
        self.config = config
        self.wv_model = wv_model
        self.corpus = corpus if corpus else []

    @classmethod
    def required_packages(cls):
        # type: () -> List[Text]
        return ["gensim"]

    @classmethod
    def cache_key(cls, model_metadata):
        # type: (Metadata) -> Optional[Text]
        return None

    @classmethod
    def create(cls, config):
        # 在training之前加载config
        return Embedding(config)

    @classmethod
    def process_raw_data(cls, sentences, max_sentence_length=MAX_WORDS_IN_BATCH, limit=None):
        """
        Todo: 该函数需要进一步修改和需求分析

        Simple format: one sentence = one line; words already preprocessed and separated by whitespace.

        Args:
            sentences: only support .bz2, .gz, and text files
                Example::
                    sentences = LineSentence('myfile.txt')
                Or for compressed files::
                    sentences = LineSentence('compressed_text.txt.bz2')
                    sentences = LineSentence('compressed_text.txt.gz')

            max_sentence_length:

            limit: lines (or not clipped if limit is None, the default).

        Returns:
            LineSentence(sentences)

        Raises:
            ValueError

        """
        from gensim.models.word2vec import LineSentence
        if sentences is not None:
            return LineSentence(sentences, max_sentence_length=max_sentence_length, limit=limit)
        raise ValueError("Sentences needs at least one sentence.")

    def provide_context(self):
        # type: () -> Dict[Text, Any]
        return {"embedding": self.create()}

    def train(self, training_data, config, **kwargs):
        """

        Args:
            training_data:
                LineSentence(data_path)

            config:
                Instance of AnnotatorConfig

                Initialize the model from an iterable of `sentences`. Each sentence is a
                list of words (unicode strings) that will be used for training.

                The `sentences` iterable can be simply a list, but for larger corpora,
                consider an iterable that streams the sentences directly from disk/network.
                See :class:`BrownCorpus`, :class:`Text8Corpus` or :class:`LineSentence` in
                this module for such examples.

                If you don't supply `sentences`, the model is left uninitialized -- use if
                you plan to initialize it in some other way.

                `sg` defines the training algorithm. By default (`sg=0`), CBOW is used.
                Otherwise (`sg=1`), skip-gram is employed.

                `size` is the dimensionality of the feature vectors.

                `window` is the maximum distance between the current and predicted word within a sentence.

                `alpha` is the initial learning rate (will linearly drop to `min_alpha` as training progresses).

                `seed` = for the random number generator. Initial vectors for each
                word are seeded with a hash of the concatenation of word + str(seed).
                Note that for a fully deterministically-reproducible run, you must also limit the model to
                a single worker thread, to eliminate ordering jitter from OS thread scheduling. (In Python
                3, reproducibility between interpreter launches also requires use of the PYTHONHASHSEED
                environment variable to control hash randomization.)

                `min_count` = ignore all words with total frequency lower than this.

                `max_vocab_size` = limit RAM during vocabulary building; if there are more unique
                words than this, then prune the infrequent ones. Every 10 million word types
                need about 1GB of RAM. Set to `None` for no limit (default).

                `sample` = threshold for configuring which higher-frequency words are randomly downsampled;
                    default is 1e-3, useful range is (0, 1e-5).

                `workers` = use this many worker threads to train the model (=faster training with multicore machines).

                `hs` = if 1, hierarchical softmax will be used for model training.
                If set to 0 (default), and `negative` is non-zero, negative sampling will be used.

                `negative` = if > 0, negative sampling will be used, the int for negative
                specifies how many "noise words" should be drawn (usually between 5-20).
                Default is 5. If set to 0, no negative samping is used.

                `cbow_mean` = if 0, use the sum of the context word vectors. If 1 (default), use the mean.
                Only applies when cbow is used.

                `hashfxn` = hash function to use to randomly initialize weights, for increased
                training reproducibility. Default is Python's rudimentary built in hash function.

                `iter` = number of iterations (epochs) over the corpus. Default is 5.

                `trim_rule` = vocabulary trimming rule, specifies whether certain words should remain
                in the vocabulary, be trimmed away, or handled using the default (discard if word count < min_count).
                Can be None (min_count will be used), or a callable that accepts parameters (word, count, min_count) and
                returns either `utils.RULE_DISCARD`, `utils.RULE_KEEP` or `utils.RULE_DEFAULT`.
                Note: The rule, if given, is only used to prune vocabulary during build_vocab() and is not stored as part
                of the model.

                `sorted_vocab` = if 1 (default), sort the vocabulary by descending frequency before
                assigning word indexes.

                `batch_words` = target size (in words) for batches of examples passed to worker threads (and
                thus cython routines). Default is 10000. (Larger batches will be passed if individual
                texts are longer than 10000 words, but the standard cython code truncates to that maximum.)

        Returns:
            Word2vec model that have been trained.

        """
        from gensim.models import Word2Vec
        # for message in training_data.example_iter():
        #     self.corpus.append(message.get("tokens"))
        # corpus = self.process_raw_data(self.corpus, max_sentence_length=config.max_sentence_length,
        #                                limit=config.limit)
        corpus = training_data
        if self.wv_model:
            # 加载已有模型,在此基础上进行增量学习
            model = self.wv_model
            model.train(corpus, total_examples=model.corpus_count, epochs=model.iter)
            print("retrain model")
        else:
            # 没有based model, 从零开始建模
            model = Word2Vec(corpus, size=config.train_config["size"],
                             alpha=config.train_config["alpha"],
                             window=config.train_config["window"],
                             min_count=config.train_config["min_count"],
                             workers=config.train_config["workers"],
                             sample=config.train_config["sample"],
                             sg=config.train_config["sg"],
                             hs=config.train_config["hs"],
                             negative=config.train_config["negative"],
                             cbow_mean=1, iter=config.train_config["iter"])
        self.wv_model = model
        return model

    # 不允许使用一个句子或者一段文字训练word2vec模型?
    # def process(self, message, **kwargs):
    #     model = self.train(message.text, self.config)
    #     return model

    @classmethod
    def load(cls, model_dir=None, model_metadata=None, cached_component=None, **kwargs):
        """
        @Q: model_metadata是否包含了model_dir?

        Args:
            model_dir:
            model_metadata:
            cached_component:

        Returns:

        Raise:

        """
        # type: (Text, Metadata, Optional[Word2VecNLP], **Any) -> Word2VecNLP
        from gensim.models import Word2Vec
        if cached_component:
            return cached_component
        word2vec_file = model_metadata.get("wv_model_path")
        return Embedding(None, wv_model=Word2Vec.load(word2vec_file))

    def persist(self, model_dir, is_binary=False):
        """
        @Q: 对于训练好的模型,要怎么保存? 要好好讨论一下
            metadata = {trained_date: , pipeline: , version: , langage: } 格式是否已经确定? metadata是否要保存model_dir?
            metadata.json要如何命名?

        Args:
            model_dir:
            is_binary:

        Returns:

        Raise:

        """
        # type: (Text) -> Dict[Text, Any]
        # metadata = {trained_date: , pipeline: , version: , langage: }
        # from chi_annotator.algo_factory.common import Metadata
        # metadata_info = {
        #     "trained_at" :
        # }
        import os.path
        if self.wv_model:
            self.wv_model.save(model_dir)
            self.wv_model.wv.save_word2vec_format(model_dir + '.vector', binary=is_binary)
        return {"wv_model_path": model_dir, "embedding_path": model_dir + '.vector'}
