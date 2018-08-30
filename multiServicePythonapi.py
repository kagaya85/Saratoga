#!/usr/bin/python
# -*- coding: UTF-8 -*-
import urllib
import json
import requests
from bs4 import BeautifulSoup
import re


def imageSearch(fileurl):
    url = "http://www.iqdb.org/"
    proxies = {"http": "socks5://127.0.0.1:1080","https": "socks5://127.0.0.1:1080"}

    file = requests.get(fileurl)
    files = {'file': file}

    data = {
        'url':fileurl
        }
    try:
        r = requests.post(url, data=data, proxies=proxies)
    except requests.exceptions.ProxyError as e:
        print(str(e))
    except requests.exceptions.ConnectionError as e:
        print('ConnectionError ')
        print(str(e))
    except requests.exceptions.ChunkedEncodingError as e:
        print('ChunkedEncodingError')
        print(str(e))
    except requests.exceptions.HTTPError as e:
        print(str(e))
    except requests.exceptions.Timeout as e:
        print(str(e))

    html = BeautifulSoup(r.text,"html.parser")
    picpageURL = html.find(text="Best match").parent.parent.parent.select('td.image')[0].select('a')[0]['href']
    similarity = html.find(text=re.compile(".*similarity"))
    try:
        if(picpageURL == None):
            print("not found")
        elif("danbooru" in picpageURL):
            ############################
            ##  picURL     图片链接     
            ##  sourceURL  图片出处链接  
            ##  author     作者         
            ##  character  人物(未知:None)
            ##  tags       所有标签     
            #############################
            danbooruTEXT = requests.get("https:"+picpageURL, proxies=proxies)
            danbooruHTML = BeautifulSoup(danbooruTEXT.text,"html.parser")

            picURL = danbooruHTML.select("img#image")[0]['src']
            sourceURL = danbooruHTML.select('#post-information')[0].find(text=re.compile("Source.*")).parent.select('a')[0]['href']
            author = danbooruHTML.find('a',itemprop="author").text

            tags = []
            tagsHTML = danbooruHTML.select('.category-0')
            for tagHTML in tagsHTML:
                tag = tagHTML.select('a')[1].text
                tags.append(tag)

            if(danbooruHTML.select(".category-4")):
                character = danbooruHTML.select(".category-4")[0].select('a')[1].text
            else:
                character = None

        elif("yande.re" in picpageURL):
            ############################
            ##  picURL     图片链接     
            ##  sourceURL  图片出处链接  
            ##  author     作者         
            ##  character  人物
            ##  tags       所有标签     
            #############################
            yandereTEXT = requests.get(picpageURL, proxies=proxies)
            yandereHTML = BeautifulSoup(yandereTEXT.text,"html.parser")

            picURL = yandereHTML.select("img#image")[0]['src']
            sourceURL = yandereHTML.select('#stats')[0].find(text=re.compile("Source.*")).parent.select('a')[0]['href']
            author = yandereHTML.select('li.tag-type-artist')[0].select('a')[1].text

            tags = []
            tagsHTML = yandereHTML.select(".tag-type-general")
            for tagHTML in tagsHTML:
                tag = tagHTML.select('a')[1].text
                tags.append(tag)

            if(yandereHTML.select('.tag-type-character')):
                character = yandereHTML.select('.tag-type-character')[0].select('a')[1].text
            else:
                character = None

        elif("sankaku" in picpageURL):
            if("http" not in picpageURL):
                sankakuTEXT = requests.get("http:"+picpageURL,proxies=proxies)
            else:
                sankakuTEXT = requests.get(picpageURL,proxies=proxies)
                
            sankakuHTML = BeautifulSoup(sankakuTEXT.text,"html.parser")

            picURL = sankakuHTML.select("img#image")[0]['src']
            sourceURL = None
            author = sankakuHTML.select(".tag-type-artist")[0].select('a')[0].text
            
            tags = []
            tagsHTML = sankakuHTML.select(".tag-type-general")
            for tagHTML in tagsHTML:
                tag = tagHTML.selec('a')[0].text
                tags.append(tag)

            if(sankakuHTML.selec('.tag-type-character')):
                character = sankakuHTML.select(".tag-type-character")[0].select('a')[0].text
            else:
                character = None
    except:
        result = {
            'picpageURL':picpageURL,
            "picURL":picURL,
            "author":author,
            "similarity":similarity,
            "character":character,
            "tags":tags,
            "sourceURL":picpageURL
        }

    result = {
        'picpageURL':picpageURL,
        "picURL":picURL,
        "author":author,
        "similarity":similarity,
        "character":character,
        "tags":tags,
        "sourceURL":sourceURL
    }
    return result
