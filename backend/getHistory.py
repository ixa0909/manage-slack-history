import requests
from dotenv import load_dotenv
import os
import json

load_dotenv(override=True)

channel_id = os.getenv("CHANNEL")
# https://api.slack.com/methods/conversations.history
url="https://slack.com/api/conversations.history"
token=os.getenv("SLACK_BOT_TOKEN")

# UNIX TIMESTAMP
# https://www.unixtimestamp.com/
start="1661443031"
end="1661529431"

def main():
  payload={
    "channel": channel_id,
    "oldest":start,
    "latest":end,
    "limit":100,
    "inclusive":True
  }
  headersAuth = {
    "Authorization":"Bearer "+str(token),
  }

  response = requests.get(url,headers=headersAuth,params=payload)
  json_data = response.json()

  msgs=json_data["messages"]

  # 現在ディレクトリに保存される
  with open('./sample.json',"w") as f:
    json.dump(msgs,f,ensure_ascii=False)

  return 0

if __name__=="__main__":
  main()