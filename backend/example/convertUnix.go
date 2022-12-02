package main

import (
	"fmt"
	"time"
)
func str2unix(t string) int64 {
	// 文字列 -> time.Time型の関数
	str2time := func(t string) time.Time {
		parsedTime, _ := time.Parse("2006-01-02T15:04:05Z07:00", t)
		return parsedTime
	}
	// time.Time型 -> UNIX時間の関数
	time2unix := func(t time.Time) int64 {
		return t.Unix()
	}
	return time2unix(str2time(t))
}

func main() {
	var strTime string = "2022-12-03T01:29:00+09:00"
	fmt.Println(str2unix(strTime))
	// 1648771200
}