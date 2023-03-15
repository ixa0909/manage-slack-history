module slackModule

go 1.18

replace typeChange => ../typeChange

require (
	github.com/joho/godotenv v1.5.1
	github.com/slack-go/slack v0.12.1
	typeChange v0.0.0-00010101000000-000000000000
)

require github.com/gorilla/websocket v1.4.2 // indirect
