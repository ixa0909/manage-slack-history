https://github.com/slack-go/slack/blob/v0.12.1/conversation.go#L502
https://github.com/slack-go/slack/blob/v0.12.1/users.go#L384
https://github.com/slack-go/slack/blob/v0.12.1/emoji.go#L14
GetConversationHistoryParameters
```Go
type GetConversationHistoryParameters struct {
	ChannelID          string
	Cursor             string
	Inclusive          bool
	Latest             string
	Limit              int
	Oldest             string
	IncludeAllMetadata bool
}
```

GetConversationHistoryResponse
```Go
type GetConversationHistoryResponse struct {
	HasMore          bool   `json:"has_more"`
	PinCount         int    `json:"pin_count"`
	Latest           string `json:"latest"`
	ResponseMetaData struct {
		NextCursor string `json:"next_cursor"`
	} `json:"response_metadata"`
	Messages []Message `json:"messages"`
}
```

GetConversationHistory
```Go
func (api *Client) GetConversationHistory(params *GetConversationHistoryParameters) (*GetConversationHistoryResponse, error) {
	return api.GetConversationHistoryContext(context.Background(), params)
}
```

GetConversationHistoryContext 

```Go
func (api *Client) GetConversationHistoryContext(ctx context.Context, params *GetConversationHistoryParameters) (*GetConversationHistoryResponse, error) {
	values := url.Values{"token": {api.token}, "channel": {params.ChannelID}}
	if params.Cursor != "" {
		values.Add("cursor", params.Cursor)
	}
	if params.Inclusive {
		values.Add("inclusive", "1")
	} else {
		values.Add("inclusive", "0")
	}
	if params.Latest != "" {
		values.Add("latest", params.Latest)
	}
	if params.Limit != 0 {
		values.Add("limit", strconv.Itoa(params.Limit))
	}
	if params.Oldest != "" {
		values.Add("oldest", params.Oldest)
	}
	if params.IncludeAllMetadata {
		values.Add("include_all_metadata", "1")
	} else {
		values.Add("include_all_metadata", "0")
	}

	response := GetConversationHistoryResponse{}

	err := api.postMethod(ctx, "conversations.history", values, &response)
	if err != nil {
		return nil, err
	}

	return &response, response.Err()
}
```