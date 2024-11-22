package utils

import "fmt"

func MakeHealthText(text string) string {
	return fmt.Sprintf("[green][✔] %s", text)
}

func MakeWarnText(text string) string {
	return fmt.Sprintf("[red][✔] %s", text)
}
