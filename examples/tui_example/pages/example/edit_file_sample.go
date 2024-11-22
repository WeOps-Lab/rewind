package example

import (
	"github.com/WeOps-Lab/rewind/lib/tui/model"
	"github.com/WeOps-Lab/rewind/lib/tui/utils"
	"github.com/rivo/tview"
	"io/ioutil"
	"path/filepath"
)

func add(target *tview.TreeNode, path string) {
	files, err := ioutil.ReadDir(path)
	if err != nil {
		return
	}

	for _, file := range files {
		node := tview.NewTreeNode(file.Name()).
			SetReference(filepath.Join(path, file.Name())).
			SetSelectable(true)
		if file.IsDir() {
			node.SetColor(tview.Styles.SecondaryTextColor)
			target.AddChild(node)
			add(node, filepath.Join(path, file.Name()))
		} else {
			node.SetColor(tview.Styles.PrimaryTextColor)
			target.AddChild(node)
		}
	}
}

func SetupEditFilePage(receiver *model.AppModel) {
	rootDir := "/var/log/" // 设置你想要显示的文件系统的根目录

	// 创建一个文本框用于显示和编辑文件内容
	editorTextView := tview.NewTextView().SetDynamicColors(true)
	editorTextView.SetBorder(true).SetTitle("File Editor").SetTitleAlign(tview.AlignCenter)
	editorTextView.SetChangedFunc(func() {
		receiver.CoreApp.Draw()
	})

	// 创建一个树形视图用于显示文件系统
	tree := tview.NewTreeView().
		SetSelectedFunc(func(node *tview.TreeNode) {
			reference := node.GetReference()
			if reference == nil {
				return // 如果节点没有引用（比如目录节点），则返回
			}

			// 获取节点对应的文件路径
			path := reference.(string)

			// 读取文件内容并显示在编辑器中
			content, err := ioutil.ReadFile(path)
			if err != nil {
				editorTextView.SetText(err.Error())
				return
			}
			editorTextView.SetText(string(content))
		})

	root := tview.NewTreeNode(rootDir).
		SetColor(tview.Styles.PrimaryTextColor)
	tree.SetRoot(root).
		SetCurrentNode(root)

	// 递归添加文件系统的目录和文件到树形视图
	add(root, rootDir)

	// 创建一个布局，左侧是树形视图，右侧是编辑器
	flex := tview.NewFlex().SetDirection(tview.FlexColumn).
		AddItem(tree, 0, 1, true).
		AddItem(editorTextView, 0, 3, false)

	// 创建一个页面
	utils.ShowPage(receiver, "edit_file_page", flex)
}
