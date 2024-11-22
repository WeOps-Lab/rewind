package example

import (
	"fmt"
	"github.com/WeOps-Lab/rewind/lib/tui/model"
	"github.com/WeOps-Lab/rewind/lib/tui/utils"
	"github.com/rivo/tview"
	"os/exec"
	"strings"
)

func SetUpShellCommandPage(receiver *model.AppModel) {
	// 创建一个表单页面
	formPage := tview.NewForm()
	formPage.SetBorder(true).SetTitle("Shell Command Executor").SetTitleAlign(tview.AlignCenter)

	// 添加一个表单条目用于输入shell命令
	commandLabel := "Shell Command"
	formPage.AddInputField(commandLabel, "", 15, nil, nil)

	// 创建一个文本框用于显示命令输出
	outputTextView := tview.NewTextView().SetDynamicColors(true)
	outputTextView.SetBorder(true).SetTitle("Command Output").SetTitleAlign(tview.AlignCenter)

	// 添加一个按钮，当点击时执行shell命令并显示输出
	formPage.AddButton("Execute Command", func() {
		// 获取用户输入的命令
		shellCommand := formPage.GetFormItemByLabel(commandLabel).(*tview.InputField).GetText()

		// 执行命令并获取输出
		out, err := exec.Command("sh", "-c", shellCommand).Output()
		if err != nil {
			fmt.Fprintf(outputTextView, "Error: %v\n", err)
		} else {
			// 将命令输出显示在文本框中
			fmt.Fprintf(outputTextView, "Command Output: %s\n", strings.TrimSpace(string(out)))
		}
	})

	// 创建一个布局，左侧是表单，右侧是命令输出
	flex := tview.NewFlex().SetDirection(tview.FlexColumn).
		AddItem(formPage, 0, 1, true).
		AddItem(outputTextView, 0, 3, false)

	// 创建一个页面
	utils.ShowPage(receiver, "shell_command_page", flex)
}
