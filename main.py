import subprocess
import requests
import os
from bilibili_api import live, sync
import datetime
import pygame
import time
from typing import Dict, TypedDict
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bilibili_api import live, sync
import asyncio

#全部变量

# ChatGPT API的URL和密钥
bot_api_url = "https://proxy.nvoid.games/proxy/https://api.openai.com/v1/chat/completions" # openai的api链接
bot_api_key = "key" # 填写你的api-key

#Edgetts音色
bot_voice = "zh-CN-XiaoyiNeural"

# ChatGPT参数
chatgpt_params = {
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "system", "content": "现在你正在哔哩哔哩直播，你的名字叫XX，你是由XXX制造的AI模型，后面的聊天将会是b站用户和你的互动，且每一条消息与上一条都没有联系，你的回答要尽量简短。"}],# 设置ai预设
    "max_tokens": 1000,# 设置单次回复量（最大）
    "temperature": 0.7,
    "n": 1,
    "stop": "\n"
}

# 连接Bilibili直播弹幕服务器
room_id = int(input("请输入直播间编号: "))# 请勿修改，在CMD界面填写
room = live.LiveDanmaku(room_id)
sched = AsyncIOScheduler(timezone="Asia/Shanghai")  # 定时任务框架

#语音输出模块
def putvoice(answer):

    # 使用Edge TTS生成回答的音频文件
    tts_text = answer.replace('"', '\\"')  # 转义引号
    # 设置要合成的文本
        #生成TTS语音
    command = f'edge-tts --voice {bot_voice} --text "{tts_text}" --write-media output.mp3'  # 将 AI 生成的文本传递给 edge-tts 命令
    subprocess.run(command, shell=True)  # 执行命令行指令

    # 播放音频文件
        # 初始化 Pygame
    pygame.mixer.init()

        # 加载语音文件
    pygame.mixer.music.load("output.mp3")

        # 播放语音
    pygame.mixer.music.play()

        # 等待语音播放结束
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

        # 退出临时语音文件
    pygame.mixer.quit()


#礼物感谢功能
class Gift(TypedDict):
    """
    用户赠送礼物列表
    username: 用户名
    last_gift_time: 最后一次赠送礼物时时间戳
    gift_list: 赠送的礼物字典，格式 礼物名: 数量
    """
    username: str
    last_gift_time: int
    gift_list: Dict[str, int]

user_list: Dict[int, Gift] = dict()

@room.on('SEND_GIFT')
async def on_gift(event):
    "记录礼物"
    info = event['data']['data']
    uid = info['uid']
    user = user_list.get(uid)
    if user:
        # 如果用户列表中有该用户 则更新他的礼物字典以及礼物时间戳
        num = user['gift_list'].get(info['giftName'], 0)
        user['gift_list'][info['giftName']] = num + info['num']
        user['last_gift_time'] = int(time.time())
    else:
        # 不存在则以现在时间及礼物新建 Gift 对象
        user_list[uid] = Gift(
            username=info['uname'],
            last_gift_time=int(time.time()),
            gift_list={info['giftName']: info['num']}
        )
        # 开启一个监控
        sched.add_job(check, 'interval', seconds=1, args=[uid], id=str(uid))
async def check(uid: int):
    "判断是否超过阈值并输出"
    user = user_list.get(uid)
    if user:
        if int(time.time()) - user.get('last_gift_time', 0) > 5:  # 此处的 5 即需求中的 n 表示秒数
            sched.remove_job(str(uid))  # 移除该监控任务
            gift_result = user_list.pop(uid)  # 将该用户从列表中弹出并打印
            out = '谢谢' + gift_result['username'] + '赠送的' + '、'.join([str(v) + '个' + k for k, v in gift_result['gift_list'].items()])
            putvoice(out)
if __name__ == '__main__':
    sched.start()  # 启动定时任务

#回复弹幕功能
@room.on("DANMU_MSG")
async def on_danmaku(event):
    content = event["data"]["info"][1]  # 获取弹幕内容
    user_name = event["data"]["info"][2][1]  # 获取用户昵称
    print(f"[{user_name}]: {content}")  # 打印弹幕信息

    question = content  # 设置观众提问

    # 使用ChatGPT与观众进行对话
    chatgpt_params["messages"].append({"role": "user", "content": question})
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {bot_api_key}"
    }
    response = requests.post(bot_api_url, headers=headers, json=chatgpt_params)
    response_data = response.json()
    answer = response_data["choices"][0]["message"]["content"]
    print(f"[AI回复{user_name}]: {answer}")  # 打印AI回复信息

    putvoice(answer)

sync(room.connect())  # 开始监听弹幕流

if __name__ == '__main__': #如果不被调用则并发执行
    asyncio.get_event_loop().run_until_complete(get_data())