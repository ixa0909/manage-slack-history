module main

go 1.18

replace typeChange => ../typeChange

replace slackModules => ../slackModules

require slackModules v0.0.0-00010101000000-000000000000

require (
	github.com/gorilla/websocket v1.4.2 // indirect
	github.com/joho/godotenv v1.5.1 // indirect
	github.com/slack-go/slack v0.12.1 // indirect
	typeChange v0.0.0-00010101000000-000000000000 // indirect
)
