package layout

import (
	"github.com/WeOps-Lab/rewind/lib/tui/frame"
	"github.com/WeOps-Lab/rewind/lib/tui/model"
	"github.com/gdamore/tcell/v2"
	"github.com/rivo/tview"
)

type App struct {
	model *model.AppModel
}

func NewApp() *App {
	coreApp := tview.NewApplication()
	corePage := tview.NewPages()
	coreList := tview.NewList()

	coreApp.SetRoot(corePage, true)

	model := &model.AppModel{
		CoreApp:   coreApp,
		CorePages: corePage,
		CoreList:  coreList,
	}
	return &App{model: model}
}

func (receiver *App) setupPages(menuItems []frame.MenuItem) {
	frame.SetUpMenuPage(receiver.model, menuItems)
}

func (receiver *App) setupInputCapture(mainPageName string) {
	receiver.model.CoreApp.SetInputCapture(func(event *tcell.EventKey) *tcell.EventKey {
		if event.Key() == tcell.KeyEscape {
			if receiver.model.CancelFunc != nil {
				receiver.model.CancelFunc()
			}
			receiver.model.CorePages.SwitchToPage(mainPageName)
			return nil
		}
		return event
	})
}

func (receiver *App) Start(menuItems []frame.MenuItem) {
	receiver.setupPages(menuItems)
	receiver.setupInputCapture("menuls")

	if err := receiver.model.CoreApp.Run(); err != nil {
		panic(err)
	}
}
