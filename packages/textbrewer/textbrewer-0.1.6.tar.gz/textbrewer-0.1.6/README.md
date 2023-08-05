[**中文说明**](README.md) | [**English**](README_EN.md)

# TextBrewer

**TextBrewer** 是一个基于PyTorch的、为实现NLP中的**知识蒸馏**任务而设计的工具包。

知识蒸馏以较低的性能损失压缩神经网络模型的大小，提升模型的推理速度，减少内存占用。

## 更新
当前版本: 0.1.6

## 目录
1.  [简介](#简介) 
2.  [安装要求](#安装要求) 
3.  [工作流程](#工作流程) 
4.  [快速开始](#快速开始)
5.  [蒸馏效果](#蒸馏效果)
6.  [核心概念](#核心概念) 
    1.  [变量与规范](#变量与规范)
    2.  [Config和Distiller](#Config和Distiller)
    3.  [用户定义函数](#用户定义函数)
7.  [FAQ](#FAQ)
8.  [API](#API)
9.  [预定义列表与字典 (presets)](#预定义列表与字典 (presets))

## 简介

**TextBrewer** 为NLP中的知识蒸馏任务设计，提供方便快捷的知识蒸馏框架。其主要特点有：

* 方便灵活：适用于多种模型结构（主要面向**Transfomer**结构）
* 易于扩展：诸多蒸馏参数可调，支持增加自定义损失等模块
* 非侵入式：无需对教师与学生模型本身结构进行修改
* 支持典型的NLP任务：文本分类、阅读理解、序列标注等

TextBrewer的主要模块与功能分为3块：

1. **Distillers**：进行蒸馏的核心部件。不同的distiller提供不同的蒸馏模式。有 GeneralDistiller, MultiTeacherDistiller, MultiTaskDistiller 等

2.  **Configurations and presets**(配置与预定义策略)：训练与蒸馏方法的配置，以及预定义蒸馏策略 (soft-label crossentropy, attention/hidden states matching, schedulers, ...)
3.  **Utilities**(辅助工具)：模型参数分析显示等辅助工具

用户准备好 (1) 已训练好的**教师**模型, 待蒸馏的**学生**模型，(2) 训练数据与必要的实验配置， 即可开始蒸馏。

在多个典型NLP任务上，TextBrewer都能取得较好的压缩效果。相关实验见[蒸馏效果](#蒸馏效果)。

## 安装

### 安装要求

* Python >= 3.6
* PyTorch >= 1.1.0
* TensorboardX or Tensorboard

### 安装方式

* 从PyPI安装：

```python
pip install textbrewer
```

* 从源码文件夹安装:

```she
pip install ./textbrewer
```

## 工作流程

![](distillation_workflow.png)

* **Stage 1 :** 在开始蒸馏之前，需要做一些准备工作 :
  1. 训练教师模型
  2. 定义与初始化学生模型（随机初始化，或载入预训练权重）
  3. 构造蒸馏用数据集的dataloader，训练学生模型用的optimizer和learning rate scheduler
  
* **Stage 2 :** 开始蒸馏：
  1. 初始化**distiller**，构造训练配置(**TrainingConfig**)和蒸馏配置(**DistillationConfig**)
  2. 定义*adaptors* 和 *callback* ，分别用与适配模型输入输出和训练过程中的回调 (见 [在用户定义函数](#用户定义函数) )
  3. 调用distiller的train方法开始蒸馏

用户应先实现 **stage 1** ，得到训练好的教师模型；**TextBrewer** 主要负责 **Stage 2**的蒸馏工作。

（TextBrewer中也提供了用于 stage 1 的 BasicTrainer，用于训练教师模型）

下面展示一个简单的例子，包含了TextBrewer的基本用法

## 快速开始

（可运行代码参见 examples/random_token_example）

以蒸馏基于BERT的文本分类模型为例，数据为随机数据，展示TextBrewer的基本用法。

（一些概念会在**核心概念**中解释；在看完[**核心概念**](#核心概念)后再看一遍例子会更容易理解）

* **Stage 1** ： 准备工作

```python
import textbrewer
from textbrewer import GeneralDistiller
from textbrewer import TrainingConfig, DistillationConfig

import torch
from torch.utils.data import Dataset,DataLoader

# 用transformers构建教师与学生模型
# 这段代码中用的transformers == 2.3
from transformers import BertForSequenceClassification, BertConfig, AdamW

# 运行设备
device = torch.device('cpu')

# 定义模型
# bert_config 是 12层BERT-base的配置
# bert_config_T3 是截至3层的BERT
bert_config = BertConfig.from_json_file('bert_config/bert_config.json')
bert_config_T3 = BertConfig.from_json_file('bert_config/bert_config_T3.json')

# 使用hidden_states作为中间输出特征
bert_config.output_hidden_states = True
bert_config_T3.output_hidden_states = True

# 定义教师模型
teacher_model = BertForSequenceClassification(bert_config) #, num_labels = 2
# 教师模型应当被合理初始化，如载入预训练权重，并在下游任务上训练
# 这里出于演示目的，省略相关步骤

# 定义学生模型
student_model = BertForSequenceClassification(bert_config_T3) #, num_labels = 2

teacher_model.to(device=device)
student_model.to(device=device)

#支持 DataParallel并行
#teacher_model = torch.nn.DataParallel(teacher_model)
#student_model = torch.nn.DataParallel(student_model)

# 定义字典形式的Dataset,字典的key和model的forward方法的参数名匹配
# 也可用PyTorch自带的TensorDataset构造数据集，但要注意元素顺序和model的forward的参数顺序一致
class DictDataset(Dataset):
    def __init__(self, all_input_ids, all_attention_mask, all_labels):
        assert len(all_input_ids)==len(all_attention_mask)==len(all_labels)
        self.all_input_ids = all_input_ids
        self.all_attention_mask = all_attention_mask
        self.all_labels = all_labels

    def __getitem__(self, index):
        return {'input_ids': self.all_input_ids[index],
                'attention_mask': self.all_attention_mask[index],
                'labels': self.all_labels[index]}
    
    def __len__(self):
        return self.all_input_ids.size(0)

# 准备一些随机的数据
all_input_ids = torch.randint(low=0,high=100,size=(100,128))  
all_attention_mask = torch.ones_like(all_input_ids)
all_labels = torch.randint(low=0,high=2,size=(100,))
dataset = DictDataset(all_input_ids, all_attention_mask, all_labels)
eval_dataset = DictDataset(all_input_ids, all_attention_mask, all_labels)
dataloader = DataLoader(dataset,batch_size=32)

# 初始化Optimizer和learning rate scheduler.
# Learning rate scheduler 可以为None.
optimizer = AdamW(student_model.parameters(), lr=1e-4)
scheduler = None
```
* **Stage 2** : 使用TextBrewer蒸馏：
```python
######蒸馏相关准备#########
# 展示模型参数量的统计
print("\nteacher_model's parametrers:")
_ = textbrewer.utils.display_parameters(teacher_model,max_level=3)

print("student_model's parametrers:")
_ = textbrewer.utils.display_parameters(student_model,max_level=3)

# 定义 adaptor
def simple_adaptor(batch, model_outputs):
    # model_outputs 的第二个元素是softmax之前的logits
    # model_outputs 的第三个元素是hidden states, 
    # model_outputs[2][i] 是模型第i层的hidden state;
    # model_outputs[2][0] 是模型的embedding。
    # 具体的输出见transformers的相关说明
    return {'logits': model_outputs[1],
            'hidden': model_outputs[2],
            'inputs_mask': batch['attention_mask']}

  
#定义回调函数, 也可以为None
#model和step分别是学生模型和当前训练步数
#这里的例子为：callback用于在验证集上测试模型
def predict(model, eval_dataset, step, device):
    # eval_dataset: 验证数据集
    model.eval()
    pred_logits = []
    label_ids =[]
    dataloader = DataLoader(eval_dataset,batch_size=32)
    for batch in dataloader:
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['labels']
        with torch.no_grad():
            logits, _ = model(input_ids=input_ids, attention_mask=attention_mask)
            cpu_logits = logits.detach().cpu()
        for i in range(len(cpu_logits)):
            pred_logits.append(cpu_logits[i].numpy())
            label_ids.append(labels[i])
    model.train()
    pred_logits = np.array(pred_logits)
    label_ids = np.array(label_ids)
    y_p = pred_logits.argmax(axis=-1)
    accuracy = (y_p==label_ids).sum()/len(label_ids)
    print ("Number of examples: ",len(y_p))
    print ("Acc: ", accuracy)

from functools import partial
# 填充多余的参数
callback_fun = partial(predict, eval_dataset=eval_dataset, device=device) 


# 初始化配置
# 训练配置
train_config = TrainingConfig(device=device)
# 蒸馏配置
distill_config = DistillationConfig(
    temperature=8,     # 温度
    hard_label_weight=0,      # hard_label_loss的权重
    kd_loss_type='ce',        # kd_loss 设为 交叉熵
    probability_shift=False,  # 不启用probability shift策略
    intermediate_matches=[    # 中间层特征匹配策略
     {'layer_T':0, 'layer_S':0, 'feature':'hidden', 'loss': 'hidden_mse','weight' : 1},
     {'layer_T':8, 'layer_S':2, 'feature':'hidden', 'loss': 'hidden_mse', 'weight' : 1},
     {'layer_T':[0,0], 'layer_S':[0,0], 'feature':'hidden', 'loss': 'nst', 'weight': 1},
     {'layer_T':[8,8], 'layer_S':[2,2], 'feature':'hidden', 'loss': 'nst', 'weight': 1}])

print ("train_config:")
print (train_config)

print ("distill_config:")
print (distill_config)

#初始化distiller
distiller = GeneralDistiller(
    train_config=train_config, distill_config = distill_config,
    model_T = teacher_model, model_S = student_model, 
    adaptor_T = simple_adaptor, adaptor_S = simple_adaptor)

# 开始蒸馏
distiller.train(optimizer, scheduler, dataloader, num_epochs=1, callback=callback_fun)

```

## 蒸馏效果

我们在多个中英文文本分类、阅读理解、序列标注数据集上进行了蒸馏实验。实验的配置和效果如下。

### 英文数据集

| Dataset    | Task type | Metrics | \#Train | \#Dev |
| ---------- | -------- | ------- | ------- | ---- |
| MNLI       | 文本分类 | Acc     | 393K    | 20K  |
| SQuAD1.1   | 阅读理解 | EM/F1   | 88K     | 11K  |
| CoNLL-2003 | 序列标注 | F1      | 23K     | 6K   |

* [**MNL**](https://www.nyu.edu/projects/bowman/multinli/)是句对三分类（entailment，neutral，contradictory）任务。

* [**SQuAD1.1**](https://rajpurkar.github.io/SQuAD-explorer/)是抽取式阅读理解任务，要求从篇章中抽取片段作为问题的答案。

* [**CoNLL-2003**](https://www.clips.uantwerpen.be/conll2003/ner)是命名实体识别任务，需要标记出句子中每个词的实体类型。

### 中文数据集

| Dataset | Task type | Metrics | \#Train | \#Dev |
| ------- | ---- | ------- | ------- | ---- |
| XNLI | 文本分类 | Acc | 393K | 2.5K |
| LCQMC | 文本分类 | Acc | 239K | 8.8K |
| CMRC2018 | 阅读理解 | EM/F1 | 10K | 3.4K |
| DRCD | 阅读理解 | EM/F1 | 27K | 3.5K |

* [**XNLI**](https://github.com/google-research/bert/blob/master/multilingual.md) 是MNLI的中文翻译版本，同样为3分类任务。
* [**LCQMC**](http://icrc.hitsz.edu.cn/info/1037/1146.htm)由哈工大深圳研究生院智能计算研究中心发布的句对二分类任务， 判断两个句子的语义是否相同。
* [**CMRC 2018**](https://github.com/ymcui/cmrc2018)是哈工大讯飞联合实验室发布的中文机器阅读理解数据集。 形式与SQuAD相同。
* [**DRCD**](https://github.com/DRCKnowledgeTeam/DRCD)由中国台湾台达研究院发布的基于繁体中文的抽取式阅读理解数据集。其形式与SQuAD相同。


### 模型

对于英文任务，教师模型为[**BERT-base**](https://github.com/google-research/bert); 对于中文任务，教师模型为HFL发布的[**RoBERTa-wwm-ext**](https://github.com/ymcui/Chinese-BERT-wwm)

我们测试了不同的学生模型，除了BiGRU都是和BERT一样的多层transformer结构。模型的参数如下

| Model                 | \#Layers | Hidden_size | Feed-forward size | \#Params | Relative size |
| --------------------- | --------- | ----------- | ----------------- | -------- | ------------- |
| BERT-base (Teacher) | 12        | 768         | 3072              | 108M     | 100%          |
| RoBERTa-wwm (Teacher) | 12        | 768         | 3072              | 108M     | 100%          |
| T6              | 6         | 768         | 3072              | 65M      | 60%           |
| T3              | 3         | 768         | 3072              | 44M      | 41%           |
| T3-small        | 3         | 384         | 1536              | 17M      | 16%           |
| T4-Tiny         | 4         | 312         | 1200              | 14M      | 13%           |
| BiGRU           | -         | 768         | -                 | 31M      | 29%           |

参数量的统计包括了embedding层，但不包括最终适配各个任务的输出层

### 蒸馏配置

```python
distill_config = DistillationConfig(
	temperature = 8,
  intermediate_matches = matches)
# 其他参数为默认值
```

不同的模型用的matches我们采用了以下配置：

| Model    | matches                                                      |
| -------- | ------------------------------------------------------------ |
| BiGRU    | None                                                         |
| T6       | L6_hidden_mse + L6_hidden_smmd                               |
| T3       | L3_hidden_mse + L3_hidden_smmd (英文任务上)  或  L3_hidden_mse (中文任务上) |
| T3-small | L3n_hidden_mse + L3_hidden_smmd                              |
| T4-Tiny  | L4t_hidden_mse + L4_hidden_smmd                              |

各种matches的定义在exmaple/matches/matches.py文件中。均使用GeneralDistiller进行蒸馏。

### 训练配置
蒸馏用的学习率 lr=1e-4(除非特殊说明)。训练30\~60轮。学习率衰减模式和BERT一致(10%的warmup，90%的linear decay)

### 英文实验结果

| Model         | MNLI (m/mm Acc)   | SQuAD (EM/F1)     | CoNLL-2003 (F1) |
| ------------- | ----------------- | ----------------- | --------------- |
| **BERT-base** | 83.7 / 84.0       | 81.5 / 88.6       | 91.1            |
| BiGRU         | -                 | -                 | 85.3            |
| T6            | 83.5 / 84.0  (30) | 88.1 / 80.8  (50) | 90.7            |
| T3            | 81.8 / 82.7  (40) | 76.4 / 84.9  (50) | 87.5 (30)       |
| T3-small      | 81.3 / 81.7  (40) | 72.3 / 81.4 (50)  | 57.4            |
| T4-tiny       | 82.0 / 82.6  (40) | 73.7 / 82.5 (50)  | 54.7            |
| +  数据增强   | -                 | 75.2 / 84.0 (50)  | 79.6            |

说明：

1. 括号内为训练轮数
2. SQuAD任务上用的是NewsQA作为增强数据；CoNLL-2003上用的是HotpotQA的篇章作为增强数据。数据增强对蒸馏效果有明显的提升作用


### 中文实验结果

| Model           | XNLI (Acc) | LCQMC (Acc) | CMRC2018 (EM/F1)  | DRCD (EM/F1)      |
| --------------- | ---------- | ----------- | ----------------- | ----------------- |
| **RoBERTa-wwm** | 79.9       | 89.4        | 68.8 / 86.4       | 86.5 / 92.5       |
| T3              | 78.4 (30)  | 89.0 (30)   | 63.4 / 82.4  (50) | 76.7 / 85.2  (60) |
| + 数据增强      |            |             | 66.4 / 84.2  (50) | 78.2 / 86.4  (60) |
| T3-small        | 76.0  (30) | 88.1  (30)  | 24.4 / 48.1  (50) | 42.2 / 63.2  (40) |
| +  数据增强     | -          | -           | 58.0 / 79.3  (50) | 65.5 / 78.6  (60) |
| T4-tiny         | 76.2  (30) | 88.4  (30)  | -                 | -                 |
| +  数据增强     | -          | -           | 61.8 / 81.8  (50) | 73.3 / 83.5  (60) |

说明：

1. 括号内为训练轮数
2. 蒸馏CMRC2018和DRCD上的模型时学习率分别为1.5e-4和7e-5
3. 蒸馏到T3的实验中，XNLI和LCQMC使用的matches是L3_hidden_mse；其他所有实验使用的均是L3_hidden_mse + L3_hidden_smmd
4. 针对CMRC2018和DRCD数据集的蒸馏实验，不采用学习率衰减：学习率从增长到指定值后一直保持不变
5. 在使用了数据增强的实验中，CMRC2018和DRCD互作为增强数据。可以发现在训练集较小且模型随机初始化的情况下，数据增强的提升作用明显。





## 核心概念

### 变量与规范 

我们采用以下名称约定：

* **Model_T** (教师模型) : torch.nn.Module的实例。教师模型，一般来说参数量等于大于学生模型。

* **Model_S** (学生模型)：torch.nn.Module的实例。学生模型，蒸馏的目标模型。

* **optimizer**：优化器，torch.optim.Optimizer的实例。

* **scheduler**：动态调整学习率。torch.optim.lr_scheduler下的类的实例，提供单独的学习率调整策略。

* **dataloader** : 迭代器，用于获取 batch，一般用torch.utils.data.Dataloader构造。batch的类型可以是tuple或dict:

  ```python
  for batch in dataloader:
    # batch 可以是 tuple 或者 dict
    # do with batch
    #...
    # 前向计算
  ```
  
  **注意：** 训练循环中会判断batch是否是dict。如果是dict，那么以model(\*\*batch, \*\*args) 的形式调用model，否则以 model(\*batch, \*\*args)的形式调用model。所以当batch是tuple时，**注意batch中每个元素的顺序和model接受的参数的顺序相一致**。args则用于传递额外的参数。

### Config和Distiller

#### Configurations

* **TrainingConfig**：训练相关的配置
* **DistillationConfig**：蒸馏相关的配置

具体的可配置项参见[API](#API)说明。

#### Distillers

Distiller负责完成实际的蒸馏过程。目前实现了以下的distillers:

* **BasicDistiller**: 提供**单模型单任务**蒸馏方式。可用作测试或简单实验。
* **GeneralDistiller (常用)**: 提供**单模型单任务**蒸馏方式，并且支持**中间层特征匹配**，一般情况下**推荐使用**。
* **MultiTeacherDistiller**: 多教师蒸馏。将多个（同任务）教师模型蒸馏到一个学生模型上。**暂不支持中间层特征匹配**。
* **MultiTaskDistillation**：多任务蒸馏。将多个（不同任务）单任务教师模型蒸馏到一个多任务学生模型上。**暂不支持中间层特征匹配**。
* **BasicTrainer**：用于单个模型的有监督训练，而非蒸馏。**可用于训练教师模型**。

### 用户定义函数

蒸馏实验中，有两个组件需要由用户提供，分别是**callback** 和 **adaptor**。他们的作用与约定如下：

####  **Callback** 
回调函数，可选，可以为None。在每个checkpoint，保存模型后会调用callback，并传入参数 model=model_S, step=global_step。可以借由回调函数在每个checkpoint评测模型效果。**如果在callback中评测模型，别忘了在callback中调用 model.eval()**。callback的签名为：

* ```python
  callback(model: torch.nn.Module, step: int) -> Any
  ```

#### Adaptors (**adaptor_T** 和 **adaptor_S**)
将模型的输入和输出转换为指定的格式，向distiller解释模型的输入和输出，以便distiller根据不同的策略进行不同的计算。具体地说，在每个训练步，batch和模型的输出model_outputs会作为参数传递给adaptor，adaptor负责重新组织这些数据，返回一个dict（以下分别称作**results_T和results_S**)：

  ```python
    adatpor(batch: Union[Dict,Tuple], model_outputs: Tuple) -> Dict
  ```

它的作用示意图如下

![](trainingloop.png)



 返回的dict的可以包含如下的键值：

  * '**logits**' : List[torch.tensor] or torch.tensor : 类型为list of tensor 或 tuple of tensor 或 tensor ，表示需要计算蒸馏损失的logits，通常为模型最后softmax之前的输出。列表中每一个tensor形状为 (batch_size, num_labels) 或 (batch_size, length, num_labels)
  
  * '**logits_mask**' : List[torch.tensor] or torch.tensor:  0/1矩阵，对logits的某些位置做mask，类型为list of tensor 或 tuple of tensor 或 tensor。如果不想对logits某些位置计算损失，用mask遮掩掉（对应位置设为0）。列表中每一个tensor的形状为 (batch_size, length)
  
    **注意**: logits_mask 仅对形状为 (batch_size, length, num_labels) 的 logits 有效，用于在length维度做mask，一般用于序列标注类型的任务
  
* **’labels'**: List[torch.tensor] or torch.tensor: ground-truth标签，列表中每一个tensor形状为形状为 (batch_size, ) 或 (batch_size, length)

logits 和 logits_mask 和 labels **要么同为 list/tuple of tensor, 要么都是tensor**。

  * ’**losses**' : List[torch.tensor] : 如果模型中已经计算了一些损失并想利用这些损失训练，例如预测的logits和ground-truth的交叉熵，可放在这里。训练时 'losses'下的所有损失将求和并乘以**hard_label_weight**,和蒸馏的损失加在一起做backward。列表中每一个tensor应为scalar，即shape为[]

  * '**attention**': List[torch.tensor] :attention矩阵的列表，用于计算中间层特征匹配。每个tensor的形状为 (batch_size, num_heads, length, length) 或 (batch_size, length, length) ，取决于应用于attention的损失的选取。各种损失函数详见**损失函数**

* '**hidden**': List[torch.tensor] :hidden_states的列表，用于计算中间层特征匹配。每个tensor的形状为(batch_size, length,hidden_dim)

* '**inputs_mask**' : torch.tensor : 0/1矩阵，对'attention'和“hidden'中张量做mask。形状为 (batch_size, length)


这些key**都是可选**的：

* 如果没有inputs_mask或logits_mask，则视为不做masking，或者说相应的mask全为1
* 如果不做相应特征的中间层特征匹配，可不提供'attention'或'hidden'
* 如果不想利用有标签数据上的损失，或者hard_label_weight==0，可不提供'losses'
* 如果不提供'logits'，会略去最后输出层的蒸馏损失的计算
* 'labels' 仅在 probability_shift==True 时需要
* 当然也不能什么都没有，那就不会进行任何训练

**一般情况下，除非做multi-stage的训练，否则'logits' 是必须要有的。**





## FAQ

## API

### Configurations

class **textbrewer.TrainingConfig** (**gradient_accumulation_steps** = 1, **ckpt_frequency** = 1, **ckpt_epoch_frequency**=1, **log_dir** = './logs', **output_dir** = './saved_models', **device** = 'cuda'):

* **gradient_accumulation_steps** (int) : 梯度累加以节约显存。每计算 *gradient_accumulation_steps* 个batch的梯度，调用一次optimizer.step()。大于1时用于在大batch_size情况下节约显存。
* **ckpt_frequency** (int) : 存储模型权重的频率。每训练一个epoch储存模型权重的次数
* **ckpt_epoch_frequency** (int)：每多少个epoch储存模型
  * **ckpt_frequency**=1, **ckpt_epoch_frequency**=1 : 每个epoch结束时存一次 （默认行为）
  * **ckpt_frequency**=2, **ckpt_epoch_frequency**=1 : 在每个epoch的一半和结束时，各存一次
  * **ckpt_frequency**=1, **ckpt_epoch_frequency**=2 : 每两个epoch结束时，存一次
  * **ckpt_frequency**=2, **ckpt_epoch_frequency**=2 : 每2个epoch，仅在第2个epoch的一半和结束时各存一次（一般不会这样设置）
* **log_dir** (str) : 存放tensorboard日志的位置
* **output_dir** (str) : 储存模型权重的位置
* **device** (str, torch.device) : 在CPU或GPU上训练

示例：

```python
from textbrewer import TrainingConfig
#一般情况下，除了log_dir和output_dir自己设置，其他用默认值即可
train_config = TrainingConfig(log_dir=my_log_dir, output_dir=my_output_dir)
```

* (classmethod) **TrainingConfig.from_json_file**(json_file : str) :
  * 从json文件读取配置

* (classmethod) **TrainingConfig.from_dict**(dict_object : Dict) :
  * 从字典读取配置



class **textbrewer.DistillationConfig** (**temperature** = 4, **temperature_scheduler**='none', **hard_label_weight** = 0, **hard_label_weight_scheduler**='none', **kd_loss_type** = 'ce', **kd_loss_weight**=1, **kd_loss_weight_scheduler**='none', **probability_shift**=False, **intermediate_matches** = None):

* **temperature** (float) : 蒸馏的温度。计算kd_loss时教师和学生的logits将被除以temperature。
* **temperature_scheduler** (str): 动态温度调节。有效取值见[**presets**](#预定义列表与字典 (presets))下的**TEMPERATURE_SCHEDULER**。
* **kd_loss_weight** (float): 'logits'项上的kd_loss的权重。
* **hard_label_weight** (float) : 'losses'项的权重。一般来说'losses'项是ground-truth上的损失权重。

  若**hard_label_weight**>0，且在adaptor中提供了 'losses'，那么如下的损失将被包含于最终的total_loss：

​		$$kd\_loss\_weight * kd\_loss + hard\_label\_weight * sum(losses)$$

* **kd_loss_weight_scheduler** (str) 和 **hard_label_weight_scheduler**(str): 动态损失权重调节。有效取值见[**presets**](#预定义列表与字典 (presets))下的 **WEIGHT_SCHEDULER**

* **kd_loss_type** (str) : 模型最后输出的logits上的蒸馏损失函数。有效取值见[**presets**](#预定义列表与字典 (presets))下的 **KD_LOSS_MAP**。常可用的有：
  
  * 'ce': 计算学生和教师的logits的交叉熵损失 。大多数情况下使用'ce'可获得较好的效果
  * 'mse':计算学生和教师的logits的mse损失 。
  
* **probability_shift** (bool): 是否启用probabliity shift 策略：交换教师模型预测的概率最高标签的logit和ground-truth标签的logit，使得ground-truth标签的logit总是最高。需要adaptor提供'labels'。

* **intermediate_matches** (List[Dict] or None) : 可选，模型中间层匹配损失的配置，list的每一个元素为一个字典，表示一对匹配配置。字典的key如下：
  
  * 'layer_T' :  选取教师的第layer_T层
  
  * 'layer_S' :  选取学生的第layer_S层
  
    **注意**：**layer_T 和 layer_S选取的层数是adaptor返回的字典中的feature('attention' 或 'hidden')下的列表中元素的指标，不直接代表网络中实际的层数。**
  
    **注意**：**layer_T 和 layer_S一般来说都为int。但计算FSP/NST loss时，需要分别选取teacher的两层和student的两层。因此当loss为FSP或NST时，layer_T和layer_S是一个包含两个整数的列表，分别表示选取的teacher的两层和student的两层。可参见[例子](toy-example)以及下文示例中的蒸馏配置**
  
  * 'feature' : feature(str) : 中间层的特征名，有效取值见[**presets**](#预定义列表与字典 (presets))下的 **FEATURES** 。可为：
  
    * 'attention' : 表示attention矩阵，大小应为 (batch_size, num_heads, length,length) 或 (batch_size, length, length)
    * 'hidden'：表示隐层输出，大小应为 (batch_size, length, hidden_dim)
  
  * 'loss' : loss(str) :损失函数的具体形式，有效取值见[**presets**](#预定义列表与字典 (presets))下的**MATCH_LOSS_MAP**。常用的有：
  
    * 'attention_mse'
    * 'attention_ce'
    * 'hidden_mse'
    * 'nst'
    * ......
    
  * 'weight': weight (float) : 损失的权重
  
  * 'proj' : proj(List, optional) : 教师和学生的feature维度一样时，可选；不一样时，必选。为了匹配教师和学生中间层feature，所需要的投影函数，将学生侧的输入的维数转换为与教师侧相同。是一个列表，元素为：
  
    * proj[0] (str) :具体的转换函数，有效值见 **PROJ_MAP**。可用的有
      * 'linear'
      * 'relu'
      * 'tanh'
    * proj[1] (int):  转换函数的输入维度（学生侧的维度）
    * proj[2] (int):  转换函数的输出维度（教师侧的维度）
    * proj[3] (dict): 可选，转换函数的学习率等优化相关配置字典。如果不提供，projection的学习率等优化器相关参数将采用optimzer的defaults配置，否则采用这里提供的参数。

**示例：**

```python
from textbrewer import DistillationConfig

#最简单的配置：仅做最基本的蒸馏，用默认值即可，或尝试不同的temperature
distill_config = DistillationConfig(temperature=8)

#加入中间单层匹配的配置。
#此配置下，adaptor_T/S返回的字典results_T/S要包含'hidden'键。
#教师的 results_T['hidden'][10]和学生的results_S['hidden'][3]将计算hidden_mse loss
distill_config = DistillationConfig(
	temperature = 8,
  intermediate_matches = [{'layer_T':10, 'layer_S':3, 'feature':'hidden','loss': 'hidden_mse', 'weight' : 1}]
)

#多层匹配。假设教师和学生的hidden dim分别为768和384，在学生和教师间增加投影（转换）函数
distill_config = DistillationConfig(
	temperature = 8, 
  intermediate_matches = [ \
    {'layer_T':0, 'layer_S':0, 'feature':'hidden','loss': 'hidden_mse', 'weight' : 1,'proj':['linear',384,768]},
    {'layer_T':4, 'layer_S':1, 'feature':'hidden','loss': 'hidden_mse', 'weight' : 1,'proj':['linear',384,768]},
    {'layer_T':8, 'layer_S':2, 'feature':'hidden','loss': 'hidden_mse', 'weight' : 1,'proj':['linear',384,768]},
    {'layer_T':12, 'layer_S':3, 'feature':'hidden','loss': 'hidden_mse', 'weight' : 1,'proj':['linear',384,768]},
  {'layer_T':[0,0], 'layer_S':[0,0], 'feature':'hidden','loss': 'nst', 'weight' : 1},
  {'layer_T':[4,4], 'layer_S':[1,1], 'feature':'hidden','loss': 'nst', 'weight' : 1},
  {'layer_T':[8,8], 'layer_S':[2,2], 'feature':'hidden','loss': 'nst', 'weight' : 1},
  {'layer_T':[12,12],'layer_S':[3,3],'feature':'hidden','loss': 'nst', 'weight' : 1}]
)
```

* (classmethod) **DistillConfig.from_json_file**(json_file : str) :
  * 从json文件读取配置

* (classmethod) **DistillConfig.from_dict**(dict_object : Dict) :
  * 从字典读取配置

### Distillers

初始化某个distiller后，调用用其train方法开始训练/蒸馏。各个distiller的train方法的参数相同。

#### GeneralDistiller 

单模型单任务蒸馏推荐使用。

* class **textbrewer.GeneralDistiller**(**train_config**, **distill_config**, **model_T**, **model_S**, **adaptor_T**, **adaptor_S**, **custom_matches** = None):

  * train_config (TrainingConfig) : 训练配置
  * Distill_config (DistillationConfig)：蒸馏配置
  * model_T (torch.nn.Module)：教师模型
  * model_S (torch.nn.Module)：学生模型
  * custom_matches (List) : 如果预定义的match不满足需求，可通过custom_matches自定义 (暂勿用，未测试)
  * adaptor_T (Callable, function)：教师模型的adaptor
  * adaptor_S (Callable, function)：学生模型的adaptor

    * adatpor (batch, model_outputs) -> Dict：

  为适配不同模型的输入与输出，adaptor需要由用户提供。Adaptor是可调用的函数，接受两个输入，分别为batch （dataloader的输出）和model_outputs（模型的输出）。返回值为一个字典。见**变量与规范**中关于adaptor的说明。


* textbrewer.GeneralDistiller.train(**optimizer**, **schduler**, **dataloader**, **num_epochs**,**call_back**, **\*\*args**)
  * optimizer: 优化器
  * schduler: 调整学习率，可以为None
  * dataloader: 数据集迭代器
  * num_epochs : 训练的轮数
  * callback: 回调函数，可以为None。在每个checkpoint会调用，调用方式为callback(model=self.model_S, step = global_step)。可用于在每个checkpoint做evaluation
  * \*\*args：额外的需要提供给模型的参数

调用模型过程说明：

* 如果batch是list或tuple，那么调用模型的形式为model(\*batch, \*\*args)。所以**请注意batch中各个字段的顺序和模型接受的顺序相匹配。**
* 如果batch是dict，那么调用模型的形式为model(\*\*batch,\*\*args)。所以**请注意batch中的key和模型接受参数名相匹配。**

#### BasicTrainer

进行有监督训练，而非蒸馏。可用于调试，或训练教师模型。

* class **textbrewer.BasicTrainer** (**train_config**, **model**, **adaptor**):
  * train_config (TrainingConfig) : 训练配置
  * model (torch.nn.Module)：待训练的模型
  * adaptor (Callable, function)：待训练的模型的adaptor
* BasicTrainer.train 同 GeneralDistiller.train

#### BasicDistiller

提供最简单的soft-label+hard-label蒸馏方式，**不支持中间层特征匹配**。可作为调试或测试使用。

* class **textbrewer.BasicDIstiller**(**train_config**, **distill_config**, **model_T**, **model_S**, **adaptor_T**, **adaptor_S**):
  * train_config (TrainingConfig) : 训练配置
  * Distill_config (DistillationConfig)：蒸馏配置
  * model_T (torch.nn.Module)：教师模型
  * model_S (torch.nn.Module)：学生模型
  * adaptor_T (Callable, function)：教师模型的adaptor
  * adaptor_S (Callable, function)：学生模型的adaptor
* BasicDistiller.train 同 GeneralDistiller.train

#### MultiTeacherDistiller

多教师蒸馏。将多个（同任务）教师模型蒸馏到一个学生模型上。**不支持中间层特征匹配**。

* class **textbrewer.MultiTeacherDistiller** (**train_config**, **distill_config**, **model_T**, **model_S**, **adaptor_T**, **adaptor_S**):

  * train_config (TrainingConfig) : 训练配置
  * Distill_config (DistillationConfig)：蒸馏配置
  * model_T (List[torch.nn.Module])：教师模型的列表
  * model_S (torch.nn.Module)：学生模型
  * adaptor_T (Callable, function)：教师模型的adaptor
  * adaptor_S (Callable, function)：学生模型的adaptor

* MultiTeacherDistiller.train 同 GeneralDistiller.train

#### MultiTaskDistiller
待补充

### utils

* function **textbrewer.utils.display_parameters(model, max_level=None)**:

  显示模型各个子模块的参数与内存占用量。

  * model (torch.nn.Module) : 待分析的模型
  * max_level(int or None): 显示到第max_level层次。如果max_level==None, 则显示所有层次的参数。

### data_utils
待补充



## 预定义列表与字典 (presets)

Presets中包含了一些预先实现的损失函数等模块以及它们对应的名称

* list **textbrewer.presets.ADAPTOR_KEYS**

  adaptor返回的字典用到的keys ：

  *  'logits', 'logits_mask', 'losses', 'inputs_mask', 'labels', 'hidden', 'attention'

* dict **textbrewer.presets.KD_LOSS_MAP**

  可用的kd_loss种类
  * 'mse' : logits上的mse损失
  * 'ce': logits上的交叉熵损失

* dict **PROJ_MAP** 

  用于匹配不同hidden size的中间层输出结果的转换层

  * 'linear' : 线性变换，无激活函数
  * 'relu' : 激活函数为ReLU
  * 'tanh': 激活函数为Tanh

* dict **MATCH_LOSS_MAP**

  中间层特征损失函数

  * 包含 'attention_mse_sum', 'attention_mse', ‘attention_ce_mean', 'attention_ce', 'hidden_mse', 'cos', 'pkd', 'fsp', 'nst']，细节参见 [中间特征损失函数](#中间特征损失函数)

* dict **WEIGHT_SCHEDULER**

  用于动态调整kd_loss权重和hard_label_loss权重的scheduler

  * ‘linear_decay' : 从1衰减到0
  * 'linear_growth' : 从0增加到1

* dict **TEMPERATURE_SCHEDULER**

  用于动态调整蒸馏温度

  * 'constant' : 温度不变（作为测试用）

  * 'flsw' :  具体参见arxiv: 1911.07471。使用此策略时需要提供两个参数beta和gamma
    
  * 'cwsm': 具体参见arxiv: 1911.07471。使用此策略时需要提供一个参数beta

  与其他预定义模块不同，使用’flsw'和'cwsm'时，应附带上需要的额外的参数，例如：

    ```python
  #flsw
  distill_config = DistillationConfig(
    temperature_scheduler = ['flsw', 1， 1]
    ...)
    
  #cwsm
  distill_config = DistillationConfig(
    temperature_scheduler = ['cwsm', 1]
    ...)
    ```

### 自定义

如果预设模块不能满足需求，可向上述字典中添加自定义的函数/模块，例如

```python
MATCH_LOSS_MAP['my_L1_loss'] = my_L1_loss
WEIGHT_SCHEDULER['my_weight_scheduler'] = my_weight_scheduler
```

在DistiilationConfig中使用：

```python
distill_config = DistillationConfig(
  kd_loss_weight_scheduler = 'my_weight_scheduler'
  intermediate_matches = [{'layer_T':0, 'layer_S':0, 'feature':'hidden','loss': 'my_L1_loss', 'weight' : 1}]
  ...)
  
```

函数的参数规范参见源代码（之后将在更详细的文档中给出）。



### 中间特征损失函数

#### attention_mse

* 接收两个形状为 (**batch_size, num_heads, len, len**)的矩阵，计算两个矩阵间的mse损失。

* 如果adaptor提供了inputs_mask，计算中会按inputs_mask遮掩对应位置。

#### attention_mse_sum

* 接收两个矩阵，如果形状为(**batch_size, len, len**) ，直接计算两个矩阵间的mse损失；如果形状为 (**batch_size, num_heads, len, len**)，将num_heads维度求和，再计算两个矩阵间的mse损失。

* 如果adaptor提供了inputs_mask，计算中会按inputs_mask遮掩对应位置。

#### attention_ce

* 接收两个形状为 (**batch_size, num_heads, len, len**)的矩阵，取dim=-1为softmax的维度，计算两个矩阵间的交叉熵损失。

* 如果adaptor提供了inputs_mask，计算中会按inputs_mask遮掩对应位置。

#### attention_ce_mean

* 接收两个矩阵，如果形状为(**batch_size, len, len**) ，直接计算两个矩阵间的交叉熵损失；如果形状为 (**batch_size, num_heads, len, len**)，将num_heads维度求平均，再计算两个矩阵间的交叉熵损失。计算方式同**attention_ce** 。

* 如果adaptor提供了inputs_mask，计算中会按inputs_mask遮掩对应位置。

#### hidden_mse

* 接收两个形状为 (**batch_size, len, hidden_size**)的矩阵，计算两个矩阵间的mse损失。

* 如果adaptor提供了inputs_mask，计算中会按inputs_mask遮掩对应位置。

#### cos

* 接收两个形状为 (**batch_size, len, hidden_size**)的矩阵，计算它们间的余弦相似度损失。
* 来自[DistilBERT](https://arxiv.org/abs/1910.01108)
* 如果adaptor提供了inputs_mask，计算中会按inputs_mask遮掩对应位置。

#### pkd

* 接收两个形状为 (**batch_size, len, hidden_size**)的矩阵，计算len==0位置上的归一化向量mse损失。
* 来自 [Patient Knowledge Distillation for BERT Model Compression](https://arxiv.org/abs/1908.09355)

#### nst (mmd)

* 接收两个矩阵列表A和B，每个列表中包含两个形状为(**batch_size, len, hidden_size**)的矩阵。A中的矩阵的hidden_size和B中矩阵的hidden_size不必相同。计算A中的两个矩阵的相似度矩阵 ( (batch_size, len, len) ) 和B中的两个矩阵的相似度矩阵  ( (batch_size, len, len) ) 的mse损失。
* 参考：[Like What You Like: Knowledge Distill via Neuron Selectivity Transfer](https://arxiv.org/abs/1707.01219)
* 如果提供了inputs_mask，mask掉padding位。

#### fsp

* 接收两个矩阵列表A和B，每个列表中包含两个形状为(**batch_size, len, hidden_size**)的矩阵。计算A中的两个矩阵的相似度矩阵 ( (batch_size, hidden_size, hidden_size) ) 和B中的两个矩阵的相似度矩阵  ( (batch_size, hidden_size, hidden_size) ) 的mse损失。

* 参考：[A Gift from Knowledge Distillation: Fast Optimization, Network Minimization and Transfer Learning](http://openaccess.thecvf.com/content_cvpr_2017/papers/Yim_A_Gift_From_CVPR_2017_paper.pdf)
* 如果提供了inputs_mask，mask掉padding位。

