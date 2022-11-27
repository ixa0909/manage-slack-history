package main

import (
	"fmt"
	"os"

	"github.com/joho/godotenv"
	"github.com/slack-go/slack"
)

func main() {
	godotenv.Load("./.env")
	TOKEN := os.Getenv("SLACK_BOT_TOKEN")
	DEV_CHANNEL := os.Getenv("DEV_CHANNEL")

	api := slack.New(TOKEN)
	// attachment := slack.Attachment{
	// 	Pretext: "some pretext",
	// 	Text:    "some text",
	// 	// Uncomment the following part to send a field too
	// 	/*
	// 		Fields: []slack.AttachmentField{
	// 			slack.AttachmentField{
	// 				Title: "a",
	// 				Value: "no",
	// 			},
	// 		},
	// 	*/
	// }

	channelID, timestamp, err := api.PostMessage(
		DEV_CHANNEL,
		slack.MsgOptionText("テスト", false),
		// slack.MsgOptionAttachments(attachment),
		// slack.MsgOptionAsUser(false), // Add this if you want that the bot would post message as a user, otherwise it will send response using the default slackbot
	)
	if err != nil {
		fmt.Printf("%s\n", err)
		return
	}
	fmt.Printf("Message successfully sent to channel %s at %s", channelID, timestamp)
}
