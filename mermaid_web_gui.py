#!/usr/bin/env python3
"""
Mermaid 流程图生成工具 - Web 界面
基于 Flask 的替代 GUI，适用于 Tkinter 有问题的环境
"""

import os
import sys
import tempfile
import subprocess
import webbrowser
from flask import Flask, render_template_string, request, send_file, redirect, url_for
from mermaid_generator import MermaidGenerator

app = Flask(__name__)
generator = MermaidGenerator()
current_image_path = None

# HTML 模板
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Mermaid 流程图生成工具</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            height: 100vh;
        }
        .container {
            display: flex;
            flex: 1;
            gap: 20px;
        }
        .editor-section {
            flex: 1;
            display: flex;
            flex-direction: column;
        }
        .preview-section {
            flex: 1;
            border: 1px solid #ccc;
            padding: 10px;
            background-color: white;
            display: flex;
            flex-direction: column;
        }
        textarea {
            flex: 1;
            padding: 10px;
            font-family: monospace;
            font-size: 14px;
            resize: none;
        }
        .button-group {
            margin-top: 10px;
            display: flex;
            gap: 10px;
        }
        button {
            padding: 8px 15px;
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
        .preview-image {
            max-width: 100%;
            max-height: 100%;
            margin: auto;
        }
        .status-bar {
            margin-top: 10px;
            padding: 5px;
            background-color: #f1f1f1;
            border: 1px solid #ddd;
        }
        h2 {
            margin-top: 0;
        }
    </style>
</head>
<body>
    <h1>Mermaid 流程图生成工具</h1>
    <div class="container">
        <div class="editor-section">
            <h2>Mermaid 语法</h2>
            <form action="/generate" method="post">
                <textarea name="mermaid_text" rows="20">{{ mermaid_text }}</textarea>
                <div class="button-group">
                    <button type="submit">生成流程图</button>
                    <button type="button" onclick="location.href='/example'">插入示例</button>
                    <button type="button" onclick="document.querySelector('textarea').value = ''">清除</button>
                    {% if image_path %}
                    <button type="button" onclick="location.href='/download'">保存流程图</button>
                    {% endif %}
                </div>
            </form>
        </div>
        <div class="preview-section">
            <h2>预览</h2>
            <div style="flex: 1; display: flex; justify-content: center; align-items: center;">
                {% if image_path %}
                <img src="/image?t={{ timestamp }}" class="preview-image" alt="生成的流程图">
                {% else %}
                <p>生成流程图后将在此处显示</p>
                {% endif %}
            </div>
        </div>
    </div>
    <div class="status-bar">
        {{ status_message }}
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(
        HTML_TEMPLATE, 
        mermaid_text='', 
        image_path=None,
        status_message='就绪',
        timestamp=0
    )

@app.route('/example')
def example():
    example_type = request.args.get('type', 'sequence')
    
    if example_type == 'sequence':
        example_text = """sequenceDiagram
    participant User as 用户
    participant App as 您的 Web 应用
    participant OpenAM as OpenAM (OIDC 提供者)

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
    else:
        example_text = """graph LR
    A[用户] --> B[Web 应用]
    B --> C[OpenAM]
    C --> B
    B --> A

    subgraph 认证流程
    A -->|1. 访问资源| B
    B -->|2. 重定向| A
    A -->|3. 访问登录页面| C
    C -->|4. 显示登录表单| A
    A -->|5. 提交凭据| C
    C -->|7. 发放授权码| A
    A -->|8. 重定向到回调 URL| B
    B -->|9. 用授权码换取令牌| C
    C -->|10. 返回 ID 令牌| B
    B -->|12. 访问资源| A
    end"""
    
    return render_template_string(
        HTML_TEMPLATE, 
        mermaid_text=example_text, 
        image_path=None,
        status_message='已插入示例',
        timestamp=0
    )

@app.route('/generate', methods=['POST'])
def generate():
    global current_image_path
    
    mermaid_text = request.form.get('mermaid_text', '')
    
    if not mermaid_text.strip():
        return render_template_string(
            HTML_TEMPLATE, 
            mermaid_text='', 
            image_path=None,
            status_message='错误: 请输入 Mermaid 语法',
            timestamp=0
        )
    
    # 生成流程图
    output_path = generator.generate_from_text(mermaid_text)
    
    if output_path:
        current_image_path = output_path
        import time
        return render_template_string(
            HTML_TEMPLATE, 
            mermaid_text=mermaid_text, 
            image_path=output_path,
            status_message=f'流程图已生成: {output_path}',
            timestamp=int(time.time())
        )
    else:
        return render_template_string(
            HTML_TEMPLATE, 
            mermaid_text=mermaid_text, 
            image_path=None,
            status_message='生成流程图失败',
            timestamp=0
        )

@app.route('/image')
def image():
    global current_image_path
    if current_image_path and os.path.exists(current_image_path):
        return send_file(current_image_path)
    return "No image available", 404

@app.route('/download')
def download():
    global current_image_path
    if current_image_path and os.path.exists(current_image_path):
        return send_file(current_image_path, as_attachment=True)
    return redirect(url_for('index'))

def main():
    # 检查依赖
    try:
        import flask
    except ImportError:
        print("错误: 未安装 Flask。请运行: pip install flask")
        sys.exit(1)
        
    try:
        subprocess.run(["mmdc", "--version"], 
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE)
    except FileNotFoundError:
        print("错误: 未找到 mermaid-cli (mmdc)。")
        print("请按照以下步骤安装:")
        print("1. 确保已安装 Node.js")
        print("2. 运行: npm install -g @mermaid-js/mermaid-cli")
        sys.exit(1)
    
    # 打开浏览器
    webbrowser.open('http://127.0.0.1:5000')
    
    # 启动 Flask 应用
    app.run(debug=False)

if __name__ == "__main__":
    main() 