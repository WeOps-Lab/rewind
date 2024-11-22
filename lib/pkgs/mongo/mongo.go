package mongo

import (
	"github.com/gofiber/fiber/v2/log"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

type MongoInstance struct {
	Client *mongo.Client
	Db     *mongo.Database
}

func NewMongoInstance(url string, database string) *MongoInstance {
	client, err := mongo.NewClient(options.Client().ApplyURI(url))
	if err != nil {
		panic(err)
	}
	err = client.Connect(nil)
	if err != nil {
		panic(err)
	}

	db := client.Database(database)
	if err != nil {
		log.Infof("☹️  Could Not Establish Mongo DB Connection")
		log.Fatal(err)
	}

	log.Infof("😀 Connected To Mongo DB")

	return &MongoInstance{
		Client: client,
		Db:     db,
	}
}
