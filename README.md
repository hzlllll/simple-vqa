# simple-vqa

- 一个简单的 vqa demo
- 网上代码都和 shit 一样，要么环境不对，要么要现在各种大数据集和模型权重
- 代码基于 Python3，推荐用 anaconda 维护纯洁环境

## About the Dataset

- 4000 个训练图片
- 1000 张测试图片
  所有图片是 64\*64 的，包含计数 识别 颜色 判断等问题

### Example Images

easy_vqa 和 use_keras 中的 zip 文件解压后可以看数据集 包括问题 答案 和 图片

## Installing the Package

`pip install simple-vqa`

## Generating the Dataset

安装必备的库

```shell
pip install -r gen_data/requirements.txt
```

使用如下命令生成数据，可自行调整

```shell
python gen_data/generate_data.py
```

## Using the Package

通过 use_keras 下 requirements.txt 下的 安装必备的库

```shell
pip install -r use_keras/requirements.txt
```

- use_keras 下 train.py 训练模型
- windows.py 可视化界面
- analyze.py 分析结果
- model.py 模型的结构 可自行修改

## Personal Thinking

- vqa 噱头太大了，而且难以落地，为了提高准确率开放式变多选，不断造数据集，本质还是把图像和自然语言领域的模型各种结合
- 快跑!!!
