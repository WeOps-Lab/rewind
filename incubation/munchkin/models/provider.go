package models

import (
	"time"
)

type EmbedProvider struct {
	ID             uint           `gorm:"primaryKey;autoIncrement" json:"id"`
	Name           string         `gorm:"type:varchar(255);unique;column:name" json:"name"`
	EmbedModelType string         `gorm:"type:varchar(50);column:embed_model_type" json:"embed_model_type"`
	EmbedConfig    map[string]any `gorm:"type:json;column:embed_config" json:"embed_config"`
	Enabled        bool           `gorm:"default:true;column:enabled" json:"enabled"`
}

type LLMModel struct {
	ID           uint           `gorm:"primaryKey;autoIncrement" json:"id"`
	Name         string         `gorm:"type:varchar(255);unique;column:name" json:"name"`
	LLMModelType string         `gorm:"type:varchar(50);column:llm_model_type" json:"llm_model_type"`
	LLMConfig    map[string]any `gorm:"type:json;column:llm_config" json:"llm_config"`
	Enabled      bool           `gorm:"default:true;column:enabled" json:"enabled"`
}

type LLMSkill struct {
	ID                        uint            `gorm:"primaryKey;autoIncrement" json:"id"`
	Name                      string          `gorm:"type:varchar(255);column:name" json:"name"`
	LLMModelID                *uint           `gorm:"column:llm_model_id" json:"llm_model_id"`
	LLMModel                  LLMModel        `gorm:"foreignKey:LLMModelID" json:"llm_model"`
	SkillPrompt               string          `gorm:"type:text;column:skill_prompt" json:"skill_prompt"`
	EnableConversationHistory bool            `gorm:"default:false;column:enable_conversation_history" json:"enable_conversation_history"`
	ConversationWindowSize    int             `gorm:"default:10;column:conversation_window_size" json:"conversation_window_size"`
	EnableRAG                 bool            `gorm:"default:false;column:enable_rag" json:"enable_rag"`
	EnableRAGKnowledgeSource  bool            `gorm:"default:false;column:enable_rag_knowledge_source" json:"enable_rag_knowledge_source"`
	RAGScoreThresholdMap      map[string]any  `gorm:"type:json;column:rag_score_threshold_map" json:"rag_score_threshold_map"`
	KnowledgeBase             []KnowledgeBase `gorm:"many2many:llm_skill_knowledge_base;" json:"knowledge_base"`
	Introduction              string          `gorm:"type:text;column:introduction;" json:"introduction"`
	Team                      []string        `gorm:"type:json;column:team" json:"team"`
	Temperature               float32         `gorm:"type:real;default:0.7;column:temperature" json:"temperature"`
}

type SkillRule struct {
	MaintainerInfo
	TimeInfo
	ID          uint           `gorm:"primaryKey;autoIncrement" json:"id"`
	SkillID     uint           `gorm:"column:skill_id" json:"skill_id"`
	Skill       LLMSkill       `gorm:"foreignKey:SkillID" json:"skill"`
	Name        string         `gorm:"type:varchar(255);column:name" json:"name"`
	Description string         `gorm:"type:text;column:description" json:"description"`
	Condition   map[string]any `gorm:"type:json;column:condition" json:"condition"`
	Action      int            `gorm:"type:int;default:0;column:action" json:"action"`
	ActionSet   map[string]any `gorm:"type:json;column:action_set" json:"action_set"`
	IsEnabled   bool           `gorm:"default:true;column:is_enabled" json:"is_enabled"`
}

type OCRProvider struct {
	ID        uint           `gorm:"primaryKey;autoIncrement" json:"id"`
	Name      string         `gorm:"type:varchar(255);unique;column:name" json:"name"`
	OCRConfig map[string]any `gorm:"type:json;column:ocr_config" json:"ocr_config"`
	Enabled   bool           `gorm:"default:true;column:enabled" json:"enabled"`
}

type RerankProvider struct {
	ID              uint           `gorm:"primaryKey;autoIncrement" json:"id"`
	Name            string         `gorm:"type:varchar(255);unique;column:name" json:"name"`
	RerankModelType string         `gorm:"type:varchar(50);column:rerank_model_type" json:"rerank_model_type"`
	RerankConfig    map[string]any `gorm:"type:json;column:rerank_config" json:"rerank_config"`
	Enabled         bool           `gorm:"default:true;column:enabled" json:"enabled"`
}

type TokenConsumption struct {
	ID           uint      `gorm:"primaryKey;autoIncrement" json:"id"`
	BotID        int       `gorm:"type:int;default:0;column:bot_id;index" json:"bot_id"`
	CreatedAt    time.Time `gorm:"autoCreateTime;column:created_at" json:"created_at"`
	InputTokens  int64     `gorm:"type:bigint;column:input_tokens" json:"input_tokens"`
	OutputTokens int64     `gorm:"type:bigint;column:output_tokens" json:"output_tokens"`
	Username     string    `gorm:"type:varchar(100);column:username" json:"username"`
	UserID       string    `gorm:"type:varchar(100);column:user_id" json:"user_id"`
}
