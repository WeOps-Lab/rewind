package cmd

import (
	"github.com/gofiber/fiber/v2/log"
	"github.com/urfave/cli/v2"
	"os"
	"rewind_example/cmd/db"
	"rewind_example/cmd/server"
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
