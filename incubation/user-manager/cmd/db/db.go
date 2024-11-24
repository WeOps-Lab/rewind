package db

import (
	"github.com/urfave/cli/v2"
)

func Command() *cli.Command {
	return &cli.Command{
		Name:  "db",
		Usage: "datasource operations",
		Subcommands: []*cli.Command{
			{
				Name:  "migrate",
				Usage: "migration",
				Action: func(c *cli.Context) error {
					return nil
				},
			},
		},
	}
}
