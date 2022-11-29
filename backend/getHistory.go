package main

import (
	"encoding/json"
	"fmt"
	"os"

	"github.com/joho/godotenv"
	"github.com/slack-go/slack"
)

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

func main() {

	godotenv.Load("./.env")
	TOKEN := os.Getenv("SLACK_BOT_TOKEN")
	CHANNEL_ID := os.Getenv("RANDOM_CHANNEL_ID")

	p := slack.GetConversationHistoryParameters{ChannelID: CHANNEL_ID, Cursor: "", Inclusive: true, Latest: "", Limit: 1, Oldest: "", IncludeAllMetadata: false}
	// fmt.Print(p.ChannelID)
	api := slack.New(TOKEN)

	history, err := api.GetConversationHistory(&p)
	if err != nil {
		fmt.Printf("%s\n", err)
		return
	}

	// json にエンコードする必要があった
	b, err := json.Marshal(history)
	fmt.Printf("%s\n", b)
}
