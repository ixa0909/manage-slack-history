module example.com/slackModules

go 1.18

replace example.com/typeChange => ../typeChange

require (
	example.com/typeChange v0.0.0-00010101000000-000000000000
	github.com/joho/godotenv v1.4.0
	github.com/slack-go/slack v0.12.1
)

require github.com/gorilla/websocket v1.4.2 // indirect
