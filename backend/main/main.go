package main

import (
	"computeTime"
	"fmt"
	"slackModules"
	"time"
	"typeChange"
)

func main() {

	start := time.Now()
	fmt.Println(start)
	fmt.Println("履歴の取得開始\n")

	// 実行時が 12 月 15 日だとすると, 11 月の履歴を取得
	slackModules.GetChannelsInfo()
	// チャンネル名とチャンネル ID を取得
	mapChannels := slackModules.ReadChannelsInfo()
	// User 情報ファイルを作成
	slackModules.GetUsersInfo()
	// 絵文字情報ファイルを作成
	slackModules.GetEmojiInfo()
	// 履歴ファイル作成
	slackModules.GetHistory(mapChannels)

	end := time.Now()
	fmt.Print("\n\n")
	fmt.Println(time.Parse("2006-01-02 15:04:05", typeChange.TimeToString(end)))
	fmt.Println("\n履歴の取得終了\n")

	programDuration := end.Sub(start)

	// 現在時刻から 1 ヶ月後に履歴を再度 1 ヶ月分取得
	today := time.Now()
	afterTwoMonth := computeTime.AddMonth(today, 1)
	duration := afterTwoMonth.Sub(today)
	ticker := time.NewTicker(time.Duration(duration - programDuration))

	// 無限ループで一定期間ごとに履歴取得 (getHistory()) を実行
	for {
		select {
		case <-ticker.C:

			start = time.Now()
			fmt.Println(start)
			fmt.Println("履歴の取得開始\n")

			// 実行時が 12 月 15 日だとすると, 11 月の履歴を取得
			slackModules.GetChannelsInfo()
			// チャンネル名とチャンネル ID を取得
			mapChannels = slackModules.ReadChannelsInfo()
			// User 情報ファイルを作成
			slackModules.GetUsersInfo()
			// 絵文字情報ファイルを作成
			slackModules.GetEmojiInfo()
			// 履歴ファイル作成
			slackModules.GetHistory(mapChannels)

			end = time.Now()
			fmt.Print("\n\n")
			fmt.Println(end)
			fmt.Println("\n履歴の取得終了\n")

			programDuration = end.Sub(start)

			// 現在時刻から 1 ヶ月後に履歴を再度 1 ヶ月分取得
			today = time.Now()
			afterTwoMonth = computeTime.AddMonth(today, 1)
			duration = afterTwoMonth.Sub(today)
			ticker = time.NewTicker(time.Duration(duration - programDuration))
		}
	}
	// 遅延実行 main() 終了後 ticker 停止 形式的に記述
	defer ticker.Stop()

}
