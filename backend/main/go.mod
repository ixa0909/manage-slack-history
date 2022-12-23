module example.com/main

go 1.18

replace example.com/slackModules => ../slackModules

replace example.com/typeChange => ../typeChange

require example.com/slackModules v0.0.0-00010101000000-000000000000

require (
	example.com/typeChange v0.0.0-00010101000000-000000000000 // indirect
	github.com/gorilla/websocket v1.4.2 // indirect
	github.com/joho/godotenv v1.4.0 // indirect
	github.com/slack-go/slack v0.12.1 // indirect
)
