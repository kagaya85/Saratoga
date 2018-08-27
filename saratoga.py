#!/usr/bin/python
# -*- coding: UTF-8 -*-
from cqhttp import CQHttp
<<<<<<< HEAD
import multi-service-python-api
=======
import multiServicePythonapi
>>>>>>> 2dc9d0e7b8599253783a63e096d9d236392249e7

bot = CQHttp(api_root='http://127.0.0.1:5700/')

state = 0
# 0 空闲
# 1 搜索图片
command = ["搜索图片"]
function = []


@bot.on_message('friend')
def handle_msg(context):
    print("msg"+str(context))
    if("image" in context['message']):
        msg = context['message']
        start = msg.index("file=") + 5
<<<<<<< HEAD
        imgsrc = msg[]
=======
        end = len(msg)
        imgsrc = msg[start:end]
        print(imgsrc)
>>>>>>> 2dc9d0e7b8599253783a63e096d9d236392249e7
    return


@bot.on_notice('group_increase')  # 如果插件版本是 3.x，这里需要使用 @bot.on_event
def handle_group_increase(context):
    bot.send(context, message='欢迎新人～', auto_escape=True)  # 发送欢迎新人


@bot.on_request('group', 'friend')
def handle_request(context):
    return {'approve': True}  # 同意所有加群、加好友请求


bot.run(host='172.17.0.1', port=8081)
