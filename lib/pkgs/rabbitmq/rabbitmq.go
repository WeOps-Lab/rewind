package rabbitmq

import (
	"fmt"
	"github.com/gofiber/fiber/v2/log"
	"github.com/streadway/amqp"
)

type RabbitMQInstance struct {
	Conn *amqp.Connection
	Ch   *amqp.Channel
}

func (receiver RabbitMQInstance) Close() {
	if receiver.Ch != nil {
		err := receiver.Ch.Close()
		if err != nil {
			log.Infof("☹️  Could Not Close RabbitMQ Channel")
			log.Fatal(err)
		}
	}

	if receiver.Conn != nil {
		err := receiver.Conn.Close()
		if err != nil {
			log.Infof("☹️  Could Not Close RabbitMQ Connection")
			log.Fatal(err)
		}
	}

	log.Infof("😀 RabbitMQ Connection Closed")
}

func NewRabbitMQInstance(
	host string, port int,
	username string, password string,
) *RabbitMQInstance {

	amqpURI := fmt.Sprintf("amqp://%s:%s@%s:%d/",
		username,
		password,
		host,
		port,
	)
	RmqConn, err := amqp.Dial(amqpURI)
	if err != nil {
		log.Infof("☹️  Could Not Establish RabbitMQ Connection")
		log.Fatal(err)
	}

	RmqCh, err := RmqConn.Channel()
	if err != nil {
		log.Infof("☹️  Could Not Establish RabbitMQ Channel")
		log.Fatal(err)
	}
	log.Infof("😀 Connected To RabbitMQ")

	return &RabbitMQInstance{
		Conn: RmqConn,
		Ch:   RmqCh,
	}
}
