
# IDKB-QAS：Independent Dynamic Knowledge-Based Retrieval Augmented Question-Answering Systems

## 模型框架


## 项目框架


## 环境配置


idkb.node.server
IDKB-计算、存储节点：IDKB内核、数据库、向量数据库存储、API服务
docker,sql，milvus-standalone，django

```
conda create -n idkb_env python=3.10 -y




basedir=/root/idkb
cd $basedir

# clone
git clone https://github.com/yasuo626/IDKB.git

workdir=$basedir/idkb/WorkNode/idkb_work





#安装docker和milvus
docker安装
https://docs.docker.com/engine/install/ubuntu/

mkdir $basedir/milvus
cd $basedir/milvus
wget https://github.com/milvus-io/milvus/releases/download/v2.3.8/milvus-standalone-docker-compose.yml -O docker-compose.yml


#conda安装环境
conda env create -f idkb.yaml

source activate
conda activate idkb
sudo python3 manage.py runserver 8000


```



idkb.llm.local
IDKB_LLM-本地模型部署节点：IDKB本地模型支持
glm3-6b

```
# 创建glm3环境

bash local_model.sh

```


idkb.llm.web
IDKB_LLM-云端模型节点：IDKB云端模型支持
gpt3.5，gpt4



idkb.node.app
IDKB_ASSISTANT-业务、管理节点：前端业务处理、模块管理服务
django,nginx

```
basedir=/root/idkb
cd $basedir

# clone
git clone idkb

workdir=$basedir/idkb



```

## 项目部署

## 图示

