package cmd

import (
	"github.com/gofiber/fiber/v2/log"
	"github.com/urfave/cli/v2"
	"munchkin/cmd/db"
	"munchkin/cmd/server"
	_ "munchkin/models"
	"os"
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
