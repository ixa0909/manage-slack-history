package typeChange

import "time"

// 型変換
// time.Time → Unix
func StrToUnix(t time.Time) int64 {
	return t.Unix()
}
// time.Time → string
func TimeToString(t time.Time) string {
	str := t.Format("2006-01-02")
	return str
}