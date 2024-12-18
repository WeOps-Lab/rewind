package models

type Channel struct {
	MaintainerInfo
	ID            uint           `gorm:"primaryKey" json:"id"`
	Name          string         `gorm:"type:varchar(100);not null;unique;column:name" json:"name"`
	ChannelType   string         `gorm:"type:varchar(100);not null;column:channel_type" json:"channel_type"`
	ChannelConfig map[string]any `gorm:"type:json;column:channel_config" json:"channel_config"`
	Enabled       bool           `gorm:"default:false;column:enabled" json:"enabled"`
}
