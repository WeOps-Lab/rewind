package hooks

import (
	kc "github.com/WeOps-Lab/rewind/lib/pkgs/keycloak"
	"github.com/WeOps-Lab/rewind/lib/web/middleware/keycloak"
	"github.com/gofiber/fiber/v2"
	"os"
	"rewind_example/controllers"
)

func (e ExampleAppHooks) ExtendRouter(app *fiber.App) {

	kcClient := kc.NewKeyCloakBasicClient(
		os.Getenv("KEYCLOAK_ENDPOINT"),
		os.Getenv("KEYCLOAK_REALM"),
		os.Getenv("KEYCLOAK_CLIENT_ID"),
		os.Getenv("KEYCLOAK_CLIENT_SECRET"),
	)

	api := app.Group("/api")
	v1 := api.Group("/v1")

	example := v1.Group("/example")
	example.Get("/hello", keycloak.KeycloakMiddleware(kcClient),
		controllers.HelloWorld)

	example.Get("/list", controllers.List)
	example.Get("/:id", controllers.GetEntity)
	example.Delete("/:id", controllers.DeleteEntity)
	example.Post("/", controllers.CreateEntity)
	example.Put("/", controllers.UpdateEntity)

}
