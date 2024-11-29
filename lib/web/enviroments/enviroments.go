package enviroments

import (
	"github.com/caitlinelfring/go-env-default"
	"strings"
)

func GetAppHost() string {
	return env.GetDefault("APP_HOST", "localhost")
}

func GetAppPort() string {
	return env.GetDefault("APP_PORT", "8001")
}

func GetAppEnv() string {
	return env.GetDefault("APP_ENV", "development")
}

func IsDev() bool {
	return env.GetDefault("APP_ENV", "development") == "development"
}

func GetAuthProvider() string {
	return env.GetDefault("AUTH_PROVIDER", "keycloak")
}

func GetAPIPrefix() string {
	return env.GetDefault("API_PREFIX", "/reqApi")
}

func GetBasicAuthUserList() map[string]string {
	userList := env.GetDefault("BASIC_AUTH_USER_LIST", "")
	users := make(map[string]string)
	for _, user := range strings.Split(userList, ",") {
		parts := strings.SplitN(user, ":", 2)
		if len(parts) == 2 {
			users[parts[0]] = parts[1]
		}
	}
	return users
}

func GetKeyAuthAPIKey() []byte {
	return []byte(env.GetDefault("KEY_AUTH_API_KEY", ""))
}

func GetMeshAPIKey() []byte {
	return []byte(env.GetDefault("MESH_API_KEY", "mesh"))
}
