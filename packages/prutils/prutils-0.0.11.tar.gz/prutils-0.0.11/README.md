# prutils

#### 介绍
将自己工作学习中可能会重复使用的功能代码抽取到这里，在多个项目中可以方便的安装使用

#### 软件架构
#### 安装教程
#### 使用说明

#### 参与贡献
#### 码云特技


###  有道云笔记非会员Markdown文档不能粘贴图片的折衷替代方案
#### 需求
* 有道云笔记非会员Markdown文档不能粘贴图片，多有不便

#### 寻求方案
* 发现有道云笔的简单笔记文档可以粘贴图片，分享该文档，打开分享链接可以得到图片的链接
* Markdown文档可以用`![]()`的方式引入图片

#### 解决方案
* 有道云笔记创建一个简单笔记作为图库
* 写一个工具读取这个文档最后一张图片的链接
* 在Markdown文档使用该链接

#### 工具安装
* 下载安装python
    * 下载地址:https://www.python.org/ftp/python/3.8.1/python-3.8.1.exe
    * 安装路径:C:\Python38\python.exe
    * 添加C:\Python38和C:\Python38\Scripts路径到环境变量path
* 安装prutils
    进cmd, 执行pip install --upgrade prutils==0.0.9

#### 工具使用
* 进cmd执行`pru_cmds ydtk {图片url}`,输出最后一张图片地址
![](https://note.youdao.com/yws/public/resource/4f855482811f21fa7e1581222cfda6e7/xmlnote/380345736A804E90B12DE16BA3932D8D/21532)
