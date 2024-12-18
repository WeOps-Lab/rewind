package models

import "time"

type MaintainerInfo struct {
	CreatedBy string `gorm:"type:varchar(100);column:created_by" json:"created_by"`
	UpdatedBy string `gorm:"type:varchar(100);column:updated_by" json:"updated_by"`
}

type TimeInfo struct {
	CreatedAt time.Time `gorm:"column:created_at" json:"created_at"`
	UpdatedAt time.Time `gorm:"column:updated_at" json:"updated_at"`
}
