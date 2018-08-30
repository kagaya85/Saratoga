#!/usr/bin/python
# -*- coding: UTF-8 -*-
from cqhttp import CQHttp
import multiServicePythonapi
import random

bot = CQHttp(api_root='http://127.0.0.1:5700/')
global state
state = 0
# 0 空闲
# 1 搜索图片
command = ["搜索图片"]
function = []


@bot.on_message()
def handle_msg(context):
    print("msg"+str(context))
    global state
    if(context['group_id'] == 826530174):
        

        if("image" in context['message'] and state == context["user_id"]):
            msg = context['message']
            start = msg.index("url=") + 4
            end = len(msg) -1 
            try:
                imgurl = msg[start:end]
                print(imgurl)
            
                result = multiServicePythonapi.imageSearch(imgurl)
                bot.send(context,str(result["sourceURL"]))
            except:
                bot.send(context,"失败")
        elif("组长是谁" in context['message']):
            zuzhang = ["辉辉啊","董先森啊","顺子啊"]
            bot.send(context,zuzhang[random.randint(0,2)])
        elif("搜图" in context['message']):
            state = context["user_id"]

    if(context['group_id'] == 491922235):

        if("image" in context['message'] and state == context["user_id"]):
            state = 0
            msg = context['message']
            start = msg.index("url=") + 4
            end = len(msg) -1 
            try:
                imgurl = msg[start:end]
                print(imgurl)
            
                result = multiServicePythonapi.imageSearch(imgurl)
                bot.send(context,str(result["sourceURL"]))
            except:
                bot.send(context,"失败")
        if("搜图" in context['message']):
            state = context["user_id"]
        return


@bot.on_notice('group_increase')  # 如果插件版本是 3.x，这里需要使用 @bot.on_event
def handle_group_increase(context):
    bot.send(context, message='欢迎新人～', auto_escape=True)  # 发送欢迎新人


@bot.on_request('group', 'friend')
def handle_request(context):
    return {'approve': True}  # 同意所有加群、加好友请求


bot.run(host='172.17.0.1', port=8081)
