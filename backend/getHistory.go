package main

import (
	"fmt"
	"os"

	"github.com/joho/godotenv"
	"github.com/slack-go/slack"
)

// type GetConversationHistoryParameters struct {
// 	ChannelID          string
// 	Cursor             string
// 	Inclusive          bool
// 	Latest             string
// 	Limit              int
// 	Oldest             string
// 	IncludeAllMetadata bool
// }

func main() {

	godotenv.Load("./.env")
	TOKEN := os.Getenv("SLACK_BOT_TOKEN")
	CHANNEL_ID := os.Getenv("DEV_CHANNEL_ID")

	p := slack.GetConversationHistoryParameters{ChannelID: CHANNEL_ID, Cursor: "", Inclusive: true, Latest: "", Limit: 5, Oldest: "", IncludeAllMetadata: true}
	// fmt.Print(p.ChannelID)
	api := slack.New(TOKEN)

	history, err := api.GetConversationHistory(&p)
	if err != nil {
		fmt.Printf("%s\n", err)
		return
	}
	fmt.Print(history)
}
