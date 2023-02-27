package slackModules

import (
	"encoding/json"
	"os"

	"github.com/joho/godotenv"
	"github.com/slack-go/slack"
)

func GetUsersInfo() {
	godotenv.Load("./.env")
	TOKEN := os.Getenv("SLACK_USER_TOKEN")
	api := slack.New(TOKEN)

	users, _ := api.GetUsers()
	b, _ := json.Marshal(users)
	fileName := "../../frontend/users.json"
	file, _ := os.Create(fileName)
	file.Write(b)
	defer file.Close()
}
