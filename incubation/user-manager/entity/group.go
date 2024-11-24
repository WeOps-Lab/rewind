package entity

import "github.com/WeOps-Lab/rewind/lib/web/response"

type GroupItemResponse struct {
	Name string `json:"name"`
}

type GroupListResponse struct {
	response.PageEntity
	Items []GroupItemResponse `json:"items"`
}
