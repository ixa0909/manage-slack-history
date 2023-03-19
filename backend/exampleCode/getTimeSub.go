package main

import (
	"fmt"
	"time"
)

func main() {
	day1 := time.Now()
	day2 := AddMonth(day1, 2)
	duration := day2.Sub(day1)
	fmt.Println(duration.Hours()) // => "60h30m0s"
}

func AddMonth(t time.Time, d_month int) time.Time {
	year := t.Year()
	month := t.Month()
	day := t.Day()
	newMonth := int(month) + d_month
	newLastDay := getLastDay(year, newMonth)
	var newDay int
	if day > newLastDay {
		newDay = newLastDay
	} else {
		newDay = day
	}

	return time.Date(year, time.Month(newMonth), newDay, t.Hour(), t.Minute(), t.Second(), t.Nanosecond(), t.Location())

}

// その月の最終日を求める
func getLastDay(year, month int) int {
	t := time.Date(year, time.Month(month+1), 1, 0, 0, 0, 0, time.Local)
	t = t.AddDate(0, 0, -1)
	return t.Day()
}
