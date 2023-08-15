# GPTinBlive

一个将GPT接入哔哩哔哩直播的项目,目前实现了自动回复弹幕以及礼物并语音输出的功能

闲着没事自己做着玩的，之后不一定更不更新




### 运行环境

- Python 3.6+
- Windows操作系统

### 安装依赖

下载源码后完整解压得到文件夹

进入文件夹后在上方点击![image](https://github.com/Nothingness-Void/GPTinBlive/assets/55913486/ed9fdb93-9143-4dbb-87ed-23a8097ec397)  

输入`cmd`打开命令提示符  

在命令提示符中使用以下命令安装所需库：

`pip install -r requirements.txt`

**或**

直接复制文件夹路径按`win`+`r`输入`cmd`打开命令提示符
输入`cd 刚才复制的路径`
并执行上述安装命令

### 使用

1. 用代码编辑工具打开main.py文件。
2. 在# ChatGPT API的URL和密钥中设置api链接（这个可以不改）和你的APIKey
3. 按照您的意愿调整机器人的预设。
4. 用Python运行main.py文件。
5. 输入要连接的B站直播间编号。
6. 按下`Enter`键开始监听弹幕流。


##特别感谢

启发项目 `https://github.com/yxc0915/GPTForBiliBiliLive` 

B站API `https://github.com/Nemo2011/bilibili-api`
