
## 几个开源文本标注工具的简单调研


### IEPY

![](/docs/images/1.png)

整个工程比较完整，有用户管理系统。前端略重，对用户不是非常友好

代码 https://github.com/machinalis/iepy

说明 http://iepy.readthedocs.io/en/latest/index.html

 
### DeepDive (Mindtagger)

![](/docs/images/2.png)

Screenshot of Mindtagger precision task in progress

介绍 http://deepdive.stanford.edu/labeling

前端比较简单，用户界面友好。

前端代码 https://github.com/HazyResearch/mindbender

将DeepDive的corenlp部分转为支持中文的代码尝试：

https://github.com/SongRb/DeepDiveChineseApps

https://github.com/qiangsiwei/DeepDive_Chinese

https://github.com/mcavdar/deepdive/commit/6882178cbd38a5bbbf4eee8b76b1e215537425b2

 
### BRAT

![](/docs/images/3.png)

介绍 http://brat.nlplab.org/index.html

在线试用 http://weaver.nlplab.org/~brat/demo/latest/#/

代码 https://github.com/nlplab/brat

 
### SUTDAnnotator

![](/docs/images/4.png)

用的不是网页前端而是pythonGUI，但比较轻量。

代码 https://github.com/jiesutd/SUTDAnnotator

Paper https://github.com/jiesutd/SUTDAnnotator/blob/master/lrec2018.pdf
 
 
### Snorkel

![](/docs/images/5.png)

![](/docs/images/6.png)

Page: https://hazyresearch.github.io/snorkel/

Github: https://github.com/HazyResearch/snorkel

Demo Paper:https://hazyresearch.github.io/snorkel/pdfs/snorkel_demo.pdf
 
 
### Slate

![](/docs/images/7.png)

![](/docs/images/8.png)

Code: https://bitbucket.org/dainkaplan/slate/

Paper: http://www.jlcl.org/2011_Heft2/11.pdf
 
 
### Prodigy(闭源)

![](/docs/images/9.png)

和著名的spacy是一家做的

Website: https://prodi.gy/docs/

Blog: https://explosion.ai/blog/prodigy-annotation-tool-active-learning


### labelme(闭源)

[Blog](https://www.toutiao.com/a6486320837224825358/?tt_from=weixin&utm_campaign=client_share&app=news_article&utm_source=weixin&iid=17348668095&utm_medium=toutiao_android&wxshare_count=1)

腾讯内部工具。

labelme只有“文本类目标注和关键词标注”两种task；另外active learning的思路基本一致但貌似还没有实现。

 