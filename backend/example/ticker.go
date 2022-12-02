package main
// 1 秒ごとに処理を実行
import (
	"fmt"
	"log"
	"time"
)

func main() {
	log.SetFlags(log.Lmicroseconds)
	ticker := time.NewTicker(time.Millisecond * 1000)
	defer ticker.Stop()
	count := 0
	for {
		select {
		case <-ticker.C:
			log.Printf("count=%d\n", count)
			count++
			doPeriodically()
		}
	}
}

func doPeriodically() {
	/* do something */
	fmt.Print("Hello!")
}
