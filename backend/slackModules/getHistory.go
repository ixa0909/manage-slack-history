// 自作パッケージ SlackGo を応用したもの
package slackModules

// パッケージの import
import (
	"encoding/json"
	"fmt"
	"os"
	"strconv"
	"time"

	// 自作パッケージ　日時を UNIX や String 型に変更するため
	"typeChange"

	// env 用
	"github.com/joho/godotenv"
	// Slack-Go
	"github.com/slack-go/slack"
)

// 履歴を取得。引数は Slack のチャンネル名とチャンネル ID を格納した辞書
func GetHistory(mapChannels map[string]string) {

	// トークンとチャンネル ID をロード
	godotenv.Load("./.env")
	TOKEN := os.Getenv("SLACK_USER_TOKEN")

	// Slack API 初期化
	api := slack.New(TOKEN)

	// チャンネルごとに履歴を順次取得
	for CHANNEL_NAME, CHANNEL_ID := range mapChannels {

		// 履歴の取得開始日と取得終了日 time.Parse(フォーマット (2006-01), 時刻)
		// 2 ヶ月ごとに取得想定 fromDate: 取得開始月 toDate: 取得終了日
		fromDate, _ := time.Parse("2006-01", typeChange.TimeToString(time.Now().AddDate(0, -2, 0)))
		toDate := fromDate.AddDate(0, 2, 0)

		// date: 取得日 fromDate ~ toDate を Unix で範囲を定める 一ヶ月ごとに取得
		for date := fromDate; date.Unix() < toDate.Unix(); date = date.AddDate(0, 1, 0) {

			// サーバーに集中アクセスして負荷をかけないように 2 秒間隔
			time.Sleep(time.Second * 2)

			// GetConversation のパラメータ値
			// oldest ~ latest の期間の履歴を取得
			oldest := strconv.FormatInt(typeChange.StrToUnix(date), 10)
			latest := strconv.FormatInt(typeChange.StrToUnix(date.AddDate(0, 1, 0)), 10)

			// 取得する最大投稿数
			limit := 1000

			// Slack-go の投稿履歴取得 API のパラメータ値
			p := slack.GetConversationHistoryParameters{
				ChannelID:          CHANNEL_ID,
				Cursor:             "",
				Inclusive:          true,
				Latest:             latest,
				Limit:              limit,
				Oldest:             oldest,
				IncludeAllMetadata: true,
			}

			// history: 履歴 (binary 型)
			history, err := api.GetConversationHistory(&p)
			if err != nil {
				fmt.Printf("%s\n", err)
				return
			}

			// binary 型 → json に変換
			var mapData map[string]interface{}
			b, err := json.Marshal(history)
			json.Unmarshal([]byte(b), &mapData)

			// その月のメッセージ履歴が無ければファイルは作成しない
			isNone, _ := json.Marshal(mapData["messages"])
			if string(isNone) == "[]" {
				continue
			}

			// チャンネルごとにディレクトリを作成
			if err := os.MkdirAll("../../data/"+CHANNEL_NAME, 0777); err != nil {
				fmt.Println(err)
			}

			// 一ヶ月ごとに投稿履歴ファイルを作成して書き込み
			fileMonth, _ := time.Parse("2006-01", typeChange.TimeToString(date))
			fileName := "../../data/"+CHANNEL_NAME + "/" + typeChange.TimeToString(fileMonth)[0:7] + ".json"
			file, err := os.Create(fileName)
			file.Write(b)
			file.Close()
		}
	}
}
