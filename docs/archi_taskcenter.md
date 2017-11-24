
author: @burkun


## 基本模块结构

![](/docs/images/arch_taskcenter.png)

## 基本处理流程

![](/docs/images/pipeline_taskcenter.png)



### 定义基本数据类型

#### Message

    基本成员变量
    
        string：text（保存每条样本的原始文本数据）
        dict: data (保存经过每个component后attach到message上的附加数据，按照key value格式存储
        date: datetime （数据生成日期）
        
    基本成员函数
    
        set/get 设置key，和获取key，value对儿，如可以设置分类问题的tag，ner的ne等，所有的设置都是在self.data上进行的


#### TrainData

    基本成员变量
    
        list<Message>: training_examples (代表的是Message的集合）
        
    基本成员函数
    
        classify_examples()  获取所有的分类数据
        entity_examples()    获取所有的ner数据
        num_entity_examples()   ner任务的样本数量
        num_classify_examples() 分类任务的样本数量
        example_iter()  所有样本迭代器


#### Component/Module (数据处理的最基础的模块)

    基本成员变量
        string：name，当前模块的名字，默认是空字符串
        List<string>: requires，需要上一个component提供的处理数据结果的key（这个结果保存在message中）
        List<string>：provides， 在运行数据处理等命令后往Message里面塞入的key，value的key
        Dict: context，全局上下文，跟message无关的（如embedding等，需要在构造函数里面传入）
        Dict: config,包含数据存储路径，模型配置参数，预训练模型地址等
        
    基本成员函数
        create：new一个当前模块
        persist： 持久化component的数据
        load：加载component的数据
        train：批量训练TrainData
        process：预测单条Message
        provide_context: 根据传入的context来判定加载全局的变量（Emebding，TF-IDF等）
        cache_key: 如果改模块是单例，返回None，否则返回一个string标识当前模块的id

--------------------------------------------------------------------------------

## 可配置模块：

* Tokenizer：包含字粒度的Tokenizer，基于分词的Tokenizer（包含postag）（继承自Component）
* Normalizer：归一化文本，包含：繁简，大小写，全半角，数字替换，英文替换等预定义的归一化类（继承自Component）
* FeatureExtracter: 特征提取模块，仅考虑分类问题的话，有依据tokenizer的输出的ngram，embedding，tf-idf等特征抽取（继承自Component）
* Classifier：目前只有基于SVM的classifier，以后可以扩展knn，lr，nn等（继承自Component）
* NentityRelRec：实体关系抽取模块（继承自Component）
* NentityRec：NER识别模块（继承自Component）


## 初步的配置：

### 全局配置文件：

1. 模型存储路径
2. 预训练数据路径（embeding，tf-idf，分词数据库等）
3. 默认的文本数据语言
4. log地址，和log level
5. 服务端口号
6. pipline数组
7. svm参数
8. 训练时线程数

