#### requirenment

python==3.7.0
pytorch==1.3.1
pytorch-crf==0.7.2
seqeval==0.0.12



#### 目录说明

| - utils.py				存储配置参数等

| - preprocess.py	  预处理数据

| - train.py				训练

| - model.py			  模型及数据类

| - tagging.py			进行标注

| - requirement.txt	 配置项要求

| - model_result		存储训练后的模型

| - data					   语料数据库（源：https://github.com/GeneZC/Chinese-NER, https://github.com/davidsbatista/NER-datasets）



#### 流程

依次运行 preprocess.py， train.py即可获得f1，然后运行tagging.py可对utils.py中的TEST_SENTENCE句子进行标注（注：本程序没有实现中文分词，测试句子需要将分词以空格隔开，或者从data\chinese\train.txt中任意截取一句进行测试）。



#### 实验结果

##### train

模拟 f1_max = 90.7%

测试 f1_max = 89.7%

##### tagging

就 以色列 内阁 通过 耶路撒冷 扩建 计划 外交部 发言人 发表 评论
O B-LOCATION O O B-LOCATION O O B-ORGANIZATION O O O



#### 注：

内含一次训练好的model（9.pt）和中文语料库