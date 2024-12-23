import tkinter as tk

class AnimeWindows:
    def __init__(self, options, on_submit):
        # 初始化
        self.window = tk.Tk()
        self.window.title("選擇順序")
        self.options = options
        self.selected_order = []
        self.on_submit = on_submit  # 回調函數

        # 按鈕列表
        for i, option in enumerate(self.options):
            button = tk.Button(self.window, text=option, command=lambda o=option: self.on_button_click(o))
            button.grid(row=i, column=0, padx=10, pady=10)

        # 顯示選中順序的文字區域
        self.text_box = tk.Text(self.window, height=10, width=40)
        self.text_box.grid(row=0, column=1, rowspan=len(self.options), padx=10, pady=10)

        # 提交按鈕
        submit_button = tk.Button(self.window, text="提交", command=self.submit)
        submit_button.grid(row=len(self.options), column=0, pady=10)

        self.window.mainloop()

    def on_button_click(self, option):
        # 記錄使用者按下按鈕的順序
        if option not in self.selected_order:
            self.selected_order.append(option)
            self.update_text_box()
            # print(f"目前選擇順序: {self.selected_order}")

    def update_text_box(self):
        self.text_box.delete(1.0, tk.END)
        self.text_box.insert(tk.END, f"目前選擇順序:\n{self.selected_order}")

    def submit(self):
        # 当提交按鈕按下时，調用回調函數
        print(f"最终順序: {self.selected_order}")
        self.on_submit(self.selected_order)  # 調用回調传递順序
        self.window.destroy()

import argparse
import os
from PIL import Image
from src.animation import images2animation

def main(args):
    png_files = list(filter(lambda f: f.endswith(".png"), os.listdir(args.dir)))

    def handle_submit(selected_order):
        print(f"順序: {selected_order}")

        rgb_images = list(map(lambda f: Image.open(os.path.join(args.dir, f)).convert("RGB"), selected_order))
        
        images2animation( rgb_images, args.dir + "/morphing_animation222.gif")

    # 創建 AnimeWindows 实例并传递回調函數
    w = AnimeWindows(png_files, handle_submit)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Images to Animation")
    parser.add_argument("--dir", type=str, help="dirname of images", default="./res/women_cheetah/mix")
    args = parser.parse_args()

    main(args)