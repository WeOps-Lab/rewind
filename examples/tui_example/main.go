package main

import (
	"github.com/WeOps-Lab/rewind/examples/tui_example/pages/example"
	"github.com/WeOps-Lab/rewind/lib/tui/frame"
	"github.com/WeOps-Lab/rewind/lib/tui/layout"
	"github.com/WeOps-Lab/rewind/lib/tui/model"
)

func main() {
	app := layout.NewApp()

	var sampleMenu = []frame.MenuItem{
		{
			Name: "查看日志",
			Action: func(bs *model.AppModel) {
				example.SetUpLogViewerPage(bs)
			},
		},
		{
			Name: "Shell命令",
			Action: func(bs *model.AppModel) {
				example.SetUpShellCommandPage(bs)
			},
		},
		{
			Name: "查看文件",
			Action: func(bs *model.AppModel) {
				example.SetupEditFilePage(bs)
			},
		},
		{
			Name: "表单示例",
			Action: func(bs *model.AppModel) {
				example.SetUpFormSamplePage(bs)
			},
		},
	}

	var menuItems = []frame.MenuItem{
		{
			Name: "示例",
			Action: func(model *model.AppModel) {

			},
			SubItems: sampleMenu,
		},
		{
			Name: "退出",
			Action: func(bs *model.AppModel) {
				bs.CoreApp.Stop()
			},
		},
	}
	app.Start(menuItems)
}
