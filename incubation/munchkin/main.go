package main

import (
	"github.com/WeOps-Lab/rewind/lib/pkgs/cfg"
	"munchkin/cmd"
)

func main() {
	cfg.LoadConfig()
	cmd.Run()
}
