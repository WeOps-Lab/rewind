package keycloak

import (
	"github.com/caitlinelfring/go-env-default"
	"github.com/gofiber/fiber/v2/log"
	"testing"
)

func TestTokenIntrospect(t *testing.T) {
	client := NewKeyCloakBasicClient(
		env.GetDefault("KEYCLOAK_URL", "http://localhost:8080"),
		env.GetDefault("KEYCLOAK_REALM", "master"),
		env.GetDefault("KEYCLOAK_CLIENT_ID", "admin-cli"),
		env.GetDefault("KEYCLOAK_CLIENT_SECRET", "admin-cli"),
	)
	token, err := client.GetToken(
		env.GetDefault("KEYCLOAK_USERNAME", "admin"),
		env.GetDefault("KEYCLOAK_PASSWORD", "admin"),
	)
	if err != nil {
		t.Fatal(err)
	}

	_, err = client.IntrospectToken(token.AccessToken)
	log.Infof("Access Token: %s", token.AccessToken)
	if err != nil {
		t.Fatal(err)
	}

	claims := client.DecodeToken(token.AccessToken)
	log.Infof("Token Claims: %+v", claims)

}
