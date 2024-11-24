package hooks

import (
	"github.com/gofiber/contrib/fiberi18n/v2"
	"github.com/gofiber/fiber/v2"
	"golang.org/x/text/language"
)

func (e ExampleAppHooks) InstallMiddleware(app *fiber.App) {
	app.Use(
		fiberi18n.New(&fiberi18n.Config{
			RootPath:        "localize",
			AcceptLanguages: []language.Tag{language.Chinese, language.English},
			DefaultLanguage: language.English,
		}),
	)
}
