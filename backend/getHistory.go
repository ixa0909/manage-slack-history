package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strconv"
	"time"

	"github.com/joho/godotenv"
	"github.com/slack-go/slack"
)

func main() {
	ticker := time.NewTicker(time.Millisecond * 1000 * 60)
	defer ticker.Stop()
	for {
		select {
		case <-ticker.C:
			doPeriodically()
		}
	}
	// doPeriodically()
}

// 履歴を取る関数の引数の構造体定義部分
// type GetConversationHistoryParameters struct {
// 	ChannelID          string
// 	Cursor             string
// 	Inclusive          bool
// 	Latest             string
// 	Limit              int
// 	Oldest             string
// 	IncludeAllMetadata bool
// }
// 履歴を取る関数の返り値
// type GetConversationHistoryResponse struct {
// 	SlackResponse
// 	HasMore          bool   `json:"has_more"`
// 	PinCount         int    `json:"pin_count"`
// 	Latest           string `json:"latest"`
// 	ResponseMetaData struct {
// 		NextCursor string `json:"next_cursor"`
// 	} `json:"response_metadata"`
// 	Messages []Message `json:"messages"`
// }
func strToUnix(t time.Time) int64 {
	return t.Unix()
}
func timeToString(t time.Time) string {
	str := t.Format("2006-01-02")
	return str
}
func interfaceToString(t interface{}) string {
	str := t.(string)
	return str
}
func doPeriodically() {

	godotenv.Load("./.env")
	TOKEN := os.Getenv("SLACK_USER_TOKEN")
	CHANNEL_ID := os.Getenv("RANDOM_CHANNEL_ID")

	// fromDate, _ := time.Parse("2006-01-02 (JST)", "2022-10-02 (JST)")
	fromDate, _ := time.Parse("2006-01-02", timeToString(time.Now().AddDate(0, 0, -20)))
	// toDate, _ := time.Parse("2006-01-02 (JST)", "2022-12-20 (JST)")
	toDate := fromDate.AddDate(0, 0, 20)
	fmt.Print(timeToString(time.Now().AddDate(0, 0, -20)))

	for date := fromDate; date.Unix() <= toDate.Unix(); date = date.AddDate(0, 0, 1) {
		time.Sleep(time.Second * 2)
		oldest := strconv.FormatInt(strToUnix(date), 10)

		end := date.AddDate(0, 0, 1)
		latest := strconv.FormatInt(strToUnix(end), 10)

		p := slack.GetConversationHistoryParameters{ChannelID: CHANNEL_ID, Cursor: "", Inclusive: true, Latest: latest, Limit: 1000, Oldest: oldest, IncludeAllMetadata: true}

		api := slack.New(TOKEN)

		history, err := api.GetConversationHistory(&p)
		if err != nil {
			fmt.Printf("%s\n", err)
			return
		}
		// json にエンコードする必要があった
		var mapData map[string]interface{}

		b, err := json.Marshal(history)
		json.Unmarshal([]byte(b), &mapData)

		// ファイル名のため
		s, _ := time.Parse("2006-01-02", timeToString(date))

		isNone, _ := json.Marshal(mapData["messages"])
		if string(isNone) == "[]" {
			continue
		}
		// fmt.Print(string(isNone))

		f, err := os.Create(timeToString(s)[0:10] + ".json")
		f.Write(b)
		defer f.Close()

	}

}
