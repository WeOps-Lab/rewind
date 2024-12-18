package entity

import "time"

type UserApiSecretItemResponse struct {
	ID        uint      `json:"id"`
	Username  string    `json:"username"`
	ApiSecret string    `json:"api_secret"`
	Team      string    `json:"team"`
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
}

type CreateRequest struct {
	Username  string `json:"username"`
	ApiSecret string `json:"api_secret"`
	Team      string `json:"team"`
}
