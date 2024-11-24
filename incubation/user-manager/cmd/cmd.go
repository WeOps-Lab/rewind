package cmd

import (
	"os"
	"user-manager/cmd/db"
	"user-manager/cmd/server"

	"github.com/gofiber/fiber/v2/log"
	"github.com/urfave/cli/v2"
)

func Run() {
	app := &cli.App{
		Name: "app",
		Commands: []*cli.Command{
			server.Command(),
			db.Command(),
		},
	}

	if err := app.Run(os.Args); err != nil {
		log.Fatal(err)
	}
}
