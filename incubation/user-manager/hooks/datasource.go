package hooks

import (
	"github.com/WeOps-Lab/rewind/lib/pkgs/keycloak"
	"user-manager/global"
)

func (e ExampleAppHooks) InstallDataSource() {
	global.KeycloakAdminClient = keycloak.NewKeyCloakAdminClientFromEnv()
}
