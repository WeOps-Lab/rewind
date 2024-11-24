package hooks

import (
	_ "user-manager/docs"

	"github.com/gofiber/fiber/v2"
)

type ExampleAppHooks struct {
}

func (e ExampleAppHooks) PreAppSetup(app *fiber.App) {

}

func (e ExampleAppHooks) PostAppSetup(app *fiber.App) {

}
