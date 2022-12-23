package main

import (
	"time"

	"example.com/slackModules"
)

func main() {
	// 時間間隔を設定 30 日ごと
	ticker := time.NewTicker(time.Hour * 24 * 30)

	// 遅延実行 main() 終了後 ticker 停止 形式的に記述
	defer ticker.Stop()

	// 初回の履歴取得
	slackModules.GetChannelsInfo()
	// チャンネル名とチャンネル ID を取得
	mapChannels := slackModules.ReadChannelsInfo()
	slackModules.GetUsersInfo()
	slackModules.GetEmojiInfo()
	slackModules.GetHistory(mapChannels)

	// 無限ループで一定期間ごとに getHistory() を実行
	for {
		select {
		case <-ticker.C:
			slackModules.GetChannelsInfo()
			// チャンネル名とチャンネル ID を取得
			mapChannels := slackModules.ReadChannelsInfo()
			slackModules.GetUsersInfo()
			slackModules.GetEmojiInfo()
			slackModules.GetHistory(mapChannels)
		}
	}

}
