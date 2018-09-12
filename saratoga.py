#!/usr/bin/python
# -*- coding: UTF-8 -*-
from cqhttp import CQHttp
import multiServicePythonapi
import random
from googletrans import Translator
import tweepy
import random
import json
import KeysAndTokens as kt
import datetime
from threading import Timer

"""
    global var
"""
screen_name = 'KanColle_STAFF'

auth = tweepy.OAuthHandler(kt.consumer_key, kt.consumer_secret)
auth.set_access_token(kt.access_token, kt.access_token_secret)
api = tweepy.API(auth, proxy='127.0.0.1:8118')
dataPath = "/root/.qqbot-tmp/plugins/data/reply.json"
translator = Translator(proxies = {'http': '127.0.0.1:8118', 'https': '127.0.0.1:8118'})
delta = datetime.timedelta(hours = 8)   #时间差 

alltweets = []
groupList = []
replyList = {}
replyKeys = set()
oldest_id = 0

bot = CQHttp(api_root='http://127.0.0.1:5700/')
usr = 0     # 占用搜图功能用户

# 群消息处理
@bot.on_message('group')
def handle_group_msg(context):
    global usr
    content = context['raw_message']
    print(context)
    if("[CQ:image," in context['message'] and usr == context["user_id"]):
        usr = 0 # 解除占用状态
        msg = context['message']
        start = msg.index("url=") + 4
        end = len(msg) -1 
        try:
            imgurl = msg[start:end]
            # print(imgurl)
        
            result = multiServicePythonapi.imageSearch(imgurl)
            bot.send(context,str(result["sourceURL"]))
        except:
            bot.send(context,"I can't find it, sry")
    if(context['raw_message'] == "findpic"):
        usr = context["user_id"]
        bot.send(context,"好的！直接发在这里吧。👌")
        return
    elif content == 'checkbkl':
        try:
            new_tweets = api.user_timeline('voca_ranking ', count = 1, tweet_mode="extended")
            bot.send(context, 'time: {}\n{}'.format(new_tweets[0].created_at + delta, new_tweets[0].full_text))
        except Exception as err:
            bot.send_private_msg(792735199, err)
    elif content[0:5] == 'check':
        if len(content) == 5:
            bot.send(context, "time: {}\n{}".format(alltweets[0].created_at + delta, alltweets[0].full_text))
        elif len(content) == 6 and content[5] >= '0' and content[5] <= '5':
            bot.send(context, "time: {}\n{}".format(alltweets[int(content[5])].created_at + delta, alltweets[int(content[5])].full_text))
        elif len(content) == 7 and content[5:] == 'ts':
            bot.send(context, "time: {}\n{}".format(alltweets[0].created_at + delta, translator.translate(alltweets[0].full_text, dest='zh-cn').text))
        elif len(content) == 8 and content[5] >= '0' and content[5] <= '5' and content[6:] == 'ts':
            bot.send(context, "time: {}\n{}".format(alltweets[int(content[5])].created_at + delta, translator.translate(alltweets[int(content[5])].full_text, dest='zh-cn').text))
        else:
            bot.send(context, "只接受check0~check5哦")
    elif '现在几点' in content:
        bot.send(context, "It is {} now".format(datetime.datetime.now().strftime('%H:%M')))
    elif '去哪吃' in content:
        bot.send(context, reply('eatingPlace'))            
    # elif '@ME' in content and 'hi' in content:
    #     bot.send(context, "Hello！アメリカ生まれの大型正規空母Saratogaです。歴史深い由緒ある名前を頂いています。あの大きな戦いでは、最初から最後まで頑張ったんです。")        
    # elif '@ME' in content:
    #     bot.send(context, reply('default'))
    # 特殊功能
    elif content[0:2] == '学习':
        init_replyList()
        if '回答' not in content:
            bot.send(context, "那么你想让我回答什么？")
        else:
            Q = content[2:content.index('回答')]
            A = content[content.index('回答') + 2:]
            if len(Q) == 0 or len(A) == 0:
                bot.send(context, "格式有问题啊！")
            # elif ' /表情 ' in Q or  ' /表情 ' in A:
            #     bot.send(context, "作者太菜了所以暂时无法识别QQ表情哦")
            elif len(A) > 20:
                bot.send(context, "回答太长了，不想学")
            else:
                R = add_reply(Q, context['user_id'], A)
                if R :
                    bot.send(context, "get√")
                    save_replyList()
                else:
                    bot.send(context, "有点累，不想学了")

    elif content[0:2] == '查询':
        S = content[content.index('查询') + 2:]
        init_replyList()
        oneReply = search_reply(S)
        if oneReply == None or isinstance(oneReply["content"], list):
            bot.send(context, "我查不到。。。")
        else:
            bot.send(context, "{}\n于{}添加了\n{}".format(oneReply['writer'], oneReply['time'], oneReply['content']))
    elif content[0:2] == '删除':
        S = content[content.index('删除') + 2:]
        init_replyList()
        result = del_reply(S)
        if result == 0:
            bot.send(context, "删除失败了")
        elif result == 1:
            bot.send(context, "删除失败了")
        elif result == 2:
            bot.send(context, "OK！删除成功！")
            save_replyList()
    elif content[0:2] == '翻译':
        if(len(content) > 200):
            bot.send(context, "太长不看")
        else:
            transFlag = 1
            try:
                if content[2] == '到':
                    if content[3:5] == "汉语" or content[3:5] == "中文":
                        translations = translator.translate(content[5:].lstrip(), dest='zh-cn')
                    elif content[3:7] == "简体中文":
                        translations = translator.translate(content[7:].lstrip(), dest='zh-cn')
                    elif content[3:5] == "英语" or content[3:5] == "英文":
                        translations = translator.translate(content[5:].lstrip(), dest='en')
                    elif content[3:5] == "韩语" or content[3:5] == "韩文":
                        translations = translator.translate(content[5:].lstrip(), dest='ko')
                    elif content[3:5] == "日语" or content[3:5] == "日文":
                        translations = translator.translate(content[5:].lstrip(), dest='ja')
                    elif content[3:5] == "德语":
                        translations = translator.translate(content[5:].lstrip(), dest='de')
                    elif content[3:5] == "法语":
                        translations = translator.translate(content[5:].lstrip(), dest='fr')
                    elif content[3:5] == "俄语":
                        translations = translator.translate(content[5:].lstrip(), dest='ru')
                    elif content[3:6] == "世界语":
                        translations = translator.translate(content[6:].lstrip(), dest='eo')
                    elif content[3:7] == "西班牙语":
                        translations = translator.translate(content[7:].lstrip(), dest='es')
                    elif content[3:7] == "葡萄牙语":
                        translations = translator.translate(content[7:].lstrip(), dest='pt')
                    elif content[3:7] == "繁体中文":
                        translations = translator.translate(content[7:].lstrip(), dest='zh-tw')
                    else:
                        transFlag = 0
                else:
                    translations = translator.translate(content[2:].lstrip(), dest='zh-cn')
                if transFlag:
                    bot.send(context, translations.text)
                else:
                    bot.send(context, "抱歉，我暂时做不到")
            except:
                bot.send(context, "出现了点问题，稍等一下再试试看")
    # 其他指定回复
    elif 'サラ' in content or '萨拉' in content or 'sara' in content.lower():
        bot.send(context, reply('sara'))
    else:
        for key in replyKeys:
            if key in content:
                bot.send(context, reply(key))
                break
        pass


# 私聊消息处理
@bot.on_message('private')
def handle_private_msg(context):
    if context['raw_message'] == 'hi' or context['raw_message'] == 'hello':
            bot.send(context, "Hello！アメリカ生まれの大型正規空母Saratogaです。歴史深い由緒ある名前を頂いています。あの大きな戦いでは、最初から最後まで頑張ったんです。")
    elif context['raw_message'] == '--status':
        bot.send(context, str(bot.get_status()))
    else:
        bot.send(context, reply('default'))
    return


@bot.on_notice('group_increase')  # 如果插件版本是 3.x，这里需要使用 @bot.on_event
def handle_group_increase(context):
    bot.send(context, message='欢迎新人～', auto_escape=True)  # 发送欢迎新人

# 加群请求
@bot.on_request('group')
def handle_group_invite_request(context):
    if context['user_id'] == 792735199 and context['sub_type'] == 'invite':
        return {'approve': True}  
    else:
        return {'approve': False}

@bot.on_request('friend')
def handle_friend_invite_request(context):
    if context['comment'] == "kagaya":
        return {'approve': True}  
    else:
        return {'approve': False}


def reply(s):
    reply = replyList.get(s)
    if reply == None:
        return None
    elif isinstance(reply["content"], list):
        return random.choice(reply["content"])
    else:
        return reply["content"]


def add_reply(s, writer, content):
    global replyList
    global replyKeys
    NGlist = ['default', 'sara', 'eatingPlace', '哦']
    if s in NGlist:
        return 0
    newReply = {
            s: {
                "time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "writer": writer,
                "content": content
            } 
        }
    replyList.update(newReply)
    replyKeys = replyList.keys()
    return 1


def del_reply(s):
    """
        返回值含义：
            0：删除失败，未找到
            1：删除失败，无权限
            2：删除成功
    """
    global replyKeys
    reply = replyList.get(s)
    if reply == None:
        return 0
    elif isinstance(reply["content"], list) and reply["writer"] == "administer":
        return 1
    else:
        del replyList[s]
        replyKeys = replyList.keys()
        return 2


def search_reply(s):
    """
        返回对应的dict
        查询不到返回None
    """
    if s in replyList:
        reply = replyList.get(s)
        return reply
    else:
        return None

def init_replyList():
    global replyList
    global replyKeys
    with open(dataPath, 'r', encoding='UTF-8') as f:
        replyList = json.load(f)
    replyKeys = replyList.keys()


def save_replyList():
    with open(dataPath, 'w', encoding='UTF-8') as f:
        json.dump(replyList, f, ensure_ascii = False, indent = 4)

def check_new_tweets():
    """
        定时任务
    """
    global oldest_id
    global alltweets
    try:
        new_tweets = api.user_timeline(screen_name, count = 5, tweet_mode="extended", since_id = oldest_id)
        if len(new_tweets) > 0:           
            if len(groupList) > 0:
                # 发送给所有群
                for each in groupList:
                    for tweet in new_tweets:
                        bot.send_group_msg(each['group_id'], 'time: {}\n{}'.format(tweet.created_at + delta, tweet.full_text))

            new_tweets.extend(alltweets)
            alltweets = new_tweets
            oldest_id = new_tweets[0].id
    except Exception as err:
        bot.send_private_msg(792735199, err)
    global checkThread
    checkThread = Timer(60, check_new_tweets, ()) # 设置定时检查
    checkThread.start()


"""
    BOT START
"""

# if __name__ == "main":
new_tweets = api.user_timeline(screen_name, count = 6, tweet_mode="extended")
alltweets.extend(new_tweets)
oldest_id = alltweets[0].id
groupList = bot.get_group_list()
init_replyList()
checkThread = Timer(1, check_new_tweets, ()) # 设置定时检查
checkThread.start()
bot.run(host='172.17.0.1', port=8081)
