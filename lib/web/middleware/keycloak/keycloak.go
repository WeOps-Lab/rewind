package keycloak

import (
	"github.com/WeOps-Lab/rewind/lib/pkgs/keycloak"
	"github.com/gofiber/fiber/v2"
)

func KeycloakMiddleware(kcClient *keycloak.KeycloakBasicClient) fiber.Handler {
	return func(c *fiber.Ctx) error {

		authHeader := c.Get("Authorization")
		if authHeader == "" {
			return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{"error": "Missing or invalid authorization header"})
		}

		// Extract token from Bearer <token>
		token := authHeader[len("Bearer "):]
		if token == "" {
			return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{"error": "Token is empty"})
		}

		introspectResult, err := kcClient.IntrospectToken(token)
		if err != nil || !*introspectResult.Active {
			return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{"error": "Invalid token"})
		}

		userInfo := kcClient.DecodeToken(token)
		c.Locals("account", userInfo.Account)
		c.Locals("displayName", userInfo.DisplayName)
		return c.Next()
	}
}
