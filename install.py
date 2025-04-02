#!/usr/bin/env python3
"""
Mermaid 流程图生成工具安装脚本
自动安装所有必要的依赖
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """检查 Python 版本是否满足要求"""
    if sys.version_info < (3, 6):
        print("错误: 需要 Python 3.6 或更高版本")
        sys.exit(1)

def check_nodejs():
    """检查是否安装了 Node.js"""
    try:
        subprocess.run(["node", "--version"], 
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE,
                      check=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def install_nodejs():
    """提供安装 Node.js 的指导"""
    system = platform.system()
    print("未检测到 Node.js，请安装 Node.js:")
    
    if system == "Windows":
        print("1. 访问 https://nodejs.org/")
        print("2. 下载并安装 Node.js")
    elif system == "Darwin":  # macOS
        print("1. 使用 Homebrew: brew install node")
        print("   或访问 https://nodejs.org/ 下载安装包")
    elif system == "Linux":
        print("1. 使用包管理器安装，例如:")
        print("   - Ubuntu/Debian: sudo apt install nodejs npm")
        print("   - CentOS/RHEL: sudo yum install nodejs")
        print("   或访问 https://nodejs.org/ 获取其他安装方法")
    
    print("\n安装 Node.js 后，请重新运行此脚本")
    sys.exit(1)

def install_mermaid_cli():
    """安装 mermaid-cli"""
    print("正在安装 mermaid-cli...")
    try:
        subprocess.run(["npm", "install", "-g", "@mermaid-js/mermaid-cli"], 
                      check=True)
        print("mermaid-cli 安装成功")
        return True
    except subprocess.SubprocessError:
        print("安装 mermaid-cli 失败，请手动运行:")
        print("npm install -g @mermaid-js/mermaid-cli")
        return False

def install_python_deps():
    """安装 Python 依赖"""
    print("正在安装 Python 依赖...")
    try:
        # 安装 requirements.txt 中的依赖
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True)
        
        # 安装 Flask (用于 Web GUI)
        subprocess.run([sys.executable, "-m", "pip", "install", "flask"], 
                      check=True)
        
        # 以开发模式安装当前包
        subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."], 
                      check=True)
        
        print("Python 依赖安装成功")
        return True
    except subprocess.SubprocessError:
        print("安装 Python 依赖失败，请手动运行:")
        print(f"{sys.executable} -m pip install -r requirements.txt")
        print(f"{sys.executable} -m pip install flask")
        print(f"{sys.executable} -m pip install -e .")
        return False

def check_mermaid_cli():
    """检查是否安装了 mermaid-cli"""
    try:
        subprocess.run(["mmdc", "--version"], 
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE,
                      check=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def check_tkinter():
    """检查是否安装了 Tkinter"""
    try:
        import tkinter
        return True
    except ImportError:
        return False

def main():
    """主函数"""
    print("=== Mermaid 流程图生成工具安装程序 ===")
    
    # 检查 Python 版本
    check_python_version()
    print("✓ Python 版本检查通过")
    
    # 检查并安装 Node.js
    if not check_nodejs():
        install_nodejs()
    print("✓ Node.js 已安装")
    
    # 检查并安装 mermaid-cli
    if not check_mermaid_cli():
        if not install_mermaid_cli():
            sys.exit(1)
    print("✓ mermaid-cli 已安装")
    
    # 安装 Python 依赖
    if not install_python_deps():
        sys.exit(1)
    print("✓ Python 依赖已安装")
    
    # 检查 Tkinter
    if not check_tkinter():
        print("警告: 未检测到 Tkinter 支持，图形界面将无法使用")
        print("您仍然可以使用命令行界面: python mermaid_generator.py")
        print("\n要安装 Tkinter 支持，请参考以下步骤:")
        if platform.system() == "Darwin":  # macOS
            print("在 macOS 上:")
            print("1. brew install python-tk@3.12")
            print("   或重新安装 Python: brew reinstall python@3.12 --with-tcl-tk")
        elif platform.system() == "Linux":
            print("在 Linux 上:")
            print("1. Ubuntu/Debian: sudo apt-get install python3-tk")
            print("2. Fedora: sudo dnf install python3-tkinter")
            print("3. CentOS/RHEL: sudo yum install python3-tkinter")
        elif platform.system() == "Windows":
            print("在 Windows 上:")
            print("1. 通常 Python 安装已包含 Tkinter")
            print("2. 如果没有，请重新安装 Python 并确保选中 'tcl/tk and IDLE' 选项")
    
    print("\n=== 安装完成! ===")
    print("您现在可以使用以下命令运行 Mermaid 流程图生成工具:")
    print("1. 命令行界面: mermaid-gen -h")
    print("2. 图形界面: mermaid-gui")
    print("\n或者直接运行 Python 脚本:")
    print("1. 命令行界面: python mermaid_generator.py -h")
    print("2. 图形界面: python mermaid_gui.py")

if __name__ == "__main__":
    main() 