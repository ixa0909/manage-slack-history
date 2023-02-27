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

func main() {
	// トークンやチャンネル ID をロード
	godotenv.Load("./.env")
	TOKEN := os.Getenv("SLACK_USER_TOKEN")
	// api 宣言
	api := slack.New(TOKEN)

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
		p := slack.GetConversationRepliesParameters{
			ChannelID:          "",
			Timestamp:          "1668490459.884899",
			Cursor:             "",
			Inclusive:          true,
			Latest:             latest,
			Limit:              limit,
			Oldest:             oldest,
			IncludeAllMetadata: true,
		}

		// 履歴を取得
		history,_,_, err := api.GetConversationReplies(&p)
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
		fmt.Println(string(b))
	}

}
