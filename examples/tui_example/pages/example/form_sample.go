package example

import (
	"context"
	"fmt"
	component2 "github.com/WeOps-Lab/rewind/lib/tui/component"
	"github.com/WeOps-Lab/rewind/lib/tui/model"
	"github.com/WeOps-Lab/rewind/lib/tui/utils"
	"github.com/rivo/tview"
	"os/exec"
	"strings"
	"time"
)

func SetUpFormSamplePage(receiver *model.AppModel) {
	alert := component2.NewAlert()
	progressBar := component2.NewProgressBar(100)
	formPage := tview.NewForm()
	formPage.SetBorder(true).SetTitle("WeOps部署").SetTitleAlign(tview.AlignCenter)

	appoLabel := "APPO服务器"

	formPage.AddDropDown("操作系统", []string{"Linux", "Windows", "MacOS"}, 0, nil)
	formPage.AddCheckbox("单机部署", false, nil)
	formPage.AddCheckbox("监控中心", false, nil)
	formPage.AddCheckbox("告警中心", false, nil)
	formPage.AddCheckbox("APM", false, nil)
	formPage.AddTextArea(appoLabel, "", 20, 0, 0, nil)
	outputTextView := tview.NewTextView().SetDynamicColors(true)
	outputTextView.SetBorder(true).SetTitle("输出").SetTitleAlign(tview.AlignCenter)
	outputTextView.SetText("")

	formPage.AddButton("开始部署", func() {
		ctx, cancel := context.WithCancel(context.Background())
		receiver.CancelFunc = cancel

		outputTextView.SetText("") // Clear output box content
		appoServer := formPage.GetFormItemByLabel(appoLabel).(*tview.TextArea).GetText()

		if appoServer == "" {
			alert.ShowAlert(receiver.CorePages, "APPO服务器地址不能为空")
			return
		}

		// Output server address
		fmt.Fprintf(outputTextView, "APPO服务器地址: %s\n", appoServer)
		fmt.Fprintf(outputTextView, "开始部署......:")

		go func(ctx context.Context) {
			for i := 0; i < 100; i++ {
				select {
				case <-ctx.Done():
					return
				default:
					out, err := exec.Command("sh", "-c", "ps -ef | wc -l").Output()
					if err != nil {
						fmt.Fprintf(outputTextView, "Error: %v\n", err)
					} else {
						fmt.Fprintf(outputTextView, "当前进程数量: %s\n", strings.TrimSpace(string(out)))
					}
					progressBar.UpdateProgressBar(i)
					outputTextView.ScrollToEnd()
					receiver.CoreApp.Draw()
					time.Sleep(time.Second)
				}
			}
		}(ctx)
	})

	outputFlex := tview.NewFlex().SetDirection(tview.FlexRow).
		AddItem(progressBar.GetProgressBarInstance(), 1, 0, false).
		AddItem(outputTextView, 0, 1, false)

	flex := tview.NewFlex().SetDirection(tview.FlexColumn).
		AddItem(formPage, 0, 1, true).
		AddItem(outputFlex, 0, 3, false)

	utils.ShowPage(receiver, "form_sample", flex)
}
