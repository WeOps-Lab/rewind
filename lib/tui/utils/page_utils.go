package utils

import (
	"github.com/WeOps-Lab/rewind/lib/tui/model"
	"github.com/rivo/tview"
)

func ShowPage(receiver *model.AppModel, view_name string, flex *tview.Flex) {
	if receiver.CorePages.HasPage(view_name) {
		receiver.CorePages.RemovePage(view_name)
	}
	receiver.CorePages.AddPage(view_name, flex, true, false)

	receiver.CorePages.SwitchToPage(view_name)
}
