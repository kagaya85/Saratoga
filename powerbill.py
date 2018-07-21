from cqhttp import CQHttp
import requests
import bs4
import json
import os
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

bot = CQHttp(api_root = "http://localhost:5700")

proxies = {"http": "http://localhost:8228"}

state = None

dbc = MySQLdb.connect("localhost", "qqbot", "qqbot", "QQBot", charset="utf8")
cur = dbc.cursor()

def powerbill_beforeCampus(bot, context, msg, state, individualState, inputVars, updateVars):
    updateVars.update({"state": ("powerbill_beforeCampus", GROUP)})

    s = requests.get("http://202.120.163.129:88/default.aspx", proxies = proxies)
    html = bs4.BeautifulSoup(s.text, "lxml")

    powerbill_viewStateStr = html.select_one("#__VIEWSTATE")["value"]
    updateVars.update({"powerbill_viewStateStr": (json.dumps(powerbill_viewStateStr), GROUP)})

    tagCampus = html.select_one("#drlouming")
    defaultCampusValue = tagCampus.find("option", {"selected": True})["value"]

    powerbill_campusList = []

    for child in tagCampus.select("option"):
        if child["value"] != defaultCampusValue:
            powerbill_campusList.append((child["value"], child.string.strip()))

    powerbill_campusList = dict(enumerate(powerbill_campusList))

    outString = u"选择校区："
    outString += u"\n"
    
    for i in powerbill_campusList:
        outString += "\n" + str(i) + '. ' + powerbill_campusList[i][1]

    updateVars.update({"powerbill_campusList": (json.dumps(powerbill_campusList), GROUP)})
    bot.send(context, outString)
    
    return True

def powerbill_beforeBuilding(bot, context, msg, state, individualState, inputVars, updateVars):
    msg = msg.strip()
    
    if msg == "退出":
        bot.send(context, "退出电费查询。")
        updateVars.update({"state": ("idle", GROUP)})
        return True

    if not msg.isdigit():
        return False

    opt = (msg)

    powerbill_campusList = json.loads(inputVars['powerbill_campusList'])
    powerbill_viewStateStr = json.loads(inputVars['powerbill_viewStateStr'])

    print(powerbill_campusList)
    if opt in powerbill_campusList:
        powerbill_campus = powerbill_campusList[opt][0]
        updateVars.update({"powerbill_campus": (json.dumps(powerbill_campus), GROUP)})
    else:
        return False

    updateVars.update({"state": ("powerbill_beforeBuilding", GROUP)})

    s = requests.post("http://202.120.163.129:88/default.aspx", data = {"__EVENTTARGET": "drlouming", "__EVENTARGUMENT": "", "__LASTFOCUS": "", "__VIEWSTATE": powerbill_viewStateStr, "__VIEWSTATEGENERATOR": "CA0B0334", "drlouming": powerbill_campus, "drceng": "", "dr_ceng": "", "drfangjian": ""}, proxies = proxies)
    html = bs4.BeautifulSoup(s.text, "lxml")

    powerbill_viewStateStr = html.select_one("#__VIEWSTATE")["value"]
    updateVars.update({"powerbill_viewStateStr": (json.dumps(powerbill_viewStateStr), GROUP)})

    tagBuilding = html.select_one("#drceng")
    defaultBuildingValue = tagBuilding.find("option", {"selected": True})["value"]

    powerbill_buildingList = []

    for child in tagBuilding.select("option"):
        if child["value"] != defaultBuildingValue:
            powerbill_buildingList.append((child["value"], child.string.strip()))

    powerbill_buildingList = dict(enumerate(powerbill_buildingList))

    outString = u"选择楼栋："
    outString += u"\n"
    
    for i in powerbill_buildingList:
        outString += "\n" + str(i) + '. ' + powerbill_buildingList[i][1]

    updateVars.update({"powerbill_buildingList": (json.dumps(powerbill_buildingList), GROUP)})
    bot.send(context, outString)
    return True

def powerbill_beforeFloor(bot, context, msg, state, individualState, inputVars, updateVars):
    msg = msg.strip()

    if msg == "退出":
        bot.send(context, "退出电费查询。")
        updateVars.update({"state": ("idle", GROUP)})
        return True

    if not msg.isdigit():
        return False

    opt = (msg)

    powerbill_campus = json.loads(inputVars['powerbill_campus'])
    powerbill_buildingList = json.loads(inputVars['powerbill_buildingList'])
    powerbill_viewStateStr = json.loads(inputVars['powerbill_viewStateStr'])

    if opt in powerbill_buildingList:
        powerbill_building = powerbill_buildingList[opt][0]
        updateVars.update({"powerbill_building": (json.dumps(powerbill_building), GROUP)})
    else:
        return False

    updateVars.update({"state": ("powerbill_beforeFloor", GROUP)})

    s = requests.post("http://202.120.163.129:88/default.aspx", data = {"__EVENTTARGET": "drceng", "__EVENTARGUMENT": "", "__LASTFOCUS": "", "__VIEWSTATE": powerbill_viewStateStr, "__VIEWSTATEGENERATOR": "CA0B0334", "drlouming": powerbill_campus, "drceng": powerbill_building, "dr_ceng": "", "drfangjian": ""}, proxies = proxies)
    html = bs4.BeautifulSoup(s.text, "lxml")

    powerbill_viewStateStr = html.select_one("#__VIEWSTATE")["value"]
    updateVars.update({"powerbill_viewStateStr": (json.dumps(powerbill_viewStateStr), GROUP)})

    tagFloor = html.select_one("#dr_ceng")
    defaultFloorValue = tagFloor.find("option", {"selected": True})["value"]

    powerbill_floorList = []

    for child in tagFloor.select("option"):
        if child["value"] != defaultFloorValue:
            powerbill_floorList.append((child["value"], child.string.strip()))

    powerbill_floorList = dict(enumerate(powerbill_floorList))

    outString = u"选择楼层："
    outString += u"\n"
    
    for i in powerbill_floorList:
        outString +=  "\n" + str(i) + '. ' + powerbill_floorList[i][1]

    updateVars.update({"powerbill_floorList": (json.dumps(powerbill_floorList), GROUP)})
    bot.send(context, outString)
    return True

def powerbill_beforeRoom(bot, context, msg, state, individualState, inputVars, updateVars):
    msg = msg.strip()

    if msg == "退出":
        bot.send(context, "退出电费查询。")
        updateVars.update({"state": ("idle", GROUP)})
        return True

    if not msg.isdigit():
        return False

    opt = (msg)

    powerbill_campus = json.loads(inputVars['powerbill_campus'])
    powerbill_building = json.loads(inputVars['powerbill_building'])
    powerbill_floorList = json.loads(inputVars['powerbill_floorList'])
    powerbill_viewStateStr = json.loads(inputVars['powerbill_viewStateStr'])

    if opt in powerbill_floorList:
        powerbill_floor = powerbill_floorList[opt][0]
        updateVars.update({"powerbill_floor": (json.dumps(powerbill_floor), GROUP)})
    else:
        return False

    updateVars.update({"state": ("powerbill_beforeRoom", GROUP)})

    s = requests.post("http://202.120.163.129:88/default.aspx", data = {"__EVENTTARGET": "dr_ceng", "__EVENTARGUMENT": "", "__LASTFOCUS": "", "__VIEWSTATE": powerbill_viewStateStr, "__VIEWSTATEGENERATOR": "CA0B0334", "drlouming": powerbill_campus, "drceng": powerbill_building, "dr_ceng": powerbill_floor, "drfangjian": ""}, proxies = proxies)
    html = bs4.BeautifulSoup(s.text, "lxml")

    powerbill_viewStateStr = html.select_one("#__VIEWSTATE")["value"]
    updateVars.update({"powerbill_viewStateStr": (json.dumps(powerbill_viewStateStr), GROUP)})

    tagRoom = html.select_one("#drfangjian")
    defaultRoomValue = tagRoom.find("option")["value"]

    powerbill_roomList = []

    for child in tagRoom.select("option"):
        if child["value"] != defaultRoomValue:
            powerbill_roomList.append((child["value"], child.string.strip()))

    powerbill_roomList.sort(key=lambda x:x[1])
    powerbill_roomList = dict(enumerate(powerbill_roomList))

    outString = u"选择房间（直接输入房间号）："
    outString += u"\n"
    
    for i in powerbill_roomList:
        outString += "\n" + powerbill_roomList[i][1]

    updateVars.update({"powerbill_roomList": (json.dumps(powerbill_roomList), GROUP)})
    bot.send(context, outString)
    return True

def powerbill_afterRoom(bot, context, msg, state, individualState, inputVars, updateVars):
    msg = msg.strip()
    
    if msg == "退出":
        bot.send(context, "退出电费查询。")
        updateVars.update({"state": ("idle", GROUP)})
        return True
    
    powerbill_campus = json.loads(inputVars['powerbill_campus'])
    powerbill_building = json.loads(inputVars['powerbill_building'])
    powerbill_floor = json.loads(inputVars['powerbill_floor'])
    powerbill_roomList = json.loads(inputVars['powerbill_roomList'])
    powerbill_viewStateStr = json.loads(inputVars['powerbill_viewStateStr'])

    valid = False
    for x in powerbill_roomList:
        if msg == str(powerbill_roomList[x][1]):
            valid = True
            powerbill_room = powerbill_roomList[x][0]
            updateVars.update({"powerbill_room": (json.dumps(powerbill_room), GROUP)})
            break

    if not valid:
        return False

    updateVars.update({"state": ("powerbill_askSave", GROUP)})

    s = requests.Session()
    r = s.post("http://202.120.163.129:88/default.aspx", data = {"__EVENTTARGET": "", "__EVENTARGUMENT": "", "__LASTFOCUS": "", "__VIEWSTATE": powerbill_viewStateStr, "__VIEWSTATEGENERATOR": "CA0B0334", "drlouming": powerbill_campus, "drceng": powerbill_building, "dr_ceng": powerbill_floor, "drfangjian": powerbill_room, "radio": "usedR", "ImageButton1.x": 50, "ImageButton1.y": 50}, proxies = proxies)
    html = bs4.BeautifulSoup(r.text, "lxml")

    powerbill_viewStateStr = html.select_one("#__VIEWSTATE")["value"]
    powerbill_viewStateGeneratorStr = html.select_one("#__VIEWSTATEGENERATOR")["value"]
    powerbill_eventValidationStr = html.select_one("#__EVENTVALIDATION")["value"]
    updateVars.update({"powerbill_viewStateStr_new": (json.dumps(powerbill_viewStateStr), GROUP)})
    updateVars.update({"powerbill_viewStateGeneratorStr_new": (json.dumps(powerbill_viewStateGeneratorStr), GROUP)})
    updateVars.update({"powerbill_eventValidationStr_new": (json.dumps(powerbill_eventValidationStr), GROUP)})

    credit = html.select_one(".number.orange").string

    bot.send(context, "电费还剩 ￥ " + credit + "。是否保存房间数据？")
    return True


def powerbill_directQuery(bot, context, msg, state, individualState, inputVars, updateVars):
    powerbill_campus = json.loads(inputVars['powerbill_campus_saved'])
    powerbill_building = json.loads(inputVars['powerbill_building_saved'])
    powerbill_floor = json.loads(inputVars['powerbill_floor_saved'])
    powerbill_room = json.loads(inputVars['powerbill_room_saved'])
    powerbill_viewStateStr = json.loads(inputVars['powerbill_viewStateStr_saved'])

    s = requests.Session()
    r = s.post("http://202.120.163.129:88/default.aspx", data = {"__EVENTTARGET": "", "__EVENTARGUMENT": "", "__LASTFOCUS": "", "__VIEWSTATE": powerbill_viewStateStr, "__VIEWSTATEGENERATOR": "CA0B0334", "drlouming": powerbill_campus, "drceng": powerbill_building, "dr_ceng": powerbill_floor, "drfangjian": powerbill_room, "radio": "usedR", "ImageButton1.x": 50, "ImageButton1.y": 50}, proxies = proxies)
    html = bs4.BeautifulSoup(r.text, "lxml")

    credit = html.select_one(".number.orange").string

    bot.send(context, "电费还剩 ￥ " + credit + "。")


def powerbill_afterAskSave(bot, context, msg, state, individualState, inputVars, updateVars):
    msg = msg.strip()
    
    if msg == "否":
        bot.send(context, "未保存房间数据。现在可以使用其他命令。")
        updateVars.update({"state": ("idle", GROUP)})
        return True
    
    if msg == "是":
        updateVars.update({"powerbill_viewStateStr_saved": (inputVars['powerbill_viewStateStr'], GROUP)})
        updateVars.update({"powerbill_campus_saved": (inputVars['powerbill_campus'], GROUP)})
        updateVars.update({"powerbill_building_saved": (inputVars['powerbill_building'], GROUP)})
        updateVars.update({"powerbill_floor_saved": (inputVars['powerbill_floor'], GROUP)})
        updateVars.update({"powerbill_room_saved": (inputVars['powerbill_room'], GROUP)})

        bot.send(context, "保存了房间数据。以后可以直接用“查询电费”来查询。如果要更改房间，请“删除电费房间数据”后再次查询。")
        updateVars.update({"state": ("idle", GROUP)})
        return True

    
    return False

def intercept_powerbill(bot, context, msg, state, individualState, inputVars, updateVars):
    group_id = str(context['group_id'])
    print(repr(msg))
    if u'电费' in msg:
        if u'查询' in msg or (u'剩' in msg and (u'多少' in msg or u'几' in msg)):
            powerbill_viewStateStr_saved = json.loads(inputVars['powerbill_viewStateStr_saved'])

            if powerbill_viewStateStr_saved is not None: # powerbill_viewStateStr_saved != "null"
                powerbill_directQuery(bot, context, msg, state, individualState, inputVars, updateVars)
            else:
                powerbill_beforeCampus(bot, context, msg, state, individualState, inputVars, updateVars)
    return True

def intercept_powerbill_delete(bot, context, msg, state, individualState, inputVars, updateVars):
    msg = msg.strip()
    
    if msg == "删除电费房间数据":
        updateVars.update({"powerbill_viewStateStr_saved": ("null", GROUP)})
        bot.send(context, "删除了房间数据。")
        return True

    return False

INDIVIDUAL = 1
GROUP = 0

stateFuncMap = {
    "powerbill_beforeCampus" : (powerbill_beforeBuilding, {"powerbill_viewStateStr": ("null", GROUP), "powerbill_campusList": ("null", GROUP)}),
    "powerbill_beforeBuilding" : (powerbill_beforeFloor, {"powerbill_viewStateStr": ("null", GROUP), "powerbill_buildingList": ("null", GROUP), "powerbill_campus": ("null", GROUP)}),
    "powerbill_beforeFloor" : (powerbill_beforeRoom, {"powerbill_viewStateStr": ("null", GROUP), "powerbill_campus": ("null", GROUP), "powerbill_building": ("null", GROUP), "powerbill_floorList": ("null", GROUP)}),
    "powerbill_beforeRoom" : (powerbill_afterRoom, {"powerbill_viewStateStr": ("null", GROUP), "powerbill_campus": ("null", GROUP), "powerbill_building": ("null", GROUP), "powerbill_floor": ("null", GROUP), "powerbill_roomList": ("null", GROUP)}),
    "powerbill_askSave" : (powerbill_afterAskSave, {"powerbill_viewStateStr": ("null", GROUP), "powerbill_campus": ("null", GROUP), "powerbill_building": ("null", GROUP), "powerbill_floor": ("null", GROUP), "powerbill_room": ("null", GROUP)}),
}

idleFuncList = [
#   (Priority, Function name, neededVars)
    (6000, intercept_powerbill, 
        {
            'powerbill_viewStateStr_saved': ('null', GROUP),
            'powerbill_campus_saved': ('null', GROUP),
            'powerbill_building_saved': ('null', GROUP),
            'powerbill_floor_saved': ('null', GROUP),
            'powerbill_room_saved': ('null', GROUP),
        }
    ),
    
]

allStateFuncList = [
    (5999, intercept_powerbill_delete, 
        {
        }
    ),
]

idleFuncList.sort(reverse = True)

def getVariable(context, cursor, variable, isIndividual, default):
    sql = "SELECT data FROM `main` WHERE variable=%s AND user=%s"
    if isIndividual:
        if 'group_id' in context:
            user = str(context['group_id']) + "#" + " " + str(context['user_id'])
        else:
            user = str(context['user_id'])
    else:
        if 'group_id' in context:
            user = str(context['group_id']) + "#"
        else:
            user = str(context['user_id'])
    num = cursor.execute(sql, (variable, user))

    if (num == 0):
        cursor.execute("INSERT INTO `main` (`user`, `variable`, `data`) VALUES (%s, %s, %s)", (user, variable, default))
        dbc.commit()
        value = default
    else:
        value = cursor.fetchone()[0]

    return value

def setVariable(context, cursor, variable, isIndividual, value):
    sql = "REPLACE INTO main (user, variable, data) VALUES (%s, %s, %s);"
    if isIndividual:
        if 'group_id' in context:
            user = str(context['group_id']) + "#" + " " + str(context['user_id'])
        else:
            user = str(context['user_id'])
    else:
        if 'group_id' in context:
            user = str(context['group_id']) + "#"
        else:
            user = str(context['user_id'])
    num = cursor.execute(sql, (user, variable, value))
    dbc.commit()
    return num

@bot.on_message("group")
def handle_group_message(context):
    msg = (context['message'])
    
    state = getVariable(context, cur, "state", GROUP, "idle")

    print("Current state:", state)

    individualState = getVariable(context, cur, "state", INDIVIDUAL, "idle")

    print("Current individual state:", individualState)

    msgStripped = msg.strip()

    print(msgStripped)

    if msgStripped == r'\resetStatus':
        bot.send(context, "状态重置为 IDLE。")
        setVariable(context, cur, "state", GROUP, "idle")
        setVariable(context, cur, "state", INDIVIDUAL, "idle")
        return

    if msgStripped == r'\showStatus':
        bot.send(context, "当前状态：" + state + "\n当前群聊个人状态：" + individualState)
        return

    if msgStripped == r'\prpr':
        bot.send(context, "Pero pero")
        return

    updateVars = {}

    validState = False
    everIntercepted = False
    if individualState != "idle":
        if individualState in stateFuncMap:
            print("Found individual state in stateFuncMap")
            func, neededVars = stateFuncMap[individualState]
            inputVars = {}
            for neededVarName in neededVars:
                defaultValue, isIndividual = neededVars[neededVarName]
                inputVars[neededVarName] = getVariable(context, cur, neededVarName, isIndividual, defaultValue)
            print("inputVars:", inputVars)

            intercepted = func(bot, context, msg, state, individualState, inputVars, updateVars)
            print("intercepted:", intercepted)
            if intercepted:
                everIntercepted = True
        else:
            print("Undefined individual state:", individualState, ", now resetting it to idle")
            individualState = "idle"
            setVariable(context, cur, "state", INDIVIDUAL, "idle")

    if not everIntercepted and state != "idle":
        if state in stateFuncMap:
            print("Found state in stateFuncMap")
            func, neededVars = stateFuncMap[state]
            inputVars = {}
            for neededVarName in neededVars:
                defaultValue, isIndividual = neededVars[neededVarName]
                inputVars[neededVarName] = getVariable(context, cur, neededVarName, isIndividual, defaultValue)
            print("inputVars:", inputVars)
            intercepted = func(bot, context, msg, state, individualState, inputVars, updateVars)
            print("intercepted:", intercepted)
            if intercepted:
                everIntercepted = True
        else:
            print("Undefined state:", state, ", now resetting it to idle")
            state = idle
            setVariable(context, cur, "state", GROUP, "idle")

    if not everIntercepted:
        for priority, func, neededVars in allStateFuncList:
            inputVars = {}
            for neededVarName in neededVars:
                defaultValue, isIndividual = neededVars[neededVarName]
                inputVars[neededVarName] = getVariable(context, cur, neededVarName, isIndividual, defaultValue)
            intercepted = func(bot, context, msg, state, individualState, inputVars, updateVars)
            if intercepted:
                everIntercepted = True
                break

        if not everIntercepted and state == "idle":
            for priority, func, neededVars in idleFuncList:
                inputVars = {}
                for neededVarName in neededVars:
                    defaultValue, isIndividual = neededVars[neededVarName]
                    inputVars[neededVarName] = getVariable(context, cur, neededVarName, isIndividual, defaultValue)
                intercepted = func(bot, context, msg, state, individualState, inputVars, updateVars)
                if intercepted:
                    everIntercepted = True
                    break

    if everIntercepted:
        for updateVarName in updateVars:
            value, isIndividual = updateVars[updateVarName]
            setVariable(context, cur, updateVarName, isIndividual, value)


bot.run(host = '172.17.0.1', port = 5800)