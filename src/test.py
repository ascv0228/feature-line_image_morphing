import tkinter as tk

# 初始化主窗口
window = tk.Tk()
window.title("选项排序")

# 已知选项
options = ["选项A", "选项B", "选项C", "选项D"]

# 用于保存按下按钮的顺序
selected_order = []

def on_button_click(option):
    # 记录用户按下按钮的顺序
    if option not in selected_order:
        selected_order.append(option)
        print(f"当前选择顺序: {selected_order}")

# 创建按钮
for i, option in enumerate(options):
    button = tk.Button(window, text=option, command=lambda o=option: on_button_click(o))
    button.grid(row=i, column=0, padx=10, pady=10)

# 提交按钮
def submit():
    print(f"最终顺序: {selected_order}")

submit_button = tk.Button(window, text="提交", command=submit)
submit_button.grid(row=len(options), column=0, pady=10)

# 运行主循环
window.mainloop()
