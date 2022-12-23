package slackModules

import (
	"encoding/json"
	"io/ioutil"
)

type TopicPurpose struct {
	Value    string `json:"value"`
	Creator  string `json:"creator"`
	Last_set int    `json:"last_set"`
}

type Entity struct {
	Channels []*ChannelsInfo `json:"channels"`
}

type ChannelsInfo struct {
	Id                    string       `json:"id"`
	Created               int64        `json:"created"`
	Is_open               bool         `json:"is_open"`
	Is_group              bool         `json:"is_group"`
	Is_shared             bool         `json:"is_shared"`
	Is_im                 bool         `json:"is_im"`
	Is_ext_shared         bool         `json:"is_ext_shared"`
	Is_org_shared         bool         `json:"is_org_shared"`
	Is_pending_ext_shared bool         `json:"is_pending_ext_shared"`
	Is_private            bool         `json:"is_private"`
	Is_mpim               bool         `json:"is_mpim"`
	Unlinked              int          `json:"unlinked"`
	Name_normalized       string       `json:"name_normalized"`
	Num_members           int          `json:"num_members"`
	Priority              int          `json:"priority"`
	User                  string       `json:"user"`
	Name                  string       `json:"name"`
	Creator               string       `json:"creator"`
	Is_archived           bool         `json:"is_archived"`
	Members               string       `json:"members"`
	Topic                 TopicPurpose `json:"topic"`
	Purpose               TopicPurpose `json:"purpose"`
	Is_channel            bool         `json:""`
	Is_general            bool         `json:""`
	Is_member             bool         `json:""`
	Locale                string       `json:""`
}

func ReadChannelsInfo() map[string]string {
	file, err := ioutil.ReadFile("channels.json")
	if err != nil {
		// エラー処理
	}

	// [3] 配列型のJSONデータを読み込む
	channels := make([]*ChannelsInfo, 0)
	err = json.Unmarshal(file, &channels)
	if err != nil {
		// エラー処理
	}
	mapData := make(map[string]string)

	for _, channel := range channels {
		mapData[channel.Name_normalized] = (channel.Id)
	}
	return mapData
}
