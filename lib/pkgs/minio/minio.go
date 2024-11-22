package minio

import (
	"github.com/minio/minio-go/v7"
	"github.com/minio/minio-go/v7/pkg/credentials"
	"log"
)

type MinIOInstance struct {
	Client *minio.Client
}

func NewMinIOInstance(
	endpoint string, accessKeyId string,
	secretAccessKey string, useSsl bool,
) *MinIOInstance {
	client, err := minio.New(endpoint, &minio.Options{
		Creds:  credentials.NewStaticV4(accessKeyId, secretAccessKey, ""),
		Secure: useSsl,
	})
	if err != nil {
		log.Printf("☹️  Could Not Establish MinIO Connection: %v", err)
		log.Fatal(err)
	}

	return &MinIOInstance{
		Client: client,
	}
}
