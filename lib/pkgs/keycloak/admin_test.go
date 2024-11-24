package keycloak

import (
	"github.com/caitlinelfring/go-env-default"
	"github.com/gofiber/fiber/v2/log"
	"testing"
)

func TestNewKeyCloakAdminClient(t *testing.T) {
	instance := NewKeyCloakAdminClient(
		env.GetDefault("KEYCLOAK_URL", "http://localhost:8080/auth"),
		"lite",
		env.GetDefault("KEYCLOAK_ADMIN_USERNAME", "admin"),
		env.GetDefault("KEYCLOAK_ADMIN_PASSWORD", "admin"),
	)
	log.Infof("Get Admin Token: %+v", instance.Token.AccessToken)

	rs, _ := instance.GetUserList(0, 1)
	log.Infof("Get User List: %+v", rs)
}
