package main

import (
	"github.com/WeOps-Lab/rewind/lib/pkgs/cfg"
	"user-manager/cmd"
)

func main() {
	cfg.LoadConfig()
	cmd.Run()
}
