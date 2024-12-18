package models

type User struct {
	ID          uint             `gorm:"primaryKey" json:"id"`
	Username    string           `gorm:"type:varchar(150);not null;unique;column:username" json:"username"`
	FirstName   string           `gorm:"type:varchar(100);not null;column:first_name" json:"first_name"`
	LastName    string           `gorm:"type:varchar(100);not null;column:last_name" json:"last_name"`
	IsSuperuser bool             `gorm:"default:false;column:is_superuser" json:"is_superuser"`
	Email       string           `gorm:"type:varchar(100);not null;column:email" json:"email"`
	GroupList   []map[string]any `gorm:"type:json;column:group_list" json:"group_list"`
	Roles       []string         `gorm:"type:json;column:roles" json:"roles"`
	Locale      string           `gorm:"type:varchar(20);column:locale" json:"locale"`
}

type UserAPISecret struct {
	TimeInfo
	ID        uint   `gorm:"primaryKey" json:"id"`
	Username  string `gorm:"type:varchar(150);not null;column:username;index" json:"username"`
	ApiSecret string `gorm:"type:varchar(64);not null;column:api_secret" json:"api_secret"`
	Team      string `gorm:"type:varchar(100);not null;column:team" json:"team"`
}
