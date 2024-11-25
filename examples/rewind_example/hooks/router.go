package hooks

import (
	"github.com/gofiber/fiber/v2"
	"rewind_example/controllers"
)

func (e ExampleAppHooks) InstallInternalRouter(router fiber.Router) {
	exampleGroup := router.Group("/example")
	exampleContoller := controllers.ExampleController{}

	exampleGroup.Get("/list", exampleContoller.List)
	exampleGroup.Get("/:id", exampleContoller.GetEntity)
	exampleGroup.Delete("/:id", exampleContoller.DeleteEntity)
	exampleGroup.Post("/", exampleContoller.CreateEntity)
	exampleGroup.Put("/", exampleContoller.UpdateEntity)
}

func (e ExampleAppHooks) InstallPublicRouter(router fiber.Router) {
	exampleGroup := router.Group("/example")
	exampleContoller := controllers.ExampleController{}
	exampleGroup.Get("/hello", exampleContoller.HelloWorld)
}

func (e ExampleAppHooks) InstallMeshRouter(router fiber.Router) {

}
