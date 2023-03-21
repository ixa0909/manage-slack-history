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

# 環境変数の読み込み
load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)
TOKEN = os.getenv("SLACK_USER_TOKEN")


# for 文を日付で 1 ヶ月ごとにまわすための関数
def date_range(start, stop, step=relativedelta(months=1)):
    current = start
    while current < stop:
        yield current
        current += step


# 末尾に改行ありのファイルへの書き込み
def writeln(file, text):
    file.write(text+"\n")


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
        writeln(file, "<url><a href='"+link+"'>"+link+"</a></url>")

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


def writeRepliesFile(replies, htmlFile, hasReplies,channel_name,reply_id):

    if hasReplies == False:
        return 0
    
    id = channel_name +"-"+reply_id
    htmlFile.write("\n<br><input type=\"button\" value=\"返信\" onclick=\"test(\'"+id+"\')\">")
    
    htmlFile.write("<replies id=\'"+id+"\'>\n")
    for reply in replies:
        # 送信者のユーザーID
        htmlFile.write("<br><br>"+"<user>" +
                       str(reply.get("user"))+"</user>"+"<br>\n")

        # ユーザー名がある場合
        if "username" in reply.keys():
            htmlFile.write("<br><br>"+"<user>" +
                           reply.get("username")+"</user>"+"<br>")
            # Trello からの通知の場合
            if reply["username"] == "Trello":
                htmlFile.write("<trello>"+"<br>"+reply["attachments"]
                               [0]["fallback"]+"<br>"+reply["attachments"][0]["text"]+"</trello>")

        # ファイルを添付している場合
        if "files" in reply.keys():
            files = reply["files"][0]
            if files.get("mode") == "tombstone":
                htmlFile.write("<br>表示期間が終了しています<br>\n"+"<br>" +
                               "ファイル ID: "+files.get("id")+"<br>\n")
            else:
                htmlFile.write("<br><file>"+files.get("name")+"</file><br>\n")
                if files.get("mode") == "hidden_by_limit":
                    # 以前のプランではファイルの容量制限により過去のファイルが削除されていた
                    htmlFile.write("<br>ファイルの容量制限による非表示\n")
        # チャンネル参加メッセージ
        subtype = reply.get("subtype")

        if subtype == "thread_broadcast":
            pass
        # ボットのメッセージ
        elif subtype == "bot_message":
            htmlFile.write(
                "<bot>"+reply["attachments"][0]["fallback"]+"</bot>")
        elif subtype == None:
            pass
        else:
            # 未知のもの
            print(subtype)

        # テキストメッセージがない場合
        if reply.get("blocks") == None:
            continue
        # テキストメッセージがある場合
        else:
            blocks = reply["blocks"][0]

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

        # html ファイルへの書き込み
        writeFile(elements, htmlFile)

    htmlFile.write("</replies>\n")


def makeHtmlFile():
    # チャンネル一覧の読み込み
    channelFile = open("../data/channels.json", "r")
    channels = json.load(channelFile)
    channelFile.close()

    # 投稿に対する返信を取得する API の URL
    url = "https://slack.com/api/conversations.replies"

    print("対象チャンネル")
    # チャンネルごとに html を作成
    for CHANNEL_INFO in channels:
        # チャンネル ID とチャンネル名
        CHANNEL_ID = CHANNEL_INFO["id"]
        CHANNEL_NAME = CHANNEL_INFO["name"]

        # 今月と先月の初日 (1 日)
        today = datetime.date.today()
        MonthAgo = today+relativedelta(months=-1)
        toMonth = date(today.year, today.month, 1)
        fromMonth = date(MonthAgo.year, MonthAgo.month, 1)

        # 1 ヶ月ごとに書き込み
        for month in date_range(fromMonth, toMonth):
            # 西暦と月を用いてファイル名を指定
            month = str(month)[0:7]
            fileName = "../data/"+CHANNEL_NAME+"/"+str(month)+".json"

            # 新規メッセージが無ければ更新無し
            if os.path.isfile(fileName) != True:
                continue
            print(CHANNEL_NAME)

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

            # 新チャンネルの場合
            if os.path.isfile(htmlFileName) != True:
                # html ファイルを新規作成
                htmlFile = open(htmlFileName, mode="w")
                htmlFile.write(head)
                htmlFile.close()

                # 目次ページへの追記
                htmlIndexFileName = "../index.html"
                htmlIndexFile = open(htmlIndexFileName, mode="a")
                # 各チャンネルごとのページへのリンク
                htmlLink = """
                <div>
                    <a href="./html/"""+CHANNEL_NAME+""".html">"""+CHANNEL_NAME+"""</a>
                </div>
                """
                htmlIndexFile.write(htmlLink)
                htmlIndexFile.close()

            # 履歴データの読み込み
            f = open(fileName, "r", encoding="utf-8")
            messages = json.load(f)["messages"]
            f.close()

            # メッセージを追記モードで書き込み
            htmlFile = open(htmlFileName, mode="a")
            htmlFile.write("<br>\n<h3>"+month+"</h3>\n")

            # 各メッセージごとに処理 ※ データが新→古の順であるため逆順で処理
            for datas in list(reversed(messages)):
                # 送信者
                htmlFile.write("<br><br>"+str(datas.get("user"))+"<br>\n")

                # ユーザー名がある場合
                if "username" in datas.keys():
                    htmlFile.write("<br><br>"+datas.get("username")+"<br>")
                    # Trello からの通知の場合
                    if datas["username"] == "Trello":
                        htmlFile.write("<br>"+datas["attachments"]
                                       [0]["fallback"]+"<br>")
                        htmlFile.write(datas["attachments"][0]["text"])

                # ファイルを添付している場合
                if "files" in datas.keys():
                    files = datas["files"]
                    htmlFile.write("<br>"+files[0]["name"]+"<br>\n")
                    if files[0].get("mode") == "hidden_by_limit":
                        htmlFile.write(
                            "<br>ファイルの容量制限（以前は制限があった。）のため削除されました。\n")

                # チャンネル参加メッセージ
                subtype = datas.get("subtype")
                if subtype == "channel_join":
                    htmlFile.write(datas["text"])
                # チャンネル退出メッセージ
                elif subtype == "channel_exit":
                    htmlFile.write(datas["text"])
                # ボットのメッセージ
                elif subtype == "thread_broadcast":
                    pass
                elif subtype == "bot_message":
                    htmlFile.write(datas["attachments"][0]["fallback"])
                elif subtype == None:
                    pass
                else:
                    print(subtype)

                # 投稿メッセージへの返信履歴の取得
                if "reply_count" in datas.keys():
                    hasReplies = True

                    # 送信時刻 UNIX
                    ts = datas["ts"]

                    params = {
                        "channel": CHANNEL_ID,
                        "ts": ts,
                        "inclusive": True
                    }
                    headersAuth = {
                        "Authorization": "Bearer "+str(TOKEN),
                    }
                    # api を用いた返信履歴の取得
                    response = requests.get(
                        url, headers=headersAuth, params=params)
                    # サーバ負荷対策
                    sleep(2)
                    replies = response.json()["messages"][1:]
                    reply_id=datas["client_msg_id"]

                else:
                    hasReplies = False
                    replies = 0
                    reply_id = None

                # テキストメッセージがない場合
                if datas.get("blocks") == None:
                    writeRepliesFile(replies, htmlFile, hasReplies,CHANNEL_NAME,reply_id)
                    continue
                # テキストメッセージがある場合
                else:
                    blocks = datas["blocks"][0]

                if "elements" not in blocks.keys():
                    writeRepliesFile(replies, htmlFile, hasReplies,CHANNEL_NAME,reply_id)
                    continue
                else:
                    elements = blocks["elements"][0]

                if elements.get("type") == "rich_text_section":
                    elements = elements.get("elements")
                    for element in elements:
                        writeFile(element, htmlFile)
                    writeRepliesFile(replies, htmlFile, hasReplies,CHANNEL_NAME,reply_id)
                    continue

                if "elements" not in elements.keys():
                    writeRepliesFile(replies, htmlFile, hasReplies,CHANNEL_NAME,reply_id)
                    continue
                else:
                    elements = elements["elements"][0]

                # html ファイルへの書き込み
                writeFile(elements, htmlFile)
                writeRepliesFile(replies, htmlFile, hasReplies,CHANNEL_NAME,reply_id)

            f.close()
            htmlFile.close()


# time ticker 初回実行まで時間を空けてから一ヶ月ごとに
# 何日後に実行するのか
print("初回の実行までの時間: ")
initialTimer = int(input())
print("日後にプログラムを実行")

sleep(initialTimer*3600)

while (1):
    now = datetime.datetime.now()
    print("HTML 記入開始: "+str(now))
    afterMonth = now+relativedelta(months=1)
    timer = (afterMonth-now).days*3600
    makeHtmlFile()
    print("記入終了: "+str(datetime.datetime.now()))
    print("次回記入予定時刻: "+str(afterMonth))
    sleep(timer)
