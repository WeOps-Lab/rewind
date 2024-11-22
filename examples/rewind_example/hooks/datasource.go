package hooks

import (
	"github.com/WeOps-Lab/rewind/lib/pkgs/database"
	"rewind_example/global"
)

func (e ExampleAppHooks) SetupDataSource() {
	global.DBClient = database.NewDataBaseInstanceFromEnv(true)
}
