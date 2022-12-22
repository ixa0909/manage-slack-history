package main

import (
	"fmt"
	"time"
)

func main() {
	fromDate, _ := time.Parse("2006-01-02 (JST)", "2022-11-27 (JST)")
	a, _ := time.Parse("2006-01-02 (JST)", "2022-11-30 (JST)")
	fmt.Println(fromDate)
	fmt.Println(a)
	for i := fromDate; i.Unix()+3600*9 < a.Unix()+3600*9; i = i.AddDate(0, 0, 1) {
		s, _ := time.Parse("2006-01-02 (JST)", timeToString(i))
		
		fmt.Println(timeToString(s)[0:10])
	}
}

func timeToString(t time.Time) string {
	str := t.Format("2006-01-02 (JST)")
	return str
}
