package server

import (
	"context"
	"fmt"
	kc "github.com/WeOps-Lab/rewind/lib/pkgs/keycloak"
	"github.com/WeOps-Lab/rewind/lib/web/enviroments"
	"github.com/WeOps-Lab/rewind/lib/web/middleware/keycloak"
	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/log"
	"github.com/gofiber/fiber/v2/middleware/compress"
	"github.com/gofiber/fiber/v2/middleware/cors"
	"github.com/gofiber/fiber/v2/middleware/etag"
	"github.com/gofiber/fiber/v2/middleware/expvar"
	"github.com/gofiber/fiber/v2/middleware/filesystem"
	"github.com/gofiber/fiber/v2/middleware/healthcheck"
	"github.com/gofiber/fiber/v2/middleware/helmet"
	"github.com/gofiber/fiber/v2/middleware/logger"
	"github.com/gofiber/fiber/v2/middleware/recover"
	"github.com/gofiber/fiber/v2/middleware/requestid"
	"github.com/gofiber/swagger"
	"net/http"
	"os"
)

var app *fiber.App

func Startup(ctx context.Context) error {
	app = fiber.New()
	RewindAppHooks.PreAppSetup(app)

	RewindAppHooks.InstallDataSource()

	setupMiddleware()

	api := app.Group("/api")
	publicApi := api.Group("/public")
	RewindAppHooks.InstallMiddleware(app)
	RewindAppHooks.InstallPublicRouter(publicApi)

	kcClient := kc.NewKeyCloakBasicClient(
		os.Getenv("KEYCLOAK_ENDPOINT"),
		os.Getenv("KEYCLOAK_REALM"),
		os.Getenv("KEYCLOAK_CLIENT_ID"),
		os.Getenv("KEYCLOAK_CLIENT_SECRET"),
	)
	keycloakInstance := keycloak.KeycloakMiddleware(kcClient)
	internalApi := api.Group("/internal", keycloakInstance)
	RewindAppHooks.InstallInternalRouter(internalApi)

	RewindAppHooks.PostAppSetup(app)

	err := run(ctx)

	return err
}

func run(ctx context.Context) error {
	port := fmt.Sprintf("%s:%s", enviroments.GetAppHost(), enviroments.GetAppPort())

	// 使用协程启动服务器
	done := make(chan error, 1)
	go func() {
		log.Info("Server is starting...")
		if err := app.Listen(port); err != nil {
			done <- err
		}
	}()

	select {
	case <-ctx.Done():
		log.Info("Shutdown signal received")
		return Shutdown(context.Background())
	case err := <-done:
		log.Infof("Server startup failed: %v\n", err)
		return err
	}
}

func setupMiddleware() {

	app.Use(logger.New())
	app.Use(recover.New())
	app.Use(compress.New())
	app.Use(etag.New())
	app.Use(healthcheck.New())
	app.Use(helmet.New())
	app.Use(requestid.New())
	app.Use(cors.New(cors.Config{
		AllowOrigins: "*",
		AllowHeaders: "Origin, Content-Type, Accept",
	}))

	if enviroments.IsDev() {
		app.Use(expvar.New())
		app.Use("/swagger/*", swagger.HandlerDefault)
	}
	app.Use(filesystem.New(filesystem.Config{
		Root:   http.Dir("./static"),
		Browse: false,
	}))
}

func Shutdown(ctx context.Context) error {
	log.Info("Server is shutting down...")
	if err := app.Shutdown(); err != nil {
		log.Infof("Server shutdown failed: %v\n", err)
		return fmt.Errorf("server shutdown failed: %w", err)
	}

	log.Info("Server gracefully stopped")
	return nil
}
