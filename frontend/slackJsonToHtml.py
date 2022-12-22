# -*- coding: utf-8 -*-

# import
import markdown
import json
import traceback
from datetime import date, timedelta
import emoji

# チャンネル名
chunnel = "sample"

# 変換先のマークダウンファイル
writeFileName = chunnel+".md"
fCh = open(writeFileName, mode="w")

# for 文を日付でまわすための関数


def date_range(start, stop, step=timedelta(1)):
    current = start
    while current < stop:
        yield current
        current += step


# 日付を指定する必要がある
dayStart = date(2022,12,16)
dayEnd = date(2022,12,21)

for date in date_range(dayStart, dayEnd):
    date = str(date)

    try:
        # fileName = "./"+chunnel+"/"+str(date)+".json"
        fileName = "/Users/kazuki_yabuuchi/Documents/GitHub/slackHistory/backend/"+str(date)+".json"
        f = open(fileName, "r", encoding="utf-8")
        fLoad = json.load(f)
        fCh.write("<br>")
        fCh.write('\n<h3>')
        fCh.write(date)
        fCh.write("</h3>\n")
        
        # go で取得した場合は変換する
        try:
            fLoad=fLoad["messages"]
        except:
            pass

        # try and except を酷使してデータを抽出
        # リアクションや返信であるかなどは未対応
        for j in range(len(fLoad)):

            datas = fLoad[j]

            try:
                fCh.write(datas["user"])
            except:
                fCh.write(datas["username"])
                if datas["username"] == "Trello":
                    fCh.write("<br>"+datas["attachments"]
                              [0]["fallback"]+"<br>")
                    fCh.write(datas["attachments"][0]["text"])
            try:
                fCh.write("<br>"+datas["files"][0]["name"])
                fCh.write("<br>\n")
            except:
                pass
            try:
                if datas["files"][0]["mode"] == "hidden_by_limit":
                    fCh.write("<br>ファイルの容量制限（以前は制限があった。）のため削除されました。\n")
            except:
                pass

            fCh.write("<br>\n")

            # ユーザー名がある時がたまにある
            # try:
            #     print(datas["user_profile"]["real_name"])
            # except:
            #     pass

            try:
                for data in datas["blocks"]:
                    try:
                        ele1s = data["elements"]
                        for ele1 in ele1s:
                            for ele2 in ele1["elements"]:
                                if ele2["type"] == "text":
                                    try:
                                        if ele2["style"]["bold"] == True:
                                            fCh.write("<strong>"+ele2["text"].replace("\n", "<br>").replace(
                                                "#", "\#").replace("    ", "")+"</strong>")
                                    except:
                                        try:
                                            if ele2["style"]["code"] == True:
                                                fCh.write("<code>"+ele2["text"].replace("\n", "<br>").replace(
                                                    "#", "\#").replace("    ", "")+"</code>")
                                        except:
                                            fCh.write(ele2["text"].replace("\n", "<br>").replace(
                                                "#", "\#").replace("    ", ""))

                                elif ele2["type"] == "link":
                                    # print(ele2["url"])
                                    fCh.write("<a href='"+ele2["url"]+"'>")
                                    fCh.write(ele2["url"])
                                    fCh.write("</a>")
                                    fCh.write("\n")
                                elif ele2["type"] == "emoji":
                                    fCh.write(emoji.emojize(":"+ele2["name"]+":"))
                                elif ele2["type"] == "user":
                                    fCh.write("@"+ele2["user_id"])
                                elif ele2["type"] == "broadcast":
                                    fCh.write("@"+ele2["range"])
                                elif ele2["type"] == "channel":
                                    fCh.write("\#"+ele2["channel_id"])
                                elif ele2["type"] == "rich_text_section":
                                    for ele3 in ele2["elements"]:
                                        if ele3["type"] == "text":
                                            try:
                                                if ele3["style"]["bold"] == True:
                                                    fCh.write("<strong>"+ele3["text"].replace("\n", "<br>").replace(
                                                        "#", "\#").replace("    ", "")+"</strong>")
                                            except:
                                                try:
                                                    if ele3["style"]["code"] == True:
                                                        fCh.write("<code>"+ele3["text"].replace("\n", "<br>").replace(
                                                            "#", "\#").replace("    ", "")+"</code>")
                                                except:
                                                    fCh.write(ele3["text"].replace("\n", "<br>").replace(
                                                        "#", "\#").replace("    ", ""))

                                        elif ele3["type"] == "link":
                                            # print(ele3["url"])
                                            fCh.write(
                                                "<a href='"+ele3["url"]+"'>")
                                            fCh.write(ele3["url"])
                                            fCh.write("</a>")
                                            fCh.write("\n")
                                        elif ele3["type"] == "emoji":
                                            fCh.write(emoji.emojize(":"+ele3["name"]+":"))
                                        elif ele3["type"] == "user":
                                            fCh.write("@"+ele3["user_id"])
                                        elif ele3["type"] == "broadcast":
                                            fCh.write("@"+ele3["range"])
                                        elif ele3["type"] == "channel":
                                            fCh.write("\#"+ele3["channel_id"])
                                        else:
                                            print(date)
                                            try:
                                                print(datas["user"])
                                            except:
                                                print(datas["username"])
                                            print(ele3)

                                else:
                                    print(date)
                                    try:
                                        print(datas["user"])
                                    except:
                                        print(datas["username"])
                                    print(ele2)

                            fCh.write("<br>")

                    except:
                        print(date)
                        try:
                            print(datas["user"])
                        except:
                            print(datas["username"])
                        print(ele1)
                        print(traceback.format_exc())
                        pass

            except:
                fCh.write(datas["text"].replace(
                    "\n\t", "<br>\n").replace("#", "/#"))

                try:
                    fCh.write(datas["files"][0]["name"])
                except:
                    pass
                f.close()
            fCh.write("<br><br>")

    except:
        # print(traceback.format_exc())
        # 該当する日付の JSON ファイルがなかった時
        pass


fCh.close()

# マークダウンファイルを HTML に変換

head = """<!DOCTYPE html>
<meta charset="UTF-8">
<html>
<head>
   <link rel="stylesheet" href="style.css">
</head>
<header>
   <div class ="title">
      <h1>"""+chunnel+"""</h1>
   </div>
</header>

<body>"""

tail = """
</body>
</html>"""

f = open(writeFileName, "r")
fHtml = open(chunnel+".html", "w")
lines = f.read()

md = markdown.Markdown()
fHtml.write(head)
fHtml.write(md.convert(lines))
fHtml.write(tail)

fHtml.close()
f.close()
