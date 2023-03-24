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


def writeReplyFile(reply, htmlFile, hasReplies, channel_name):
    if hasReplies == 0:
        return 0

    # 送信者のユーザーID
    writeln(htmlFile, "<user>" +
            str(reply.get("user"))+"</user>"+"<br>\n")

    # ユーザー名がある場合
    if "username" in reply.keys():
        writeln(htmlFile, "<user>" +
                reply.get("username")+"</user>")
        # Trello からの通知の場合
        if reply["username"] == "Trello":
            writeln(htmlFile, "<trello>"+reply["attachments"]
                    [0]["fallback"]+reply["attachments"][0]["text"]+"</trello>")

    # ファイルを添付している場合
    if "files" in reply.keys():
        files = reply["files"][0]
        if files.get("mode") == "tombstone":
            writeln(htmlFile, "表示期間が終了しています\n"++
                    "ファイル ID: "+files.get("id"))
        else:
            writeln(htmlFile, "<file>"+files.get("name")+"</file>")
            if files.get("mode") == "hidden_by_limit":
                # 以前のプランではファイルの容量制限により過去のファイルが削除されていた
                writeln(htmlFile, "ファイルの容量制限による非表示")
    # チャンネル参加メッセージ
    subtype = reply.get("subtype")

    if subtype == "thread_broadcast":
        pass
    # ボットのメッセージ
    elif subtype == "bot_message":
        writeln(htmlFile,
                "<bot>"+reply["attachments"][0]["fallback"]+"</bot>")
    elif subtype == None:
        pass
    else:
        # 未知のもの
        print(subtype)

    # html ファイルへの書き込み
    writeln(htmlFile, reply.get("text"))


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
        CHANNEL_ID = CHANNEL_INFO["id"]
        CHANNEL_NAME = CHANNEL_INFO["name"]
        CHANNEL_ID = "C3PRX5C9H"
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
        # dayStart = date(2018, 10, 15)
        # dayEnd = date(2018, 10, 17)
        dayStart = date(2017, 1, 10)
        dayEnd = date(2023, 3, 16)
        reply_count = 0
        # 1 日ごとに書き込み
        for day in date_range_day(dayStart, dayEnd):
            try:

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

                writeln(htmlFile, "<date>"+day+"</date>")
                
                # 各メッセージごとに処理
                for datas in messages:
                    
                    if reply_count != 0:
                        writeReplyFile(datas, htmlFile,
                                       hasReplies, CHANNEL_NAME)
                        if reply_count == 1:
                            writeln(htmlFile, "</replies>\n")

                        reply_count -= 1
                        continue

                    # 送信者 ID
                    user_id = str(datas.get("user"))
                    writeln(htmlFile, "<user_id>"+user_id+"</user_id>")

                    # 送信時刻
                    ts = datas.get("ts")
                    writeln(htmlFile, "<ts>"+str(ts)+"</ts>")

                    # 送信者名
                    user_profile = datas.get("user_profile")
                    if user_profile != None:
                        display_name = user_profile.get("display_name")
                        writeln(htmlFile, "<user>"+display_name+"</user>")

                    # 添付 URL の概要
                    attachments = datas.get("attachments")
                    if attachments != None:
                        for i, attachment in enumerate(attachments):
                            # ボタン
                            id = CHANNEL_NAME + "-" + \
                                str(ts).replace(".", "")+"-"+str(i)
                            writeln(htmlFile,
                                    "<input class=\"btn\" type=\"button\" value=\"URL 概要\" onclick=\"attachments_display(\'"+id+"\')\">")
                            writeln(htmlFile, "<attachments id=\""+id+"\">")
                            # 概要
                            title = attachment.get("title")
                            text = attachment.get("text")
                            writeln(htmlFile,
                                    "<div class=\"attachments_text\">\n"+"<title>"+str(title)+"</title>\n"+str(text)+"</div>")
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
                                writeln(htmlFile,
                                        "<img class=\"attachments_img\" src="+file_name+">")
                            writeln(htmlFile, "</attachments>")

                    # ユーザー名がある場合
                    if "username" in datas.keys():
                        writeln(htmlFile, "<user>" +
                                datas.get("username")+"</user>")
                        # Trello からの通知の場合
                        if datas["username"] == "Trello":
                            writeln(htmlFile, datas["attachments"]
                                    [0]["fallback"])
                            writeln(htmlFile, datas["attachments"][0]["text"])

                    # ファイルを添付している場合
                    if "files" in datas.keys():
                        files = datas["files"]
                        writeln(htmlFile, "<file>" +
                                str(files[0].get("name"))+"</file>")

                        if files[0].get("mode") == "hidden_by_limit":
                            writeln(htmlFile,
                                    "<br>ファイルの容量制限（以前は制限があった。）のため削除されました。\n")

                    # チャンネル参加メッセージ
                    subtype = datas.get("subtype")
                    if subtype == "channel_join":
                        writeln(htmlFile, datas["text"])
                    # チャンネル退出メッセージ
                    elif subtype == "channel_leave":
                        writeln(htmlFile, datas["text"])
                    # ボットのメッセージ
                    elif subtype == "thread_broadcast":
                        pass
                    elif subtype == "bot_message":
                        writeln(htmlFile, datas["attachments"][0]["fallback"])
                    elif subtype == None:
                        pass
                    else:
                        print(subtype)

                    # 投稿メッセージへの返信履歴の取得
                    if "reply_count" in datas.keys():
                        reply_count = datas["reply_count"]
                        hasReplies = True
                        

                    else:
                        hasReplies = False
                        replies = 0

                    # テキストメッセージがない場合
                    if datas.get("blocks") == None:

                        continue
                    # テキストメッセージがある場合
                    else:
                        blocks = datas["blocks"][0]

                    if "elements" not in blocks.keys():
                        continue
                    else:
                        elements = blocks["elements"][0]

                    if elements.get("type") == "rich_text_section":
                        elements = elements.get("elements")
                        for element in elements:
                            writeFile(element, htmlFile)
                        if hasReplies:
                            id = CHANNEL_NAME + "-" + \
                            str(datas["ts"]).replace(".", "")
                            writeln(htmlFile,
                                    "\n<br><input class=\"btn\" type=\"button\" value=\"返信\" onclick=\"test(\'"+id+"\')\">")

                            writeln(htmlFile, "<replies id=\'"+id+"\'>\n")
                        continue

                    if "elements" not in elements.keys():

                        continue
                    else:
                        elements = elements["elements"][0]

                    # html ファイルへの書き込み
                    writeFile(elements, htmlFile)
                    if hasReplies:
                        id = CHANNEL_NAME + "-" + \
                        str(datas["ts"]).replace(".", "")
                        writeln(htmlFile,
                                "\n<br><input class=\"btn\" type=\"button\" value=\"返信\" onclick=\"test(\'"+id+"\')\">")

                        writeln(htmlFile, "<replies id=\'"+id+"\'>\n")
                    # writeReplyFile(replies, htmlFile, hasReplies,
                    #  CHANNEL_NAME)
            except:
                print(traceback.format_exc())
                exit()

            htmlFile.close()


makeHtmlFile()
