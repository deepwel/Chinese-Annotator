# Pipeline Example of Spam Email Classification

* 原始数据在 /tests/data/spam_emails_chi

* 用 [xxx] 来代表程序模块，用 < xxx > 来代表配置参数。
    
* 此处以尽可能最简单的步骤，实现整个workflow；整个workflow应该预先配置好在 [user_instance] 的config文件中。

### Pipeline

1. 用户使用 [WebUI] 导入原始数据. [task_center] 调用 [user_instance]的config文件，读取参数。 [task_center] 调用 [algo_factory/preprocess] 来进行分句预处理，然后存储在[database]中。

2. [task_center] 随机调取最初的 <batch_num> 个句子，传去[WebUI]，一个一个供用户进行spam or not的标注。

3. 新标注数据(golden data)保存于 [database] 中，同时传送给 [algo_factory/online] 的feature extractor和SVM算法，进行实时online training (此处是算法大牛们施展功力的时候)，然后随机选取 <inference_num> 个句子进行预测，找出confidence最低的 <low_conf_num> 个句子，传送给webUI再次进行标注。

4. 重复2-3的过程，直到所有句子标注结束 或 [algo_factory/online]对全量数据进行预测后confidence达到 <期望阈值>. 将 [algo_factory/online] 模型参数保存去 [user_instance].

5. 使用 [algo_factory/offline] （可以暂时用相同的SVM重新offline训练一次，未来会写Deep Learning的模型）调用 [database] 中的全量标注数据进行训练，结果保存回 [database]；[WebUI] 提供offline训练进度。[algo_factory/offline] 模型参数保存去 [user_instance]

6. [WebUI] 提供用户导出全量标注数据、导出模型、甚至输入新数据调用 [user_instance] 中的模型参数使用 [algo_factory/offline] 代码进行inference的功能。