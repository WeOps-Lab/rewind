package redis

import (
	"fmt"
	"github.com/go-redis/redis/v8"
	"github.com/gofiber/fiber/v2/log"
)

type RedisInstance struct {
	Client *redis.Client
}

func NewRedisInstance(host string, port int, password string, db int) *RedisInstance {
	client := redis.NewClient(&redis.Options{
		Addr:     fmt.Sprintf("%s:%d", host, port),
		Password: password,
		DB:       db,
	})

	pong, err := client.Ping(client.Context()).Result()

	if err != nil {
		log.Infof("☹️  Could Not Establish Redis Connection")
		log.Fatal(err)
	}

	log.Infof("😀 Connected To Redis: %s\n", pong)
	return &RedisInstance{
		Client: client,
	}
}
