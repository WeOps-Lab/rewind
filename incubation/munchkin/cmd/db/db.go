package db

import (
	"github.com/WeOps-Lab/rewind/lib/pkgs/database"
	"github.com/urfave/cli/v2"
	"munchkin/global"
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
					global.DBClient = database.NewDataBaseInstanceFromEnv(true)
					global.DBClient.Migrate()
					return nil
				},
			},
		},
	}
}
