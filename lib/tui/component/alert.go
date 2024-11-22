package component

import (
	"github.com/navidys/tvxwidgets"
	"github.com/rivo/tview"
)

type Alert struct {
	dialog *tvxwidgets.MessageDialog
}

func NewAlert() *Alert {
	dialog := tvxwidgets.NewMessageDialog(tvxwidgets.InfoDialog)
	return &Alert{dialog: dialog}
}
func (receiver Alert) ShowAlert(page *tview.Pages, content string) {
	receiver.dialog.SetTitle("提示")
	receiver.dialog.SetMessage(content)
	receiver.dialog.SetDoneFunc(func() {
		page.RemovePage("alert_component")
	})

	page.AddAndSwitchToPage("alert_component", receiver.dialog, true)
}
