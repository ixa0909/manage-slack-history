package main

import (
	"encoding/json"
	"os"

	"github.com/joho/godotenv"
	"github.com/slack-go/slack"
)

func main() {
	godotenv.Load("./.env")
	TOKEN := os.Getenv("SLACK_USER_TOKEN")
	api := slack.New(TOKEN)
	limit := 500
	p := slack.GetConversationsParameters{

		Cursor:          "",
		ExcludeArchived: true,
		Limit:           limit,
		Types:           nil,
		TeamID:          "",
	}
	channels, _, _ := api.GetConversations(&p)
	b, _ := json.Marshal(channels)
	fileName := "channels.json"
	file, _ := os.Create(fileName)
	file.Write(b)
	defer file.Close()
}
