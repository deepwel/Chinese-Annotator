# Chinese-Annotator

[![Join the chat at https://gitter.im/Chinese-Annotator/Lobby](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/Chinese-Annotator/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Build Status](https://travis-ci.org/crownpku/Chinese-Annotator.svg?branch=master)](https://travis-ci.org/crownpku/Chinese-Annotator)
[![License](https://img.shields.io/badge/license-Apache%202-4EB1BA.svg)](https://www.apache.org/licenses/LICENSE-2.0.html)

Annotator for Chinese Text Corpus

Many NLP tasks require lots of labelling data. Current annotators are mostly for English. We want to develop a Chinese Annotator based on existing open source technologies.

## [Chinese-Annotator Gitter 聊天室](https://gitter.im/Chinese-Annotator/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

欢迎一起加入讨论。

## Get Start on OSX

- 安装 python3.6
- 安装 virtualenv
- 新建 python 虚拟环境, 激活虚拟环境
- 安装 mongodb

```bash
virtualenv --python $path_of_python_3.6 $target_virtual_env_path
source $target_virtual_env_path/bin/activate
```

- pip 安装依赖，推荐配置豆瓣或者阿里源

```bash
cd $repository_directory
pip install -r requirement.txt
```

- pip 安装当前项目 python 包

```bash
cd $repository_directory
pip install -e .
```

- 开启 mongodb

```bash
mongod
```

- 导入样例数据

```bash
cd $repository_directory
bash scripts/init_db.sh
```

- 启动 python api 服务

```bash
cd $repository_directory
bash scripts/run_webui.sh
```

- 安装 nodejs, 推荐 lts 版本
- 安装 yarn
- 安装 npm 依赖

```bash
npm install -g yarn
cd $repository_directory/web
yarn
```

- 启动前端开发服务

```bash
yarn start
```

## Project Alignment

![](/docs/images/chinese_annotator_arch.png)

```
.
├── config                  # System config files
├── docs                    # Documentations
├── tests                   # Test cases
│   └── data                # Raw data for tests
├── chi_annotator           # Main backend project folder
│   ├── algo_factory        # Algorithm Factory module containing general algorithms
│       ├── preprocess      # Preprocess codes
│       ├── online          # Online Algorithms for Active Learning (svm for now)
│       └── offline         # Offline Algorithms for higher Accuracy (DL models)
│   ├── task_center         # Task Center module (main entrance and logic control)
│   ├── webui               # WebUI module
│       ├── apis
│       └── static
│   ├── data                # Database module
│   └── user_instance       # User Instance module holding config files for specific tasks
│       └── examples        # User Instance examples
|           ├── classify    # Text Classification
|           ├── ner         # Named Entity Recognition
|           ├── pos_tagger  # POS Tagger
|           └── re          # Relation Extraction
├── web                     # Main frontend project folder
└── ...

```

## 构想：中文文本标注工具

自然语言处理的大部分任务是监督学习问题。序列标注问题如中文分词、命名实体识别，分类问题如关系识别、情感分析、意图分析等，均需要标注数据进行模型训练。深度学习大行其道的今天，基于深度学习的 NLP 模型更是数据饥渴。

最前沿的 NLP 技术往往首先针对英文语料。英文 NLP 的生态很好，针对不同有意思的问题都有不少大规模语料公开供大家研究，如斯坦福的 SQuAD 阅读理解语料。中文方面开源语料就少得多，各种英文 NLP 上的犀利模型和前沿技术都因为中文语料的匮乏很难迁移过来。另一方面，对于一些垂直领域，如医疗、金融、法律、公安等等，专有名词和特有需求甚多，很难将比较 general 的比如在 wikipedia dump 上面训练的模型直接拿过来用。

传统人工标注数据的过程往往是繁琐和低效率的。刚标了一个“联想”是公司名，又来一个“联想集团”，再标一次又来一个“联想集团有限公司”，如此的例子令标注过程含有大量的重复劳动。另一方面也没有一个易上手的标注 UI，标注工作者往往需要直接按预先定好的格式直接在写字板之类的软件中修改原始数据，格式错误率也较高。

能不能构建一个中文文本的标注工具，可以达到以下两个特点：

1. 标注过程背后含有智能算法，将人工重复劳动降到最低；

2. 标注界面显而易见地友好，让标注操作尽可能简便和符合直觉。

答案是可以的。事实上很多标注工具已经做到了这一点，最先进的如 Explosion.ai 的 Prodigy；然而开发了著名的 NLP 开源包 Spacy 的 explosion.ai 选择了将 Prodigy 闭源，而 Spacy 支持中文也仍然遥遥无期。我们希望构建一个开源的中文文本标注工具，而本文很多的技术灵感正是来自[Prodigy 文档](https://prodi.gy/docs/)。

### 主动学习的智能标注算法

流程：

1. 用户标一个 label

2. 主动学习的后台算法分为 online 和 offline 部分。online 部分即时更新模型，可使用诸如 SVM、bag of words 等尽可能快的传统方法；offline 部分当标注数据积累到一定数量时更新模型，可使用准确度较高的深度学习模型。

3. 模型更新后，对尽可能多的 example 做预测，将确信度排序，取确信度最低的一个 example 作为待标注例子。重复 1 的过程。

可以想象如果模型训练得好的话，这个过程将直接忽略掉确信度最大的那些例子，而把所有重点放在分类边界上的那些确信度小的例子。这样可以尽算法所能减少用户端的人工工作量。

online 与 offline 模型互相协作，与用户手动标注的过程一起不断迭代；在最终标注任务完成之后，offline 模型可以重新在所有标注数据上重新训练，以达到最好的模型效果。

### 显而易见的友好标注前端

用户标注的界面应该尽可能符合直觉，让用户完全聚焦在当前的标注任务上。

Prodigy 给了一个非常好的[demo](https://prodi.gy/demo)，每一次的标注只需要用户解决一个 case 的问题。以文本分类为例，对于算法给出的分类结果，只需要点击“正确”提供正样本，“错误”提供负样本，“略过”将不相关的信息滤除，“Redo”让用户撤回操作，四个功能键以最简模式让用户进行标注操作。

真正应用中，应该还要加入一个用户自己加入标注的交互方式，比如用户可以高亮一个词然后选择是“公司”，或者链接两个实体选择他们的关系等等。

![](/docs/images/10.png)

以上是个人觉得的一个智能中文文本标注工具的最大亮点。算法本身还有很多细节需要思考，比如 online 机器学习算法与 offline 深度学习算法的协作、中文 NLP 的特征提取与模型构建、正则规则的引入、word embedding 的训练和使用等等。系统本身还要考虑后台存储(SQLite?)和数据导入导出，前端框架选型和开发，前后端交互(django? flask? RestAPI?)等等的问题。下面是 Prodigy 的简单架构图。

![](/docs/images/11.png)

我们希望专注于中文文本标注的功能。前期我们想实现三种中文 NLP 任务的标注工具：**中文命名实体识别**，**中文关系识别**，**中文文本分类**。未来如果有更多如中文图片问答、中文图片描述之类的任务，我们可以再研究加入图片标注这一块。

希望这个工具的开发会是以中文社区的开源协作方式，为整个中文 NLP 的开源生态做出一点贡献。
