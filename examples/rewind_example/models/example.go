package models

import (
	"github.com/WeOps-Lab/rewind/lib/pkgs/database"
	"gorm.io/gorm"
)

type Example struct {
	gorm.Model
	Name string `gorm:"NOT NULL"`
}

func init() {
	database.RegisterModel(&Example{})
}
