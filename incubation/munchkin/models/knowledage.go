package models

type KnowledgeBase struct {
	ID                 uint     `gorm:"primaryKey" json:"id"`
	Name               string   `gorm:"type:varchar(100);not null;column:name;index" json:"name"`
	Introduction       string   `gorm:"type:text;not null;column:introduction;" json:"introduction"`
	Team               []string `gorm:"type:json;column:team" json:"team"`
	EmbedModel         *uint    `gorm:"column:embed_model" json:"embed_model"`
	EnableVectorSearch bool     `gorm:"default:true;column:enable_vector_search;" json:"enable_vector_search"`
	VectorSearchWeight float32  `gorm:"type:real;default:0.1;column:vector_search_weight" json:"vector_search_weight"`
	EnableTextSearch   bool     `gorm:"default:true;not null;column:enable_text_search" json:"enable_text_search"`
	TextSearchWeight   float32  `gorm:"type:real;default:0.9;column:text_search_weight" json:"text_search_weight"`
	EnableRerank       bool     `gorm:"default:true;column:enable_rerank" json:"enable_rerank"`
	RerankModel        *uint    `gorm:"column:rerank_model" json:"rerank_model"`
	RagK               int      `gorm:"type:int;default:50;column:rag_k" json:"rag_k"`
	RagNumCandidates   int      `gorm:"type:int;default:1000;column:rag_num_candidates" json:"rag_num_candidates"`
	TextSearchMode     string   `gorm:"type:varchar(20);not null;column:text_search_mode" json:"text_search_mode"`
}

type KnowledgeDocument struct {
	MaintainerInfo
	TimeInfo
	ID                                 uint          `gorm:"primaryKey" json:"id"`
	KnowledgeBaseID                    *uint         `gorm:"index;column:knowledge_base_id" json:"knowledge_base_id"`
	Name                               string        `gorm:"type:varchar(255);not null;column:name;index" json:"name"`
	ChunkSize                          int           `gorm:"type:int;column:chunk_size;" json:"chunk_size"`
	TrainStatus                        int8          `gorm:"type:smallint;default:0;column:train_status;" json:"train_status"`
	TrainProgress                      float32       `gorm:"type:real;default:0;column:train_progress;" json:"train_progress"`
	EnableGeneralParse                 bool          `gorm:"default:true;column:enable_general_parse;" json:"enable_general_parse"`
	GeneralParseChunkSize              int           `gorm:"type:int;default=256;column:general_parse_chunk_size;" json:"general_parse_chunk_size"`
	GeneralParseChunkOverlap           int           `gorm:"type:int;default=32;column:general_parse_chunk_overlap;" json:"general_parse_chunk_overlap"`
	EnableSemanticChunkParse           bool          `gorm:"default:false;column:enable_semantic_chunk_parse;" json:"enable_semantic_chunk_parse"`
	SemanticChunkParseEmbeddingModelID *uint         `gorm:"column:semantic_chunk_parse_embedding_model_id" json:"semantic_chunk_parse_embedding_model_id"`
	SemanticChunkParseEmbeddingModel   EmbedProvider `gorm:"foreignKey:SemanticChunkParseEmbeddingModelID" json:"semantic_chunk_parse_embedding_model"`
	EnableOCRParse                     bool          `gorm:"default:false;column:enable_ocr_parse;" json:"enable_ocr_parse"`
	OCRModelID                         *uint         `gorm:"column:ocr_model_id" json:"ocr_model_id"`
	OCRModel                           OCRProvider   `gorm:"foreignKey:OCRModelID" json:"ocr_model"`
	EnableExcelParse                   bool          `gorm:"default:true;column:enable_excel_parse;" json:"enable_excel_parse"`
	ExcelHeaderRowParse                bool          `gorm:"default:false;column:excel_header_row_parse;" json:"excel_header_row_parse"`
	ExcelFullContentParse              bool          `gorm:"default:true;column:excel_full_content_parse;" json:"excel_full_content_parse"`
	KnowledgeSourceType                string        `gorm:"type:varchar(20);default:file;column:knowledge_source_type;" json:"knowledge_source_type"`
}

// FileKnowledge represents the file knowledge model
type FileKnowledge struct {
	ID                  uint   `gorm:"primaryKey" json:"id"`
	File                string `gorm:"type:text;not null;column:file" json:"file"`
	KnowledgeDocumentID *uint  `gorm:"index;column:knowledge_document_id;" json:"knowledge_document_id"` // Foreign key
}

type ManualKnowledge struct {
	ID                  uint   `gorm:"primaryKey" json:"id"`
	Content             string `gorm:"type:text;column:content;" json:"content"`
	KnowledgeDocumentID *uint  `gorm:"index;column:knowledge_document_id;" json:"knowledge_document_id"` // Foreign key
}

// WebPageKnowledge represents web page knowledge content
type WebPageKnowledge struct {
	ID                  uint   `gorm:"primaryKey" json:"id"`
	URL                 string `gorm:"type:text;column:url;" json:"url"`
	MaxDepth            int    `gorm:"column:max_depth;" json:"max_depth"`
	KnowledgeDocumentID *uint  `gorm:"index;column:knowledge_document_id;" json:"knowledge_document_id"` // Foreign key
}
