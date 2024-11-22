package component

import (
	"github.com/WeOps-Lab/rewind/lib/tui/model"
	"time"

	"github.com/gdamore/tcell/v2"
	"github.com/rivo/tview"
)

type Fields []string

type Header []HeaderColumn

type HeaderColumn struct {
	Name  string
	Align int
	Wide  bool
	Color tcell.Color
}

type RefreshFunction func() TableData

type Row struct {
	ID     string
	Fields Fields
}

type Rows []Row

type TableData struct {
	Header Header
	Rows   Rows
}

func NewRow(size int) Row {
	return Row{Fields: make([]string, size)}
}

type Table struct {
	*tview.Table
	Name string
}

func NewTable(name string) *Table {
	return &Table{
		tview.NewTable(),
		name,
	}
}

// Init initializes the component.
func (t *Table) Init() {
	t.SetFixed(1, 0)
	t.SetBorder(true)
	t.SetBorderAttributes(tcell.AttrBold)
	t.SetBorderPadding(0, 0, 1, 1)
	t.SetDoneFunc(func(key tcell.Key) {
		if key == tcell.KeyEnter {
			t.SetSelectable(true, false)
		}
	})
	t.SetBackgroundColor(tcell.ColorDefault)
	t.SetTitle(t.Name)
	t.Select(0, 0)
}

func (t *Table) Update(data *TableData) {
	t.Clear()
	t.buildHeader(data.Header)
	for row, re := range data.Rows {
		t.buildRow(row+1, re, data.Header)
	}
}

func (t *Table) buildHeader(header Header) {
	for c, col := range header {
		cell := tview.NewTableCell(col.Name)
		cell.SetExpansion(1)
		cell.SetAlign(col.Align)
		t.SetCell(0, c, cell).SetBorder(true)
	}
}

func (t *Table) buildRow(r int, row Row, header Header) {
	var col int
	for c, field := range row.Fields {
		if c >= len(header) {
			continue
		}
		cell := tview.NewTableCell(field)
		cell.SetExpansion(1)
		cell.SetAlign(header[c].Align)
		if col == 0 {
			cell.SetReference(row.ID)
		}
		t.SetCell(r, col, cell)
		col++
	}
}

func (table *Table) BuildTable(bs *model.AppModel, viewName string, refreshPeriod time.Duration, refreshFunction *RefreshFunction, selectedFunction *func(row, col int)) {
	bs.CorePages.AddPage(viewName, table, true, false)
	bs.CorePages.SwitchToPage(viewName)
	if selectedFunction != nil {
		table.SetSelectedFunc(*selectedFunction)
	}
	table.Init()
	if refreshFunction != nil {
		ticker := time.NewTicker(time.Second * refreshPeriod)
		go func() {
			for range ticker.C {
				bs.CoreApp.QueueUpdateDraw(func() {
					tableData := (*refreshFunction)()
					table.Update(&tableData)
				})
			}
		}()
	}
}
