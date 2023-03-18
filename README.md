# slackHistory

<p align="center">
<img src = "./images/flow.png" style ="width:350pt;height:auto;" />
</p>

<p align="center">
図1: 作成する API の動き
</p>

## 概要

無料[プラン](https://app.slack.com/plans/T3P7YJH4H?geocode=ja-jp)ではトーク履歴（以下、履歴と呼びます。）が 3 ヶ月ごとに消えてしまいます。自動で履歴を保存し、振り返れるようにすることが目的です。<br>
履歴を得るには 手動と Slack API による 2 つの方法があり、手動の場合は zip フォルダ、Slack API の場合は GET メソッドによる JSON 形式のデータ となります。<br>

**バックエンド**とは Slack API を用いて履歴を json ファイル出力する機能のことです。ビジネスプランでは履歴の出力をスケジューリングできるようなので、無料プランでそれを可能にします。出力の対象を API ごとに分けると<br>

- トーク履歴（ファイルのダウンロード用 URL 込み）
- ユーザー名
- チャンネル名
- 絵文字

これら 4 つとなり、作成する API を実行すると[図1](https://github.com/1g-hub/slackHistory/blob/develop/images/flow.png)に示す動きを 60 日ごとにし、[こちら](#gui-で手動による履歴取得)のような構成を持つディレクトリに対して追記させます。<br>
ただし、日付ごとにファイルを分けるのではなく 2 ヶ月分をまとめる予定です。HTML で表示する際に日付ごとに分けます。<br>

**フロントエンド**とは json ファイルから Slack のトーク画面を再現する機能のことです。<br>
バックエンドの機能で取得した json 形式のデータを元に HTML で見やすくします。Slack で表示しているような画面を再現、またはそれ以上に見やすいものにすることを考えています。

### ディレクトリ構成

```:バックエンド
backend
├── exampleCode
│   参考コード
├── main
│   main 機能
├── other
│   Python で履歴を取得コード　など
├── slackModule
│   Go のモジュール
├── typeChange
│   Go のモジュール
├── reference.txt
│   参考文献
└── todo.txt
    Todo
```

```:フロントエンド
frontend
├── slackJsonToHtml.py
│   Json → Markdown → HTML の順で変換
└── style.css
```

### 開発環境

```:開発環境
OS Mac M1
go version go1.18.4 darwin/arm64
Python 3.11.0
```

#### 2017年 ~ 2023年3月中旬の履歴データについて

GUI で プランが変更される前に取得した際のデータ（2017年 ~ 2023 年 3 月中旬）は `umr` 上の 以下の構成を持つ `Slack/` にあります。

```:GUI で履歴を出力
Slack/
├── 1G-member...
    ├── general
    ├── random
    │ 　　├── 2022-12-11.json
    │ 　　├── 2022-12-15.json
    │ 　　├── 2022-01-02.json
    │ 　　├── ・
    │ 　　├── ・
    ├・
    ├・
    ├── group-b3
    ├── group-ml
    │   取得する期間内で会話があったチャネルのトーク履歴が日毎に JSON ファイルで作成される。
    │   トーク履歴も会話があった日付のもののみである。
    ├── channels.json
    │   チャンネル情報
    ├── emoji.json
    │   オリジナルの絵文字情報
    ├── integrationlogs.json
    │   API の作成、更新履歴
    └── users.json
        ユーザー情報

├── SlackArchivedFiles
    ├── general
    ├── random
    │ 　　├── a.pdf
    │ 　　├── b.png
    │ 　　├── c.png
    │ 　　├── ・
    │ 　　├── ・
    ├・
    ├・
    ├── group-b3
    ├── group-ml
    送信されたファイルをチャンネルごとに保存。
```

#### GUI で手動による履歴取得

[手動で履歴を取得する場合](https://slack.com/intl/ja-jp/help/articles/201658943-%E3%83%AF%E3%83%BC%E3%82%AF%E3%82%B9%E3%83%9A%E3%83%BC%E3%82%B9%E3%81%AE%E3%83%87%E3%83%BC%E3%82%BF%E3%82%92%E3%82%A8%E3%82%AF%E3%82%B9%E3%83%9D%E3%83%BC%E3%83%88%E3%81%99%E3%82%8B)は以下の構成を持つ zip ファイルをダウンロードすることができます。

```:GUI で履歴を出力
/
├── general
├── random
│ 　　├── 2022-12-11.json
│ 　　├── 2022-12-15.json
│ 　　├── 2022-01-02.json
│ 　　├── ・
│ 　　├── ・
├・
├・
├── group-b3
├── group-ml
│   取得する期間内で会話があったチャネルのトーク履歴が日毎に JSON ファイルで作成される。
│   トーク履歴も会話があった日付のもののみである。
├── channels.json
│   チャンネル情報
├── integrationlogs.json
│   API の作成、更新履歴
└── users.json
    ユーザー情報
```

### 備考

### 進み具合
返信を除けば timeticke を実装すれば一旦区切りがつく


### 次の作業

- 実行環境をどうするのか
- time ticker で定期的にプログラムを実行
- 投稿に対する返信の履歴を取得できるようにする
- フロントエンドを見やすくデザインする
- コードの整理
- ファイルも別でダウンロードして保存しておく

### go 
```
go mod init main
go mod edit -replace=typeChange=../typeChange
go mod edit -replace=slackModules=../slackModules
go mod tidy
go build
./main
```
