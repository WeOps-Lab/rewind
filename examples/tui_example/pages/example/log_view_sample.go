package example

import (
	"bufio"
	"context"
	"fmt"
	"github.com/WeOps-Lab/rewind/lib/tui/model"
	"github.com/WeOps-Lab/rewind/lib/tui/utils"
	"github.com/rivo/tview"
	"os"
	"time"
)

func SetUpLogViewerPage(receiver *model.AppModel) {
	// 创建一个表单页面
	formPage := tview.NewForm()
	formPage.SetBorder(true).SetTitle("Log Viewer").SetTitleAlign(tview.AlignCenter)

	// 添加一个表单条目用于输入日志文件路径
	pathLabel := "Log File Path"
	formPage.AddInputField(pathLabel, "", 20, nil, nil)

	// 创建一个文本框用于显示日志输出
	outputTextView := tview.NewTextView().SetDynamicColors(true)
	outputTextView.SetBorder(true).SetTitle("Log Output").SetTitleAlign(tview.AlignCenter)

	// 添加一个按钮，当点击时打开文件并实时显示内容
	formPage.AddButton("Watch Log", func() {
		logPath := formPage.GetFormItemByLabel(pathLabel).(*tview.InputField).GetText()
		ctx, cancel := context.WithCancel(context.Background())
		receiver.CancelFunc = cancel

		go func(ctx context.Context) {
			f, err := os.Open(logPath)
			if err != nil {
				fmt.Fprintf(outputTextView, "Error: %v\n", err)
				return
			}
			defer f.Close()

			reader := bufio.NewReader(f)
			var offset int64 = 0
			for {
				select {
				case <-ctx.Done():
					return
				default:
					f.Seek(offset, 0)
					line, _, err := reader.ReadLine()
					if err != nil {
						time.Sleep(1 * time.Second)
						continue
					}
					offset, _ = f.Seek(0, os.SEEK_CUR)
					fmt.Fprintf(outputTextView, "Log Output: %s\n", string(line))
					outputTextView.ScrollToEnd()
					receiver.CoreApp.Draw()
				}
			}
		}(ctx)
	})

	// 添加一个按钮，当点击时取消观察日志
	formPage.AddButton("Stop Watching", func() {
		if receiver.CancelFunc != nil {
			receiver.CancelFunc()
		}
	})

	// 创建一个布局，左侧是表单，右侧是命令输出
	flex := tview.NewFlex().SetDirection(tview.FlexColumn).
		AddItem(formPage, 0, 1, true).
		AddItem(outputTextView, 0, 3, false)

	// 创建一个页面
	utils.ShowPage(receiver, "log_viewer_page", flex)
}
