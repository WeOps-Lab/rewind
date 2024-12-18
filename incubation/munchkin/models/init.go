package models

import "github.com/WeOps-Lab/rewind/lib/pkgs/database"

func init() {
	database.RegisterModel(&User{})
	database.RegisterModel(&UserAPISecret{})
	database.RegisterModel(&Channel{})

	database.RegisterModel(&EmbedProvider{})
	database.RegisterModel(&OCRProvider{})
	database.RegisterModel(&RerankProvider{})
	database.RegisterModel(&TokenConsumption{})

	database.RegisterModel(&KnowledgeBase{})
	database.RegisterModel(&KnowledgeDocument{})
	database.RegisterModel(&FileKnowledge{})
	database.RegisterModel(&ManualKnowledge{})
	database.RegisterModel(&WebPageKnowledge{})

	database.RegisterModel(&LLMModel{})
	database.RegisterModel(&LLMSkill{})
	database.RegisterModel(&SkillRule{})

	database.RegisterModel(&RasaModel{})
	database.RegisterModel(&Bot{})
	database.RegisterModel(&BotConversationHistory{})
	database.RegisterModel(&ConversationTag{})
	database.RegisterModel(&ChannelUser{})
}
