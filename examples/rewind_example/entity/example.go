package entity

import (
	"github.com/WeOps-Lab/rewind/lib/web/response"
)

type ExampleCreateRequest struct {
	Name string `json:"name" validate:"required"`
}

type ExampleUpdateRequest struct {
	ID   uint   `json:"id" validate:"required"`
	Name string `json:"name" validate:"required"`
}

type ExampleItemResponse struct {
	ID   uint   `json:"id"`
	Name string `json:"name"`
}

type ExampleListResponse struct {
	response.PageEntity
	Items []ExampleItemResponse `json:"items"`
}
