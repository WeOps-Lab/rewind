package server

import "github.com/gofiber/fiber/v2"

type AppHooks interface {
	ExtendRouter(app *fiber.App)
	SetupDataSource()
	ExtendMiddleware(app *fiber.App)
}

var RewindAppHooks AppHooks
