package database

import "github.com/caitlinelfring/go-env-default"

func GetDBTypeFromEnv() string {
	return env.GetDefault("DB_TYPE", "postgres")
}

func GetDBHostFromEnv() string {
	return env.GetDefault("DB_HOST", "localhost")
}

func GetDBPortFromEnv() int {
	return env.GetIntDefault("DB_PORT", 5432)
}

func GetDBUsernameFromEnv() string {
	return env.GetDefault("DB_USERNAME", "postgres")
}

func GetDBPasswordFromEnv() string {
	return env.GetDefault("DB_PASSWORD", "")
}

func GetDBNameFromEnv() string {
	return env.GetDefault("DB_NAME", "postgres")
}
