#!/usr/bin/env python3
"""
Mermaid 流程图生成工具 - GUI 界面
"""

import os
import sys
import tempfile
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import subprocess
from mermaid_generator import MermaidGenerator

# 抑制 macOS Tkinter 弃用警告
os.environ['TK_SILENCE_DEPRECATION'] = '1'

class MermaidGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mermaid 流程图生成工具")
        self.root.geometry("1000x800")
        
        # 确保在 macOS 上正确显示
        if sys.platform == 'darwin':
            # 尝试设置 macOS 特定的选项
            try:
                self.root.tk.call('::tk::unsupported::MacWindowStyle', 'style', self.root._w, 'document', 'closeBox')
            except tk.TclError:
                pass  # 忽略错误，继续执行
        
        self.generator = MermaidGenerator()
        self.current_image_path = None
        
        self._create_widgets()
        
    def _create_widgets(self):
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建左侧编辑区域
        edit_frame = ttk.LabelFrame(main_frame, text="Mermaid 语法", padding="5")
        edit_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 创建文本编辑器
        self.text_editor = tk.Text(edit_frame, wrap=tk.WORD, font=("Courier", 12))
        self.text_editor.pack(fill=tk.BOTH, expand=True)
        
        # 添加示例按钮
        example_button = ttk.Button(edit_frame, text="插入示例", command=self._insert_example)
        example_button.pack(pady=5)
        
        # 创建按钮区域
        button_frame = ttk.Frame(edit_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        # 生成按钮
        generate_button = ttk.Button(button_frame, text="生成流程图", command=self._generate_diagram)
        generate_button.pack(side=tk.LEFT, padx=5)
        
        # 保存按钮
        save_button = ttk.Button(button_frame, text="保存流程图", command=self._save_diagram)
        save_button.pack(side=tk.LEFT, padx=5)
        
        # 清除按钮
        clear_button = ttk.Button(button_frame, text="清除", command=self._clear_text)
        clear_button.pack(side=tk.LEFT, padx=5)
        
        # 创建右侧预览区域
        preview_frame = ttk.LabelFrame(main_frame, text="预览", padding="5")
        preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 创建预览画布
        self.preview_canvas = tk.Canvas(preview_frame, bg="white")
        self.preview_canvas.pack(fill=tk.BOTH, expand=True)
        
        # 状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def _insert_example(self):
        """插入示例 Mermaid 语法"""
        example = """graph LR
    participant User as "用户"
    participant App as "您的 Web 应用"
    participant OpenAM as "OpenAM (OIDC 提供者)"

    User->>App: 1. 访问受保护资源
    App->>User: 2. 重定向到 OpenAM 登录页面
    User->>OpenAM: 3. 访问登录页面
    OpenAM->>User: 4. 显示登录表单
    User->>OpenAM: 5. 提交登录凭据
    OpenAM->>OpenAM: 6. 验证凭据
    OpenAM->>User: 7. 发放授权码（重定向）
    User->>App: 8. 重定向到 App 的回调 URL（带授权码）
    App->>OpenAM: 9. 用授权码换取 ID 令牌
    OpenAM->>App: 10. 返回 ID 令牌
    App->>App: 11. 验证 ID 令牌，建立会话
    App->>User: 12. 访问受保护资源"""
        
        self.text_editor.delete(1.0, tk.END)
        self.text_editor.insert(tk.END, example)
    
    def _generate_diagram(self):
        """生成流程图"""
        mermaid_text = self.text_editor.get(1.0, tk.END)
        
        if not mermaid_text.strip():
            messagebox.showwarning("警告", "请输入 Mermaid 语法")
            return
        
        self.status_var.set("正在生成流程图...")
        self.root.update()
        
        # 生成流程图
        output_path = self.generator.generate_from_text(mermaid_text)
        
        if output_path:
            self.current_image_path = output_path
            self._display_image(output_path)
            self.status_var.set(f"流程图已生成: {output_path}")
        else:
            self.status_var.set("生成流程图失败")
    
    def _display_image(self, image_path):
        """在预览区域显示图像"""
        # 清除画布
        self.preview_canvas.delete("all")
        
        # 加载图像
        image = Image.open(image_path)
        
        # 调整图像大小以适应画布
        canvas_width = self.preview_canvas.winfo_width()
        canvas_height = self.preview_canvas.winfo_height()
        
        # 确保画布已经渲染
        if canvas_width <= 1:
            self.root.update()
            canvas_width = self.preview_canvas.winfo_width()
            canvas_height = self.preview_canvas.winfo_height()
        
        # 计算缩放比例
        img_width, img_height = image.size
        scale = min(canvas_width / img_width, canvas_height / img_height)
        
        if scale < 1:
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            image = image.resize((new_width, new_height), Image.LANCZOS)
        
        # 转换为 Tkinter 可用的格式
        self.tk_image = ImageTk.PhotoImage(image)
        
        # 在画布上显示图像
        self.preview_canvas.create_image(
            canvas_width // 2, canvas_height // 2,
            image=self.tk_image, anchor=tk.CENTER
        )
    
    def _save_diagram(self):
        """保存流程图"""
        if not self.current_image_path or not os.path.exists(self.current_image_path):
            messagebox.showwarning("警告", "请先生成流程图")
            return
        
        # 获取文件扩展名
        ext = os.path.splitext(self.current_image_path)[1]
        
        # 打开文件保存对话框
        file_path = filedialog.asksaveasfilename(
            defaultextension=ext,
            filetypes=[
                ("PNG 图像", "*.png"),
                ("SVG 图像", "*.svg"),
                ("PDF 文档", "*.pdf"),
                ("所有文件", "*.*")
            ]
        )
        
        if file_path:
            # 复制临时文件到选定位置
            import shutil
            shutil.copy2(self.current_image_path, file_path)
            self.status_var.set(f"流程图已保存: {file_path}")
    
    def _clear_text(self):
        """清除文本编辑器内容"""
        self.text_editor.delete(1.0, tk.END)
        self.status_var.set("就绪")

def main():
    try:
        # 检查依赖
        subprocess.run(["mmdc", "--version"], 
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE)
    except FileNotFoundError:
        messagebox.showerror("错误", 
                            "未找到 mermaid-cli (mmdc)。\n\n"
                            "请按照以下步骤安装:\n"
                            "1. 确保已安装 Node.js\n"
                            "2. 运行: npm install -g @mermaid-js/mermaid-cli")
        sys.exit(1)
    
    root = tk.Tk()
    app = MermaidGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 