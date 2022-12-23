package slackModules

import (
	"encoding/json"
	"os"

	"github.com/joho/godotenv"
	"github.com/slack-go/slack"
)

func GetEmojiInfo() {
	godotenv.Load("./.env")
	TOKEN := os.Getenv("SLACK_USER_TOKEN")
	api := slack.New(TOKEN)

	emojis, _ := api.GetEmoji()
	b, _ := json.Marshal(emojis)
	fileName := "../../frontend/emojis.json"
	file, _ := os.Create(fileName)
	file.Write(b)
	defer file.Close()
}
