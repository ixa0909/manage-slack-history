package main

import (
	"fmt"
	"os"
)

func useFileRead(fileName string) {
	fp, err := os.Open(fileName)
	if err != nil {
		panic(err)
	}
	defer fp.Close()

	buf := make([]byte, 64)
	for {
		n, err := fp.Read(buf)
		if n == 0 {
			break
		}
		if err != nil {
			panic(err)
		}
		// Print にすると最後に%が表示される　読み込みファイルの最後に改行があれば出ない
		fmt.Println(string(buf))
		
	}
}

func main() {
	useFileRead("example.txt")
}
