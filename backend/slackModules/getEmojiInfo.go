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

	emojis, _ := api.GetEmoji()
	b, _ := json.Marshal(emojis)
	fileName := "emojis.json"
	file, _ := os.Create(fileName)
	file.Write(b)
	defer file.Close()
}
