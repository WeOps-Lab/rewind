package hooks

import (
	"github.com/gofiber/fiber/v2"
	"user-manager/controllers"
)

func (e ExampleAppHooks) InstallInternalRouter(router fiber.Router) {
	groupController := controllers.GroupController{}
	router.Get("/group/list", groupController.List)
}

func (e ExampleAppHooks) InstallPublicRouter(router fiber.Router) {
}
