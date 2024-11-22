package hooks

import (
	"github.com/gofiber/fiber/v2"
	"rewind_example/controllers"
)

func (e ExampleAppHooks) InstallInternalRouter(router fiber.Router) {
	exampleGroup := router.Group("/example")
	exampleGroup.Get("/list", controllers.List)
	exampleGroup.Get("/:id", controllers.GetEntity)
	exampleGroup.Delete("/:id", controllers.DeleteEntity)
	exampleGroup.Post("/", controllers.CreateEntity)
	exampleGroup.Put("/", controllers.UpdateEntity)
}

func (e ExampleAppHooks) InstallPublicRouter(router fiber.Router) {
	exampleGroup := router.Group("/example")
	exampleGroup.Get("/hello", controllers.HelloWorld)
}
