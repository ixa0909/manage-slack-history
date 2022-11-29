#!/bin/bash
# .env ファイルの読み込み
# source は/bash じゃない場合にエラーが起きるとのことなので注意
source ./.env

curl -X POST 'https://slack.com/api/chat.postMessage' \
-d token=$SLACK_BOT_TOKEN \
-d channel=$DEV_CHANNEL_NAME \
-d text="*gargag*"