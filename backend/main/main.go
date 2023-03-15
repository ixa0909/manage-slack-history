package main

import (
	"slackModules"
	"time"
)

func main() {

	// 60 日ごとに履歴を取得
	ticker := time.NewTicker(time.Hour * 24 * 60)

	// 遅延実行 main() 終了後 ticker 停止 形式的に記述
	defer ticker.Stop()

	// チャンネル名とチャンネル ID を取得
	slackModules.GetChannelsInfo()
	mapChannels := slackModules.ReadChannelsInfo()

	// User 情報ファイルを作成
	slackModules.GetUsersInfo()
	// 絵文字情報ファイルを作成
	slackModules.GetEmojiInfo()
	// 履歴ファイル作成
	slackModules.GetHistory(mapChannels)

	// 無限ループで一定期間ごとに履歴取得 (getHistory()) を実行
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
