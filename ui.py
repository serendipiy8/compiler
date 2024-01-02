import tkinter as tk
from tkinter import scrolledtext, filedialog
from graphviz import Digraph
from gramma import parser

class ASTNode:
    def __init__(self, node_type, children=None, value=None):
        self.node_type = node_type
        self.children = children if children is not None else []
        self.value = value

    def __str__(self, indent=0):
        result = "  " * indent + f"{self.node_type}"
        if self.value is not None:
            result += f"\n{'  ' * (indent + 1)}Value: {self.value}"
        for child in self.children:
            result += "\n" + child.__str__(indent + 1)
        return result

class GUIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("C语言语法分析器")
        self.root.geometry("600x400")  # 设置默认窗口大小

        # 创建菜单栏
        menu_bar = tk.Menu(root)
        root.config(menu=menu_bar)

        # 文件菜单
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="退出", command=root.destroy)

        # 创建输入文本框
        self.code_entry = scrolledtext.ScrolledText(root, width=60, height=15, wrap=tk.WORD)
        self.code_entry.pack(pady=10)

        # 创建运行按钮
        self.run_button = tk.Button(root, text="分析代码", command=self.run_syntax_analysis)
        self.run_button.pack(pady=5)

        # 创建结果显示文本框
        self.result_text = scrolledtext.ScrolledText(root, width=60, height=15, wrap=tk.WORD, state=tk.DISABLED)
        self.result_text.pack(pady=10)

        # 创建状态栏
        self.status_bar = tk.Label(root, text="准备就绪", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # 创建图形化界面展示AST按钮
        self.show_ast_button = tk.Button(root, text="展示AST", command=self.show_ast)
        self.show_ast_button.pack(pady=5)

        # 创建保存AST图按钮
        self.save_ast_button = tk.Button(root, text="保存AST图", command=self.save_ast)
        self.save_ast_button.pack(pady=5)

        # 初始化AST图
        self.ast_graph = Digraph('AST')

    def run_syntax_analysis(self):
        input_code = self.code_entry.get("1.0", tk.END)

        result = parser.parse(input_code)

        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)

        if result:
            self.result_text.insert(tk.END, "语法分析成功！\n")
            self.result_text.insert(tk.END, print_ast(result))
        else:
            self.result_text.insert(tk.END, "语法分析失败！\n")

        self.result_text.config(state=tk.DISABLED)
        self.status_bar.config(text="分析完成")

    def show_ast(self):
        input_code = self.code_entry.get("1.0", tk.END)
        result = parser.parse(input_code)

        if result:
            self.ast_graph.clear()
            self.build_ast_graph(result)
            self.ast_graph.view()
            self.status_bar.config(text="AST图已生成")

    def save_ast(self):
        input_code = self.code_entry.get("1.0", tk.END)
        result = parser.parse(input_code)

        if result:
            self.ast_graph.clear()
            self.build_ast_graph(result)
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])

            if file_path:
                self.ast_graph.format = 'png'
                self.ast_graph.render(filename=file_path, cleanup=True, format='png', engine='dot')
                self.status_bar.config(text=f"AST图已保存至 {file_path}")

    def build_ast_graph(self, node, parent=None):
        if node:
            current_node_label = f"{node.node_type}\n{str(node.value)}" if node.value is not None else f"{node.node_type}"

            if parent:
                self.ast_graph.edge(parent, current_node_label)

            for child in node.children:
                self.build_ast_graph(child, current_node_label)

def print_ast(node, indent=0):
    result = ""
    if node:
        result += "  " * indent + f"{node.node_type}"
        if node.value is not None:
            result += f"\n{'  ' * (indent + 1)}Value: {node.value}"
        for child in node.children:
            result += "\n" + print_ast(child, indent + 1)
    return result

root = tk.Tk()
app = GUIApp(root)
root.mainloop()