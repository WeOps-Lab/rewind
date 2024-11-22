package database

import (
	"fmt"
	"github.com/acmestack/gorm-plus/gplus"
	"github.com/gofiber/fiber/v2/log"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

var modelRegistry []interface{}

func RegisterModel(model interface{}) {
	modelRegistry = append(modelRegistry, model)
}

func GetRegisteredModels() []interface{} {
	return modelRegistry
}

type DataBase struct {
	Client *gorm.DB
}

func GetPostgresDSNFromEnv() string {
	host := GetDBHostFromEnv()
	port := GetDBPortFromEnv()
	username := GetDBUsernameFromEnv()
	password := GetDBPasswordFromEnv()
	dbName := GetDBNameFromEnv()

	if password == "" {
		return fmt.Sprintf(
			"host=%s port=%d user=%s dbname=%s sslmode=disable",
			host, port, username, dbName)
	}
	return fmt.Sprintf(
		"host=%s port=%d user=%s password=%s dbname=%s sslmode=disable",
		host, port, username, password, dbName)
}

func (c DataBase) Migrate() {
	c.Client.AutoMigrate(GetRegisteredModels()...)
}

func NewDataBaseInstanceFromEnv(enableGPlus bool) *DataBase {
	var dbInstance *DataBase

	dbType := GetDBTypeFromEnv()
	if dbType == "postgres" {
		dsn := GetPostgresDSNFromEnv()
		dbInstance = NewDataBaseInstance(dbType, dsn)
	} else {
		panic("Database Type Not Supported")
	}

	if enableGPlus {
		gplus.Init(dbInstance.Client)
	}
	return dbInstance
}

func NewDataBaseInstance(dbType string, dsn string) *DataBase {
	var db *gorm.DB
	var err error

	if dbType == "postgres" {
		db, err = gorm.Open(postgres.Open(dsn), &gorm.Config{})
	} else {
		panic("Database Type Not Supported")
	}
	if err != nil {
		log.Infof("☹️  Could Not Establish  DB Connection")
		panic(err)
	} else {
		log.Info("😀 Connected To DB")
	}
	return &DataBase{
		Client: db,
	}
}
