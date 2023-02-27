package slackModules

import (
	"encoding/json"
	"fmt"
	"os"
	"strconv"
	"time"

	"typeChange"
	"github.com/joho/godotenv"
	"github.com/slack-go/slack"
)

func GetHistory(mapChannels map[string]string) {

	// トークンやチャンネル ID をロード
	godotenv.Load("./.env")
	TOKEN := os.Getenv("SLACK_USER_TOKEN")
	// api 宣言
	api := slack.New(TOKEN)

	for k, v := range mapChannels {

		CHANNEL_ID := v
		// k = "random"
		// v = "C3PRX5C9H"

		// 取得開始日と取得終了日 time.Parse(フォーマット,時刻)
		fromDate, _ := time.Parse("2006-01", typeChange.TimeToString(time.Now().AddDate(0, -2, 0)))
		toDate := fromDate.AddDate(0, 2, 0)

		// 日付で for 文
		for date := fromDate; date.Unix() < toDate.Unix(); date = date.AddDate(0, 1, 0) {

			// サーバー負荷対策
			time.Sleep(time.Second * 2)

			// GetConversation のパラメータ値
			latest := strconv.FormatInt(typeChange.StrToUnix(date.AddDate(0, 1, 0)), 10)
			limit := 1000
			oldest := strconv.FormatInt(typeChange.StrToUnix(date), 10)
			p := slack.GetConversationHistoryParameters{
				ChannelID:          CHANNEL_ID,
				Cursor:             "",
				Inclusive:          true,
				Latest:             latest,
				Limit:              limit,
				Oldest:             oldest,
				IncludeAllMetadata: true,
			}

			// 履歴を取得
			history, err := api.GetConversationHistory(&p)
			if err != nil {
				fmt.Printf("%s\n", err)
				return
			}

			// json にエンコード
			var mapData map[string]interface{}
			b, err := json.Marshal(history)
			json.Unmarshal([]byte(b), &mapData)

			// その日のメッセージ履歴の有無　無ければファイルは作成しない
			isNone, _ := json.Marshal(mapData["messages"])
			if string(isNone) == "[]" {
				continue
			}
			if err := os.MkdirAll(k, 0777); err != nil {
				fmt.Println(err)
			}
			// ファイル書き込み
			fileDay, _ := time.Parse("2006-01", typeChange.TimeToString(date))
			fileName := k + "/" + typeChange.TimeToString(fileDay)[0:7] + ".json"
			file, err := os.Create(fileName)
			file.Write(b)
			file.Close()
		}
	}
}
