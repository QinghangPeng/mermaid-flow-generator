#!/usr/bin/env python3
"""
Mermaid 流程图生成工具
用于将 Mermaid 语法转换为流程图图像
"""

import os
import argparse
import tempfile
import subprocess
from pathlib import Path

class MermaidGenerator:
    def __init__(self):
        # 检查是否安装了必要的依赖
        self._check_dependencies()
    
    def _check_dependencies(self):
        """检查是否安装了必要的依赖"""
        try:
            # 检查 mmdc 命令是否可用
            subprocess.run(["mmdc", "--version"], 
                          stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE)
        except FileNotFoundError:
            print("错误: 未找到 mermaid-cli (mmdc)。")
            print("请按照以下步骤安装:")
            print("1. 确保已安装 Node.js")
            print("2. 运行: npm install -g @mermaid-js/mermaid-cli")
            exit(1)
    
    def generate_from_text(self, mermaid_text, output_path=None, format="png"):
        """
        从 Mermaid 文本生成流程图
        
        参数:
            mermaid_text (str): Mermaid 语法文本
            output_path (str): 输出文件路径，如果为 None，则使用临时文件
            format (str): 输出格式 (png, svg, pdf)
            
        返回:
            str: 生成的图像文件路径
        """
        # 创建临时文件来存储 Mermaid 文本
        with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False) as temp_file:
            temp_file.write(mermaid_text)
            input_path = temp_file.name
        
        # 如果未指定输出路径，创建临时输出文件
        if output_path is None:
            output_path = tempfile.mktemp(suffix=f'.{format}')
        
        # 使用 mermaid-cli 生成图像
        try:
            subprocess.run([
                "mmdc",
                "-i", input_path,
                "-o", output_path,
                "-f", format
            ], check=True)
            
            print(f"成功生成流程图: {output_path}")
            
            # 清理临时输入文件
            os.unlink(input_path)
            
            return output_path
        except subprocess.CalledProcessError as e:
            print(f"生成流程图时出错: {e}")
            # 清理临时文件
            os.unlink(input_path)
            if os.path.exists(output_path):
                os.unlink(output_path)
            return None
    
    def generate_from_file(self, input_file, output_path=None, format="png"):
        """
        从包含 Mermaid 语法的文件生成流程图
        
        参数:
            input_file (str): 输入文件路径
            output_path (str): 输出文件路径，如果为 None，则基于输入文件名生成
            format (str): 输出格式 (png, svg, pdf)
            
        返回:
            str: 生成的图像文件路径
        """
        # 读取输入文件
        with open(input_file, 'r') as f:
            mermaid_text = f.read()
        
        # 如果未指定输出路径，基于输入文件名生成
        if output_path is None:
            input_path = Path(input_file)
            output_path = str(input_path.with_suffix(f'.{format}'))
        
        return self.generate_from_text(mermaid_text, output_path, format)

def main():
    parser = argparse.ArgumentParser(description='Mermaid 流程图生成工具')
    
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('-t', '--text', help='Mermaid 语法文本')
    input_group.add_argument('-f', '--file', help='包含 Mermaid 语法的文件路径')
    
    parser.add_argument('-o', '--output', help='输出文件路径')
    parser.add_argument('--format', choices=['png', 'svg', 'pdf'], default='png',
                        help='输出格式 (默认: png)')
    
    args = parser.parse_args()
    
    generator = MermaidGenerator()
    
    if args.text:
        generator.generate_from_text(args.text, args.output, args.format)
    elif args.file:
        generator.generate_from_file(args.file, args.output, args.format)

if __name__ == "__main__":
    main() 