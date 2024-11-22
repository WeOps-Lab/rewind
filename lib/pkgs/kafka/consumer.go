package kafka

import (
	"github.com/confluentinc/confluent-kafka-go/kafka"
	"log"
)

type MsgHandlerFunc func(*kafka.Message)
type ErrHandlerFunc func(error)

type KafkaConsumerInstance struct {
	Consumer   *kafka.Consumer
	MsgHandler MsgHandlerFunc
	ErrHandler ErrHandlerFunc
}

func (k *KafkaConsumerInstance) Close() {
	if k.Consumer != nil {
		k.Consumer.Close()
	}
	log.Printf("😀 Kafka Consumer Connection Closed")
}

func NewKafkaConsumer(servers string, groupId string, topics []string, msgHandler MsgHandlerFunc, errHandler ErrHandlerFunc) *KafkaConsumerInstance {
	c, err := kafka.NewConsumer(&kafka.ConfigMap{
		"bootstrap.servers": servers,
		"group.id":          groupId,
		"auto.offset.reset": "latest",
	})
	if err != nil {
		log.Printf("☹️  Could Not Establish Kafka Consumer Connection: %v", err)
		log.Fatal(err)
	}
	err = c.SubscribeTopics(topics, nil)
	if err != nil {
		log.Printf("☹️  Could Not Subscribe to Topics: %v", err)
		log.Fatal(err)
	}
	log.Printf("😀 Connected To Kafka")
	kafkaConsumer := &KafkaConsumerInstance{
		Consumer:   c,
		MsgHandler: msgHandler,
		ErrHandler: errHandler,
	}
	go kafkaConsumer.startConsuming()
	return kafkaConsumer
}

func (k *KafkaConsumerInstance) startConsuming() {
	for {
		msg, err := k.Consumer.ReadMessage(-1)
		if err != nil {
			if k.ErrHandler != nil {
				k.ErrHandler(err)
			} else {
				log.Printf("☹️  Consumer Error: %v", err)
			}
			continue
		}
		if k.MsgHandler != nil {
			k.MsgHandler(msg)
		} else {
			log.Printf("😀 Received Message: %s", msg.Value)
		}
	}
}
