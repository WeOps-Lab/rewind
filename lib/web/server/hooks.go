package server

import "github.com/gofiber/fiber/v2"

type AppHooks interface {
	PreAppSetup(app *fiber.App)

	InstallDataSource()
	InstallMiddleware(app *fiber.App)
	InstallPublicRouter(router fiber.Router)
	InstallInternalRouter(router fiber.Router)

	PostAppSetup(app *fiber.App)
}

var RewindAppHooks AppHooks
