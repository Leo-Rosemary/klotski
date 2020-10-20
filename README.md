# klotski

## 图片华容道

### 开发环境

- 开发工具：pycharm
- 编程语言：python3

###  操作系统

  Windows

  Python版本:3.7以上

  参照requirements.txt

  pip install -r requirements.txt

### **编译方法**

  安装完依赖requestment.txt后直接运行图片华容道中的整个游戏项目

### **使用方法**

  也可以直接执行run文件夹中的main.exe文件

  但是要将main.exe文件与其他main文件放在同一目录下



## AI大比拼

### 操作说明

- 采用了requests库获取和提交题目
- get_undo()函数会从 http://47.102.118.1:8089/api/team/problem/49 上获取所有未做的题目或者未运行成功的题目，将每题的uuid逐行写入**get_list.txt**文件中
- get_start()函数将每个uuid提交给 http://47.102.118.1:8089/api/challenge/start/+uuid  获取题目的具体信息，返回提交所需要的uuid，返回要交换图片的步数及交换编号，同时获取base64编码的图片并且解码保存，返回给AI部分进行求解
- 通过AI算法求解出操作序列（**operations**）和交换图片（**swap**），保存在answer集合中，与提交所需的**uuid**以及小组固定的**teamid**，**token**封装为**data**列表，使用submit()函数提交
- submit()函数将需要提交的信息data，用requests的post方法提交 http://47.102.118.1:8089/api/challenge/submit 

### 使用方法

- 将无框字符，无框字符分块文件夹与AI大比拼.py放置同一文件夹下
- 在**IDE中直接运行**或者**命令行python AI大比拼.py** 



## 其他说明

[AI大比拼.py](https://github.com/Leo-Rosemary/klotski/blob/main/AI大比拼.py)即为**AI大比拼的算法代码**，[最终版本.py](https://github.com/Leo-Rosemary/klotski/blob/main/最终版本.py)为**编程作业所要求的算法代码**

**游戏原型设计的工程文件** ，**游戏原型设计实现的代码**  以及 **Release**  [请点击队友链接🔗](https://github.com/baiweidou/klotski)