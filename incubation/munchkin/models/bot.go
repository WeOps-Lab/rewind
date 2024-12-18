package models

import (
	"time"
)

type RasaModel struct {
	MaintainerInfo
	ID          uint   `gorm:"primaryKey;autoIncrement" json:"id"`
	Name        string `gorm:"type:varchar(255);column:name" json:"name"`
	Description string `gorm:"type:text;column:description" json:"description"`
	ModelFile   string `gorm:"type:text;column:model_file" json:"model_file"`
}

type Bot struct {
	MaintainerInfo
	ID              uint       `gorm:"primaryKey;autoIncrement" json:"id"`
	Name            string     `gorm:"type:varchar(255);column:name" json:"name"`
	Introduction    string     `gorm:"type:text;column:introduction" json:"introduction"`
	Team            []string   `gorm:"type:json;column:team" json:"team"`
	Channels        []int      `gorm:"type:json;column:channels" json:"channels"`
	RasaModelID     *uint      `gorm:"column:rasa_model_id" json:"rasa_model_id"`
	RasaModel       RasaModel  `gorm:"foreignKey:RasaModelID" json:"rasa_model"`
	LLMSkills       []LLMSkill `gorm:"many2many:bot_llm_skills;" json:"llm_skills"`
	EnableBotDomain bool       `gorm:"default:false;column:enable_bot_domain" json:"enable_bot_domain"`
	BotDomain       string     `gorm:"type:varchar(255);column:bot_domain" json:"bot_domain"`
	EnableNodePort  bool       `gorm:"default:false;column:enable_node_port" json:"enable_node_port"`
	NodePort        int        `gorm:"default:5005;column:node_port" json:"node_port"`
	Online          bool       `gorm:"default:false;column:online" json:"online"`
	EnableSSL       bool       `gorm:"default:false;column:enable_ssl" json:"enable_ssl"`
	APIToken        string     `gorm:"type:varchar(64);default:'';column:api_token" json:"api_token"`
}

type BotChannel struct {
	ID            uint           `gorm:"primaryKey" json:"id"`
	BotID         uint           `gorm:"type:int;not null;column:bot_id" json:"bot_id"`             // 外键
	Bot           Bot            `gorm:"foreignKey:BotID" json:"bot"`                               // 外键关系定义
	Name          string         `gorm:"type:varchar(100);column:name" json:"name"`                 // 名称字段
	ChannelType   string         `gorm:"type:varchar(100);column:channel_type" json:"channel_type"` // Channel Type
	ChannelConfig map[string]any `gorm:"type:text;column:channel_config" json:"channel_config"`     // Channel Config
	Enabled       bool           `gorm:"default:false;column:enabled" json:"enabled"`               // Enabled
}

type BotConversationHistory struct {
	ID               uint             `gorm:"primaryKey;autoIncrement" json:"id"`
	BotID            *uint            `gorm:"column:bot_id" json:"bot_id"`
	ConversationRole string           `gorm:"type:varchar(255);column:conversation_role" json:"conversation_role"`
	Conversation     string           `gorm:"type:text;column:conversation" json:"conversation"`
	CreatedAt        time.Time        `gorm:"autoCreateTime" json:"created_at"`
	ChannelUserID    *uint            `gorm:"column:channel_user_id" json:"channel_user_id"`
	CitingKnowledge  []map[string]any `gorm:"type:json;column:citing_knowledge" json:"citing_knowledge"`
}

type ConversationTag struct {
	ID                  uint                   `gorm:"primaryKey;autoIncrement" json:"id"`
	Question            string                 `gorm:"type:text;column:question" json:"question"`
	AnswerID            uint                   `gorm:"column:answer_id" json:"answer_id"`
	Answer              BotConversationHistory `gorm:"foreignKey:AnswerID" json:"answer"`
	Content             string                 `gorm:"type:text;column:content" json:"content"`
	KnowledgeBaseID     *uint                  `gorm:"column:knowledge_base_id" json:"knowledge_base_id"`
	KnowledgeDocumentID *uint                  `gorm:"column:knowledge_document_id" json:"knowledge_document_id"`
}

type ChannelUser struct {
	ID          uint   `gorm:"primaryKey;autoIncrement" json:"id"`
	UserID      string `gorm:"type:varchar(100);column:user_id" json:"user_id"`
	Name        string `gorm:"type:varchar(100);column:name" json:"name"`
	ChannelType string `gorm:"type:varchar(100);column:channel_type" json:"channel_type"`
}
