package main

import (
	"github.com/WeOps-Lab/rewind/lib/pkgs/cfg"
	"rewind_example/cmd"
)

func main() {
	cfg.LoadConfig()
	cmd.Run()
}
