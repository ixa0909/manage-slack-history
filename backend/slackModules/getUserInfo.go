package slackModules

import (
	"fmt"
	"os"

	"github.com/joho/godotenv"
	"github.com/slack-go/slack"
)

func GetUserInfo() {
	godotenv.Load("../../.env")
	TOKEN := os.Getenv("SLACK_BOT_TOKEN")
	USER := os.Getenv("SLACK_USER")
	fmt.Print(USER)
	api := slack.New(TOKEN)
	user, err := api.GetUserInfo(USER)
	if err != nil {
		fmt.Printf("%s\n", err)
		return
	}
	fmt.Printf("ID: %s, Fullname: %s, Email: %s\n", user.ID, user.Profile.RealName, user.Profile.Email)
}
