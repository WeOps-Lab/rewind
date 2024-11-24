package server

import (
	"context"
	"os"
	"os/signal"
	"syscall"
	"user-manager/hooks"

	"github.com/WeOps-Lab/rewind/lib/web/server"
	"github.com/gofiber/fiber/v2/log"
	"github.com/urfave/cli/v2"
)

func Command() *cli.Command {
	return &cli.Command{
		Name:  "server",
		Usage: "start the server",
		Subcommands: []*cli.Command{
			{
				Name:  "start",
				Usage: "start the server",
				Action: func(c *cli.Context) error {
					ctx, cancel := context.WithCancel(context.Background())

					go func() {
						server.RewindAppHooks = hooks.ExampleAppHooks{}
						if err := server.Startup(ctx); err != nil {
							log.Fatalf("Error starting the server: %v\n", err)
						}
					}()

					stop := make(chan os.Signal, 1)
					signal.Notify(stop, syscall.SIGINT, syscall.SIGTERM)
					<-stop

					server.Shutdown(ctx)

					cancel()

					return nil
				},
			},
		},
	}
}
