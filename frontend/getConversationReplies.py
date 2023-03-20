import requests
from dotenv import load_dotenv
import os
from os.path import join, dirname
import json

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

channel_id = os.getenv("RANDOM_CHANNEL_ID")
url="https://slack.com/api/conversations.replies"
token=os.getenv("SLACK_USER_TOKEN")

# UNIX TIMESTAMP
# https://www.unixtimestamp.com/
ts=1677043294.073649

def main():
  payload={
    "channel":channel_id,
    "ts":ts
  }
  headersAuth = {
    "Authorization":"Bearer "+str(token),
  }

  response = requests.get(url,headers=headersAuth,params=payload)
  json_data = response.json()
  

  msgs=json_data["messages"]
  
  for data in msgs[2:]:
    print(data.keys())
    exit()

  # 現在ディレクトリに保存される
  with open('./sampleReplies.json',"w") as f:
    json.dump(msgs,f,ensure_ascii=False)

  return 0

if __name__=="__main__":
  main()