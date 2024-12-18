package hooks

import (
	"github.com/gofiber/fiber/v2"
	"munchkin/controllers"
)

func (e ExampleAppHooks) InstallInternalRouter(router fiber.Router) {
	userApiSecretGroup := router.Group("/user_api_secret")
	userApiSecretController := controllers.UserApiSecretController{}
	userApiSecretGroup.Get("/", userApiSecretController.List)
	userApiSecretGroup.Post("/", userApiSecretController.CreateEntity)
	userApiSecretGroup.Delete("/", userApiSecretController.DeleteEntity)
	userApiSecretGroup.Post("/generate_api_secret/", userApiSecretController.GenerateApiSecret)

}

func (e ExampleAppHooks) InstallPublicRouter(router fiber.Router) {
}

func (e ExampleAppHooks) InstallMeshRouter(router fiber.Router) {

}
