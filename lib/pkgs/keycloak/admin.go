package keycloak

import (
	"context"
	"github.com/caitlinelfring/go-env-default"

	"github.com/Nerzal/gocloak/v13"
)

type KeycloakAdminClient struct {
	token  *gocloak.JWT
	client *gocloak.GoCloak
	realm  string
	ctx    context.Context
}

func NewKeyCloakAdminClient(endpoint string, realm string, username string, password string) *KeycloakAdminClient {
	client := gocloak.NewClient(endpoint)
	ctx := context.Background()
	token, err := client.LoginAdmin(ctx, username, password, "master")
	if err != nil {
		panic(err)
	}
	return &KeycloakAdminClient{
		token:  token,
		client: client,
		realm:  realm,
		ctx:    ctx,
	}
}

func NewKeyCloakAdminClientFromEnv() *KeycloakAdminClient {
	return NewKeyCloakAdminClient(
		env.GetDefault("KEYCLOAK_ENDPOINT", ""),
		env.GetDefault("KEYCLOAK_REALM", ""),
		env.GetDefault("KEYCLOAK_ADMIN_USER", ""),
		env.GetDefault("KEYCLOAK_ADMIN_PASSWORD", ""),
	)
}
