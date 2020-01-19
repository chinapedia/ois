# NMT

基于 [fairseq](https://github.com/pytorch/fairseq/tree/master/examples/translation) 训练一个英文到中文的翻译模型。

任务细分：

* 语料库数据收集以及清洗
* 预处理
* 使用单语言和双语语料库进行翻译模型训练
* 针对中文的模型优化
* 模型性能测评

## 利用Wikipedia标记数据，做NER任务训练，实现模型优化

一般来说，用多个NLP任务进行模型训练会优化模型的整体性能。可以尝试接入NER任务实现模型优化。

代码变更可以往本项目或者[chinapedia/fairseq](https://github.com/chinapedia/fairseq)提交PR，如果有疑问请创建Issue。
