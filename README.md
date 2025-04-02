# Mermaid 流程图生成工具 | Mermaid Flow Chart Generator

[中文](#mermaid-流程图生成工具) | [English](#mermaid-flow-chart-generator)

---

# Mermaid 流程图生成工具

一个简单而强大的 Python 工具，用于将 Mermaid 语法转换为流程图图像。支持命令行、图形界面和 Web 界面，满足不同用户的需求。

## 功能特点

- 支持从文本或文件生成 Mermaid 流程图
- 提供三种使用方式：命令行、图形界面和 Web 界面
- 支持 PNG、SVG 和 PDF 输出格式
- 实时预览生成的流程图
- 支持多种 Mermaid 图表类型（流程图、序列图等）

## 安装要求

- Python 3.6+
- Node.js
- mermaid-cli (`npm install -g @mermaid-js/mermaid-cli`)
- Python 依赖：Pillow、Flask（用于 Web 界面）

## 快速安装

使用提供的安装脚本一键安装所有依赖：

```bash
python install.py
```

安装脚本会自动检查并安装所需的依赖，包括：
- 检查 Python 版本
- 检查并指导安装 Node.js
- 安装 mermaid-cli
- 安装 Python 依赖
- 检查 Tkinter 支持（用于图形界面）

## 手动安装

如果您想手动安装，请按照以下步骤操作：

1. 确保已安装 Node.js 和 Python 3.6+
2. 安装 mermaid-cli:
   ```bash
   npm install -g @mermaid-js/mermaid-cli
   ```
3. 安装 Python 依赖:
   ```bash
   pip install -r requirements.txt
   ```
4. 安装 Mermaid 流程图生成工具:
   ```bash
   pip install -e .
   ```

## 使用方法

### 命令行界面

```bash
# 从文本生成流程图
mermaid-gen -t "graph TD; A-->B; B-->C;" -o flowchart.png

# 从文件生成流程图
mermaid-gen -f input.mmd -o flowchart.svg --format svg

# 查看帮助
mermaid-gen -h
```

或者直接运行 Python 脚本：
```bash
python mermaid_generator.py -t "graph TD; A-->B; B-->C;" -o flowchart.png
```

### 图形界面 (Tkinter)

> ⚠️ **警告**: 图形界面模式在 macOS 系统中可能存在兼容性问题，建议 macOS 用户使用 Web 界面模式。

```bash
mermaid-gui
```

或者直接运行 Python 脚本：
```bash
python mermaid_gui.py
```

### Web 界面 (推荐)

```bash
mermaid-web
```

或者直接运行 Python 脚本：
```bash
python mermaid_web_gui.py
```

Web 界面会在您的默认浏览器中打开，提供直观的编辑和预览功能。

## 示例

### 序列图示例

```
sequenceDiagram
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
    App->>User: 12. 访问受保护资源
```

### 流程图示例

```
graph LR
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
    end
```

## 项目结构

- `mermaid_generator.py` - 核心功能模块，提供命令行接口
- `mermaid_gui.py` - 基于 Tkinter 的图形界面
- `mermaid_web_gui.py` - 基于 Flask 的 Web 界面
- `install.py` - 安装脚本
- `setup.py` - Python 包配置
- `requirements.txt` - Python 依赖列表

## 故障排除

### Tkinter 问题

如果遇到 Tkinter 相关错误，可能是因为您的 Python 安装缺少 Tkinter 支持。您可以：

1. 在 macOS 上：
   ```bash
   brew install python-tk@3.12
   ```
   
   **注意**: 即使安装了 Tkinter，macOS 上的图形界面仍可能存在渲染问题。在这种情况下，建议使用 Web 界面。

2. 在 Linux 上：
   ```bash
   # Ubuntu/Debian
   sudo apt-get install python3-tk
   
   # Fedora
   sudo dnf install python3-tkinter
   
   # CentOS/RHEL
   sudo yum install python3-tkinter
   ```

3. 或者使用 Web 界面替代：
   ```bash
   python mermaid_web_gui.py
   ```

### mermaid-cli 问题

如果遇到 mermaid-cli 相关错误，请确保：

1. 已正确安装 Node.js
2. 已全局安装 mermaid-cli：
   ```bash
   npm install -g @mermaid-js/mermaid-cli
   ```
3. `mmdc` 命令在您的系统路径中

## 贡献

欢迎提交问题报告和改进建议！

## 许可证

MIT

---

# Mermaid Flow Chart Generator

A simple yet powerful Python tool for converting Mermaid syntax into flowchart images. Supports command-line, graphical, and web interfaces to meet different user needs.

## Features

- Generate Mermaid flowcharts from text or files
- Three usage modes: command-line, graphical interface, and web interface
- Support for PNG, SVG, and PDF output formats
- Real-time preview of generated flowcharts
- Support for various Mermaid chart types (flowcharts, sequence diagrams, etc.)

## Requirements

- Python 3.6+
- Node.js
- mermaid-cli (`npm install -g @mermaid-js/mermaid-cli`)
- Python dependencies: Pillow, Flask (for web interface)

## Quick Installation

Use the provided installation script to install all dependencies with one command:

```bash
python install.py
```

The installation script will automatically check and install the required dependencies, including:
- Checking Python version
- Checking and guiding Node.js installation
- Installing mermaid-cli
- Installing Python dependencies
- Checking Tkinter support (for graphical interface)

## Manual Installation

If you prefer to install manually, follow these steps:

1. Ensure Node.js and Python 3.6+ are installed
2. Install mermaid-cli:
   ```bash
   npm install -g @mermaid-js/mermaid-cli
   ```
3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Install the Mermaid Flow Chart Generator:
   ```bash
   pip install -e .
   ```

## Usage

### Command-line Interface

```bash
# Generate a flowchart from text
mermaid-gen -t "graph TD; A-->B; B-->C;" -o flowchart.png

# Generate a flowchart from a file
mermaid-gen -f input.mmd -o flowchart.svg --format svg

# View help
mermaid-gen -h
```

Or run the Python script directly:
```bash
python mermaid_generator.py -t "graph TD; A-->B; B-->C;" -o flowchart.png
```

### Graphical Interface (Tkinter)

> ⚠️ **Warning**: The graphical interface mode may have compatibility issues on macOS systems. macOS users are recommended to use the web interface mode.

```bash
mermaid-gui
```

Or run the Python script directly:
```bash
python mermaid_gui.py
```

### Web Interface (Recommended)

```bash
mermaid-web
```

Or run the Python script directly:
```bash
python mermaid_web_gui.py
```

The web interface will open in your default browser, providing intuitive editing and preview capabilities.

## Examples

### Sequence Diagram Example

```
sequenceDiagram
    participant User
    participant App as Web Application
    participant OpenAM as OpenAM (OIDC Provider)

    User->>App: 1. Access protected resource
    App->>User: 2. Redirect to OpenAM login page
    User->>OpenAM: 3. Access login page
    OpenAM->>User: 4. Display login form
    User->>OpenAM: 5. Submit credentials
    OpenAM->>OpenAM: 6. Validate credentials
    OpenAM->>User: 7. Issue authorization code (redirect)
    User->>App: 8. Redirect to App callback URL (with code)
    App->>OpenAM: 9. Exchange code for ID token
    OpenAM->>App: 10. Return ID token
    App->>App: 11. Validate ID token, establish session
    App->>User: 12. Access protected resource
```

### Flowchart Example

```
graph LR
    A[User] --> B[Web App]
    B --> C[OpenAM]
    C --> B
    B --> A

    subgraph Authentication Flow
    A -->|1. Access resource| B
    B -->|2. Redirect| A
    A -->|3. Access login page| C
    C -->|4. Display login form| A
    A -->|5. Submit credentials| C
    C -->|7. Issue auth code| A
    A -->|8. Redirect to callback URL| B
    B -->|9. Exchange code for token| C
    C -->|10. Return ID token| B
    B -->|12. Access resource| A
    end
```

## Project Structure

- `mermaid_generator.py` - Core functionality module, provides command-line interface
- `mermaid_gui.py` - Tkinter-based graphical interface
- `mermaid_web_gui.py` - Flask-based web interface
- `install.py` - Installation script
- `setup.py` - Python package configuration
- `requirements.txt` - Python dependency list

## Troubleshooting

### Tkinter Issues

If you encounter Tkinter-related errors, it may be because your Python installation lacks Tkinter support. You can:

1. On macOS:
   ```bash
   brew install python-tk@3.12
   ```
   
   **Note**: Even with Tkinter installed, the graphical interface may still have rendering issues on macOS. In this case, it's recommended to use the web interface.

2. On Linux:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install python3-tk
   
   # Fedora
   sudo dnf install python3-tkinter
   
   # CentOS/RHEL
   sudo yum install python3-tkinter
   ```

3. Or use the web interface instead:
   ```bash
   python mermaid_web_gui.py
   ```

### mermaid-cli Issues

If you encounter mermaid-cli related errors, ensure:

1. Node.js is correctly installed
2. mermaid-cli is globally installed:
   ```bash
   npm install -g @mermaid-js/mermaid-cli
   ```
3. The `mmdc` command is in your system path

## Contributing

Issue reports and improvement suggestions are welcome!

## License

MIT
