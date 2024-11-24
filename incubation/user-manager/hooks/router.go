package hooks

import (
	"github.com/gofiber/fiber/v2"
)

func (e ExampleAppHooks) InstallInternalRouter(router fiber.Router) {
}

func (e ExampleAppHooks) InstallPublicRouter(router fiber.Router) {
}
