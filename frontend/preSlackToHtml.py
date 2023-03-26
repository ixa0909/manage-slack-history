# -*- coding: utf-8 -*-

# import
# データ処理
import json
import emoji

# 時刻処理
from datetime import date
from dateutil.relativedelta import relativedelta
import datetime

# 環境変数
import os
from os.path import join, dirname
from dotenv import load_dotenv

# 投稿への返信データを取得する GET 送信
import requests
from time import sleep
import traceback

import queue

# 環境変数の読み込み
load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)
TOKEN = os.getenv("SLACK_USER_TOKEN")


# for 文を日付で 1 日ごとにまわすための関数
def date_range_day(start, stop, step=relativedelta(days=1)):
    current = start
    while current < stop:
        yield current
        current += step


# for 文を日付で 1 ヶ月ごとにまわすための関数
def date_range_month(start, stop, step=relativedelta(months=1)):
    current = start
    while current < stop:
        yield current
        current += step


# 末尾に改行ありのファイルへの書き込み
def writeln(file, text):
    file.write(text+"\n")


# href 形式でファイルに書き込み
def writeLink(file, link):
    writeln(file, "<url><a href='"+link+"'>"+link+"</a></url>")


def writeAttachment(file, CHANNEL_NAME, attachments, ts, isTrello):
    for i, attachment in enumerate(attachments):
        # ボタン
        id = CHANNEL_NAME + "-" + \
            str(ts).replace(".", "")+"-"+str(i)
        writeln(file,
                "<input class=\"btn\" type=\"button\" value=\"表示・非表示\" onclick=\"attachments_display(\'"+id+"\')\">")
        writeln(file, "<attachments id=\""+id+"\">")

        # 概要
        factor = {}
        factor["title"] = attachment.get("title")
        factor["author_name"] = attachment.get(
            'author_name')

        factor["fallback"] = attachment.get('fallback')

        factor["text"] = attachment.get("text")
        factor["pretext"] = attachment.get("pretext")
        factor["url"] = attachment.get(
            "author_link")

        writeln(file, "<div class=\"attachments_text\">")
        for key in factor.keys():
            # if factor[key] == None: continue
            if key == "url" and factor[key] != None:
                writeLink(file, factor[key])
                continue
            writeln(file, "<"+key+">" +
                    str(factor[key])+"</"+key+">")
        writeln(file, "</div>")
        if isTrello:
            file_name = "../file/"+"trello.png"
            writeln(file,
                    "<img class=\"attachments_img\" src="+file_name+">")
        else:
            thumb_url = attachment.get("thumb_url")
            if thumb_url != None:
                thumb_url = thumb_url.replace(r"\/", "/")
                sleep(2)
                response = requests.get(thumb_url)
                image = response.content
                file_name = "../file/"+CHANNEL_NAME + \
                    "/"+thumb_url.replace(r"/", "_")
                with open(file_name, "wb") as image_file:
                    image_file.write(image)
                writeln(file,
                        "<img class=\"attachments_img\" src="+file_name+">")
        writeln(file, "</attachments>")


# html ファイルへのメッセージの書き込み
def writeFile(elements, file):
    # テキストメッセージの場合
    if elements["type"] == "text":
        # 文字の置換
        text = elements["text"].replace("\n", "<br>").replace(
            "#", "\#").replace("    ", "")

        # 文字のスタイル 太文字 / コードブロック / 打ち消し線の順 / 未知のタグ の順
        if "style" in elements.keys():
            style = elements["style"]
            if style.get("bold") == True:
                tag = "strong"
            elif style.get("code") == True:
                tag = "code"
            elif style.get("strike") == True:
                tag = "strike"
            else:
                tag = "strong"

            writeln(file, "<"+tag+">"+text+"</"+tag+">")
        else:
            writeln(file, text)

    # リンクの場合
    elif elements["type"] == "link":
        link = elements["url"]
        writeLink(file, link)

    # 絵文字の場合
    elif elements["type"] == "emoji":
        name = elements["name"].replace(
            "man-bowing", "bowing_man").replace("woman-bowing", "bowing_woman")
        file.write("<emoji>"+emoji.emojize(':'+name +
                   ':', language='alias')+"</emoji>")

    # メンションの場合
    elif elements["type"] == "user":
        file.write("<mention>"+"@"+elements["user_id"]+"</mention>")
    elif elements["type"] == "broadcast":
        file.write("<mention>"+"@"+elements["range"]+"</mention>")
    elif elements["type"] == "channel":
        file.write("<mention>"+"\#"+elements["channel_id"]+"</mention>")


def writeReplyFile(reply, htmlFile):

    # 送信者のユーザーID
    writeln(htmlFile, "<br>ユーザー ID: <user_id>" +
            str(reply.get("user"))+"</user_id>"+"<br>\n")

    # ユーザー名がある場合
    if "username" in reply.keys():
        writeln(htmlFile, "<user>" +
                reply.get("username")+"</user>")

    # ファイルを添付している場合
    if "files" in reply.keys():
        files = reply["files"][0]
        if files.get("mode") == "tombstone":
            writeln(htmlFile, "表示期間が終了しています\n"++
                    "ファイル ID: "+files.get("id"))
        else:
            writeln(htmlFile, "<file>"+str(files.get("name"))+"</file>")
            if files.get("mode") == "hidden_by_limit":
                # 以前のプランではファイルの容量制限により過去のファイルが削除されていた
                writeln(htmlFile, "ファイルの容量制限による非表示")

    # チャンネル参加メッセージ
    subtype = reply.get("subtype")
    message_type = reply.get("type")
    if subtype == "channel_join":
        writeln(htmlFile, reply["text"])
    # チャンネル退出メッセージ
    elif subtype == "channel_leave":
        writeln(htmlFile, reply["text"])
    elif subtype == "thread_broadcast":
        pass
    # ボットのメッセージ
    elif subtype == "bot_message" and message_type == "message":
        writeln(htmlFile,
                "<bot>"+reply["text"]+"</bot>")
    elif subtype == "bot_message":
        writeln(htmlFile,
                "<bot>"+reply["attachments"][0]["fallback"]+"</bot>")
    elif subtype == None:
        pass
    else:
        # 未知のもの
        print(subtype)

    # html ファイルへの書き込み
    # テキストメッセージがない場合
    if reply.get("blocks") == None:
        return 0
    # テキストメッセージがある場合
    else:
        blocks = reply["blocks"][0]

    if "elements" not in blocks.keys():
        return 0
    else:
        elements = blocks["elements"][0]

    if elements.get("type") == "rich_text_section":
        elements = elements.get("elements")
        for element in elements:
            writeFile(element, htmlFile)

        return 0
    if "elements" not in elements.keys():

        return 0
    else:
        elements = elements["elements"][0]

    # html ファイルへの書き込み

    writeFile(elements, htmlFile)


def makeHtmlFile():
    # チャンネル一覧の読み込み
    channelFile = open("../data/channels.json", "r")
    channels = json.load(channelFile)
    channelFile.close()

    # 投稿に対する返信を取得する API の URL
    url = "https://slack.com/api/conversations.replies"

    # 今月と先月の初日 (1 日)
    today = datetime.date.today()
    MonthAgo = today+relativedelta(months=-1)
    toMonth = date(today.year, today.month, 1)
    fromMonth = date(MonthAgo.year, MonthAgo.month, 1)

    print("対象チャンネル")
    # チャンネルごとに html を作成
    count = 0
    for CHANNEL_INFO in channels:
        # チャンネル ID とチャンネル名

        CHANNEL_NAME = CHANNEL_INFO["name"]

        CHANNEL_NAME = "random"
        if count == 1:
            return 0
        count += 1

        # html の先頭部分
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
            <script type="text/javascript" src="script.js"></script>
        """

        # html ファイル
        htmlFileName = "../html/"+CHANNEL_NAME+".html"
        dataDirName = "../data/"+CHANNEL_NAME
        if os.path.isdir(dataDirName) != True:
            continue
        file_directory_name = "../file/"+CHANNEL_NAME
        if os.path.isdir(file_directory_name) != True:
            os.makedirs(file_directory_name)

        # 新チャンネルの場合
        if os.path.isfile(htmlFileName) != True:
            # html ファイルを新規作成
            htmlFile = open(htmlFileName, mode="w")
            writeln(htmlFile, head)
            htmlFile.close()

            # 目次ページへの追記
            htmlIndexFileName = "../index.html"
            htmlIndexFile = open(htmlIndexFileName, mode="a")
            # 各チャンネルごとのページへのリンク
            htmlLink = """
            <div>
                <a href="../html/"""+CHANNEL_NAME+""".html">"""+CHANNEL_NAME+"""</a>
            </div>
            """
            htmlIndexFile.write(htmlLink)
            htmlIndexFile.close()

        # 日付を指定する必要がある
        # dayStart = date(2023, 2, 14)
        # dayEnd = date(2023, 2, 19)
        dayStart = date(2017, 8, 5)
        dayEnd = date(2023, 3, 15)
        reply_count = 0

        thread_ts = None

        store_posts = []
        store_replies = queue.Queue()

        for day in date_range_day(dayStart, dayEnd):

            day = str(day)
            fileName = "../data/"+CHANNEL_NAME+"/"+str(day)+".json"
            # 新規メッセージが無ければ更新無し
            if os.path.isfile(fileName) != True:
                continue

            # メッセージを追記モードで書き込み
            htmlFile = open(htmlFileName, mode="a")
            # 履歴データの読み込み
            f = open(fileName, "r", encoding="utf-8")
            messages = json.load(f)
            f.close()

            # 投稿と返信に分類
            for data in messages:
                # 返信
                if "thread_ts" in data.keys() and "reply_count" not in data.keys():
                    store_replies.put(data)
                else:
                    store_posts.append(data)

        focus_day = None
        for post in store_posts:

            # 送信時刻
            ts_str = post.get("ts")
            ts = float(ts_str)
            dt = datetime.datetime.fromtimestamp(ts)
            date_time = dt.strftime("%Y-%m-%d %H:%M:%S")
            if focus_day != date_time[:10]:
                focus_day = date_time[:10]
                writeln(htmlFile, "<date>"+focus_day+"</date>")

            writePost(htmlFile, post, date_time, CHANNEL_NAME, ts)

            id = CHANNEL_NAME + "-" + \
                ts_str.replace(".", "")
            # 返信のある投稿
            if "reply_count" in post.keys():

                thread_ts = post["thread_ts"]
                reply_count = post["reply_count"]

                writeln(
                    htmlFile, "\n<br><input class=\"btn\" type=\"button\" value=\"返信\" onclick=\"test(\'"+id+"\')\">")
                writeln(htmlFile, "<replies id=\'"+id+"\'>\n")

                for _ in range(store_replies.qsize()):
                    reply = store_replies.get()
                    if thread_ts == reply["thread_ts"]:
                        writeReplyFile(reply, htmlFile)
                        reply_count -= 1
                    else:
                        store_replies.put(reply)

                writeln(htmlFile, "</replies>\n")

        htmlFile.close()


def writePost(file, post, date_time, channel_name, ts):

    # 送信者 ID
    user_id = str(post.get("user"))
    writeln(file, "<br><br>ユーザー ID: <user_id>" +
            user_id+"</user_id>")

    # 送信時刻
    writeln(file, "<ts>"+date_time+"</ts>")

    # 送信者名
    user_profile = post.get("user_profile")
    if user_profile != None:
        display_name = user_profile.get("display_name")
        writeln(file, "<user>"+display_name+"</user>")

    # ユーザー名がある場合
    if "username" in post.keys():
        writeln(file, "<user>" +
                post.get("username")+"</user>")

    # ファイルを添付している場合
    if "files" in post.keys():
        files = post["files"]
        writeln(file, "<file>" +
                str(files[0].get("name"))+"</file>")

        if files[0].get("mode") == "hidden_by_limit":
            writeln(file,
                    "<br>ファイルの容量制限による非表示\n")

    # チャンネル参加メッセージ
    subtype = post.get("subtype")
    message_type = post.get("type")
    if subtype == "channel_join":
        writeln(file, post["text"])
    # チャンネル退出メッセージ
    elif subtype == "channel_leave":
        writeln(file, post["text"])
    # ボットのメッセージ
    elif subtype == "thread_broadcast":
        pass
    elif subtype == "bot_message" and message_type == "message":
        writeln(file, post["text"])
    elif subtype == "bot_message":
        writeln(file, post["attachments"][0]["fallback"])
    elif subtype == None:
        pass
    else:
        print(subtype)

    
    # テキストメッセージがない場合
    if post.get("blocks") == None:
        return 0
    # テキストメッセージがある場合
    else:
        blocks = post["blocks"][0]

    if "elements" not in blocks.keys():

        return 0
    else:
        elements = blocks["elements"][0]

    if elements.get("type") == "rich_text_section":
        elements = elements.get("elements")
        for element in elements:
            writeFile(element, file)
        # 添付 URL の概要
        attachments = post.get("attachments")
        if attachments != None and post.get("username") != "Trello":
            isTrello = False
            writeAttachment(file, channel_name,
                            attachments, ts, isTrello)
        elif post.get("username") == "Trello":
            isTrello = True
            writeAttachment(file, channel_name,
                            attachments, ts, isTrello)
        return 0

    if "elements" not in elements.keys():

        return 0
    else:
        elements = elements["elements"][0]

    # html ファイルへの書き込み
    writeFile(elements, file)
    # 添付 URL の概要
    attachments = post.get("attachments")
    if attachments != None and post.get("username") != "Trello":
        isTrello = False
        writeAttachment(file, channel_name,
                        attachments, ts, isTrello)
    elif post.get("username") == "Trello":
        isTrello = True
        writeAttachment(file, channel_name,
                        attachments, ts, isTrello)


# main 関数
makeHtmlFile()
