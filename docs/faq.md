# FAQ:

## 1.待标注数据集如何分割
应该分为按句子、按段落、按文章三种，写入配置文件由用户选择。
原因是命名实体识别与关系抽取可能按句子或者段落为单位给用户标注比较合适；同时可能用户会有全文章分类的需求，需要给出全文。

## 2.为什么要使用online?
用户标注数据+offline标注数据 为什么还要使用online model 更新数据呢？
原因是offline的模型往往在全量数据上重新学习，也很可能需要使用深度学习模型，训练的速度会很慢。而active learning的人机迭代过程要求模型给出几乎实时的stream级别的训练和推断速度，这时候就需要online model来先行更新数据。

## 3.使用什么机制触发offline model？
这也可以是写入配置文件的参数。一种是用户标够了100个或提前设置好的足够多的新的数据，就可以启用offline model进行训练；另一种是给用户一个按钮，用户可以点击启动后台的offline模型训练并给出进度条。

## 4.系统使用什么格式的配置文件？
推荐json格式的配置文件。请参考一个例子在[这里](https://github.com/crownpku/Rasa_NLU_Chi/tree/master/sample_configs)

## 5. AIgo Factory是什么？和User Instance里面的部分是不是有点重合？
algo factory是算法的代码模块，你可以想象一堆tensorflow或者sklearn的代码；而user instance是config文件与模型参数，是一堆用户生成的json文件和模型文件。algo factory是可以不同user instance传入参数复用的，而每一个user instance代表了一个用户任务的实例。这样设计的目的，是尽可能使系统可复用部分模块化，而抽出用户具体任务的配置与数据单独存储管理。