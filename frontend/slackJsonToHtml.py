# -*- coding: utf-8 -*-

# import
import json
import traceback
from datetime import date, timedelta
import emoji
from dateutil.relativedelta import relativedelta
import datetime
import os


# for 文を日付でまわすための関数 一ヶ月ごと
def date_range(start, stop, step=relativedelta(months=1)):
    current = start
    while current < stop:
        yield current
        current += step


def writeFile(elements, file):
    if elements["type"] == "text":
        text = elements["text"].replace("\n", "<br>").replace(
            "#", "\#").replace("    ", "")
        if "style" in elements.keys():
            style = elements["style"]
            if style.get("bold") == True:
                file.write("<strong>"+text+"</strong>")
            elif style.get("code") == True:
                file.write("<code>"+text+"</code>")
            elif style.get("strike") == True:
                file.write("<strike>"+text+"</strike>")
            else:
                file.write(text)
        else:
            file.write(text)

    elif elements["type"] == "link":
        link = elements["url"]
        file.write("<a href='"+link+"'>"+link+"</a>\n")
    elif elements["type"] == "emoji":
        name = elements["name"]
        if name == "man-bowing":
            name = "bowing_man"
        if name == "woman-bowing":
            name = "bowing_woman"
        file.write(emoji.emojize(':'+name+':', language='alias'))
    elif elements["type"] == "user":
        file.write("@"+elements["user_id"])
    elif elements["type"] == "broadcast":
        file.write("@"+elements["range"])
    elif elements["type"] == "channel":
        file.write("\#"+elements["channel_id"])


# マークダウンから html ファイルに変更するのは絵文字を表示するためである詳細は省く
channelFile = open("../data/channels.json", "r")
fLoad = json.load(channelFile)
channelFile.close()

for CHANNEL_INFO in fLoad:
    CHANNEL_ID = CHANNEL_INFO["id"]
    CHANNEL_NAME = CHANNEL_INFO["name"]

    today = datetime.date.today()
    twoMonthAgo = today+relativedelta(months=-2)

    fromMonth = date(twoMonthAgo.year, twoMonthAgo.month, 1)
    toMonth = date(today.year, today.month, 1)

    frag = False

    for month in date_range(fromMonth, toMonth):
        month = str(month)[0:7]
        fileName = "../data/"+CHANNEL_NAME+"/"+str(month)+".json"
        if os.path.isfile(fileName):
            frag = True
            break
    if frag == False:
        continue

    for month in date_range(fromMonth, toMonth):
        month = str(month)[0:7]
        fileName = "../data/"+CHANNEL_NAME+"/"+str(month)+".json"

        if os.path.isfile(fileName) != True:
            continue

        # html の head
        head = """
        <!DOCTYPE html>
        <meta charset="UTF-8">
        <html>
        <head>
        <link rel="stylesheet" href="style.css">
        </head>
        <header>
        <div class ="title">
            <h1>"""+CHANNEL_NAME+"""</h1>
        </div>
        </header>

        <body>
        """

        # html ファイル 追記モード
        htmlFileName = "../html/"+CHANNEL_NAME+".html"
        if os.path.isfile(htmlFileName) != True:
            htmlFile = open(htmlFileName, mode="w")
            htmlFile.write(head)
            htmlFile.close()

            htmlIndexFileName = "../index.html"
            htmlIndexFile = open(htmlIndexFileName, mode="a")
            htmlLink = """
            <div>
                <a href="./html/"""+CHANNEL_NAME+""".html">"""+CHANNEL_NAME+"""</a>
            </div>
            """
            htmlIndexFile.write(htmlLink)
            htmlIndexFile.close()

        htmlFile = open(htmlFileName, mode="a")

        f = open(fileName, "r", encoding="utf-8")
        fLoad = json.load(f)
        htmlFile.write("<br>\n<h3>"+month+"</h3>\n")

        fLoad = fLoad["messages"]

        for datas in list(reversed(fLoad)):

            htmlFile.write("<br><br>"+str(datas.get("user"))+"<br>")

            if "username" in datas.keys():
                htmlFile.write("<br><br>"+datas.get("username")+"<br>")
                if datas["username"] == "Trello":
                    htmlFile.write("<br>"+datas["attachments"]
                                   [0]["fallback"]+"<br>")
                    htmlFile.write(datas["attachments"][0]["text"])
                    continue
            if "files" in datas.keys():
                files = datas["files"]
                htmlFile.write("<br>"+files[0]["name"]+"<br>\n")
                if files[0].get("mode") == "hidden_by_limit":
                    htmlFile.write("<br>ファイルの容量制限（以前は制限があった。）のため削除されました。\n")

            if datas.get("subtype") == "channel_join":
                htmlFile.write(datas["text"])
                continue

            if datas.get("subtype") == "bot_message":
                htmlFile.write(datas["attachments"][0]["fallback"])
                continue

            if "blocks" not in datas.keys():
                continue
            elif datas["blocks"] == None:
                continue
            else:
                try:
                    blocks = datas["blocks"][0]
                except:
                    print(datas)
                    print(CHANNEL_NAME)
                    exit()

            if "elements" not in blocks.keys():
                continue
            else:
                elements = blocks["elements"][0]

            if elements.get("type") == "rich_text_section":
                elements = elements.get("elements")
                for element in elements:
                    writeFile(element, htmlFile)
                continue

            if "elements" not in elements.keys():
                continue
            else:
                elements = elements["elements"][0]

            writeFile(elements, htmlFile)

        f.close()
        htmlFile.close()
