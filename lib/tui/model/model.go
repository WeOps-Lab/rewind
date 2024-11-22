package model

import (
	"context"
	"github.com/rivo/tview"
)

type AppModel struct {
	CoreApp    *tview.Application
	CorePages  *tview.Pages
	CoreList   *tview.List
	CancelFunc context.CancelFunc
}
