package component

import (
	"github.com/rivo/tview"
	"strings"
)

type ProgressBar struct {
	progressBar *tview.TextView
}

func (receiver ProgressBar) GetProgressBarInstance() *tview.TextView {
	return receiver.progressBar
}
func NewProgressBar(max int) *ProgressBar {
	progressBar := tview.NewTextView()
	progressBar.SetText(strings.Repeat(" ", max))
	progressBar.SetDynamicColors(true)

	return &ProgressBar{progressBar: progressBar}
}

func (receiver ProgressBar) UpdateProgressBar(progress int) {
	full := "[green:]" + strings.Repeat("|", progress)
	empty := "[white:]" + strings.Repeat(" ", 100-progress)
	receiver.progressBar.SetText(full + empty)
}
