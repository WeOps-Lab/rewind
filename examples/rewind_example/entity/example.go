package entity

import (
	"github.com/WeOps-Lab/rewind/lib/web/response"
)

type ExampleEntity struct {
	Name string `json:"name"`
}

type ExampleWrapperEntity struct {
	ID uint `json:"id"`
	ExampleEntity
}

type ExampleListEntity struct {
	response.PageEntity
	Items []ExampleWrapperEntity `json:"items"`
}
