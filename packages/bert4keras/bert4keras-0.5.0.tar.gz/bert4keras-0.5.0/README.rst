bert4keras
==========

-  Our elegant implement of bert for keras
-  更清晰、更轻量级的keras版bert
-  个人博客：https://kexue.fm/

功能
----

目前已经实现：

-  加载bert/roberta/albert的预训练权重进行finetune；
-  实现语言模型、seq2seq所需要的attention mask；
-  丰富的examples；
-  从零预训练代码（支持TPU、多GPU，请看pretraining）；
-  兼容keras、tf.keras

使用
----

使用例子请参考examples目录。

之前基于keras-bert给出的例子，仍适用于本项目，只需要将\ ``bert_model``\ 的加载方式换成本项目的。

理论上兼容Python2和Python3，实验环境是Python 2.7、Tesorflow
1.13+以及Keras 2.3.1（已经在2.2.4、2.3.0、2.3.1、tf.keras下测试通过）。

当然，乐于贡献的朋友如果发现了某些bug的话，也欢迎指出修正甚至Pull Requests～

权重
----

目前支持加载的权重：

-  Google原版bert: https://github.com/google-research/bert
-  徐亮版roberta: https://github.com/brightmart/roberta\_zh
-  哈工大版roberta: https://github.com/ymcui/Chinese-BERT-wwm
-  Google原版albert[例子]: https://github.com/google-research/google-research/tree/master/albert
-  徐亮版albert: https://github.com/brightmart/albert\_zh
-  转换后的albert: https://github.com/bojone/albert\_zh
-  华为的NEZHA: https://github.com/huawei-noah/Pretrained-Language-Model/tree/master/NEZHA
-  自研语言模型: https://github.com/ZhuiyiTechnology/pretrained-models

（注：徐亮版albert的开源时间早于Google版albert，这导致早期徐亮版albert的权重与Google版的不完全一致，换言之两者不能直接相互替换。为了减少代码冗余，bert4keras的0.2.4及后续版本均只支持加载Google版以徐亮版中带Google字眼的权重。如果要加载早期版本的权重，请用0.2.3版本。）

背景
----

之前一直用CyberZHG大佬的keras-bert，如果纯粹只是为了在keras下对bert进行调用和fine
tune来说，keras-bert已经足够能让人满意了。

然而，如果想要在加载官方预训练权重的基础上，对bert的内部结构进行修改，那么keras-bert就比较难满足我们的需求了，因为keras-bert为了代码的复用性，几乎将每个小模块都封装为了一个单独的库，比如keras-bert依赖于keras-transformer，而keras-transformer依赖于keras-multi-head，keras-multi-head依赖于keras-self-attention，这样一重重依赖下去，改起来就相当头疼了。

所以，我决定重新写一个keras版的bert，争取在几个文件内把它完整地实现出来，减少这些依赖性，并且保留可以加载官方预训练权重的特性。

鸣谢
----

感谢CyberZHG大佬实现的keras-bert，本实现有不少地方参考了keras-bert的源码，在此衷心感谢大佬的无私奉献。

交流
----

QQ交流群：67729435，微信群请加机器人微信号spaces\_ac\_cn
