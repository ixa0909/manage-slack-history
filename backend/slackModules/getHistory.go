package slackModules

import (
	"encoding/json"
	"fmt"
	"os"
	"strconv"
	"time"

	"example.com/typeChange"
	"github.com/joho/godotenv"
	"github.com/slack-go/slack"
)

func GetHistory() {

	// トークンやチャンネル ID をロード
	godotenv.Load("./.env")
	TOKEN := os.Getenv("SLACK_USER_TOKEN")
	CHANNEL_ID := os.Getenv("RANDOM_CHANNEL_ID")

	// api 宣言
	api := slack.New(TOKEN)

	// 取得開始日と取得終了日 time.Parse(フォーマット,時刻)
	fromDate, _ := time.Parse("2006-01-02", typeChange.TimeToString(time.Now().AddDate(0, 0, -20)))
	toDate := fromDate.AddDate(0, 0, 20)

	// 日付で for 文
	for date := fromDate; date.Unix() <= toDate.Unix(); date = date.AddDate(0, 0, 1) {

		// サーバー負荷対策
		time.Sleep(time.Second * 2)

		// GetConversation のパラメータ値
		latest := strconv.FormatInt(typeChange.StrToUnix(date.AddDate(0, 0, 1)), 10)
		limit := 100
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

		// ファイル書き込み
		fileDay, _ := time.Parse("2006-01-02", typeChange.TimeToString(date))
		fileName := typeChange.TimeToString(fileDay)[0:10] + ".json"
		file, err := os.Create(fileName)
		file.Write(b)
		defer file.Close()
	}
}
