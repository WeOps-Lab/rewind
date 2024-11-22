package enviroments

import "github.com/caitlinelfring/go-env-default"

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
