package kafka

import (
	"fmt"
	"github.com/confluentinc/confluent-kafka-go/kafka"
	"log"
)

type KafkaProducerInstance struct {
	Producer *kafka.Producer
}

func (k *KafkaProducerInstance) Close() {
	if k.Producer != nil {
		k.Producer.Close()
	}
	log.Printf("😀 Kafka Producer Connection Closed")
}

func NewKafkaProducer(servers string) *KafkaProducerInstance {
	p, err := kafka.NewProducer(&kafka.ConfigMap{"bootstrap.servers": servers})
	if err != nil {
		log.Printf("☹️  Could Not Establish Kafka Producer Connection: %v", err)
		log.Fatal(err)
	}

	log.Printf("😀 Connected To Kafka")
	return &KafkaProducerInstance{
		Producer: p,
	}
}

func (k *KafkaProducerInstance) ProduceMessage(topic string, message string) error {
	if k.Producer == nil {
		return fmt.Errorf("Kafka Producer not initialized")
	}

	err := k.Producer.Produce(&kafka.Message{
		TopicPartition: kafka.TopicPartition{Topic: &topic, Partition: kafka.PartitionAny},
		Value:          []byte(message),
	}, nil)
	if err != nil {
		log.Printf("☹️  Error Producing Message: %v", err)
		return err
	}

	return nil
}
