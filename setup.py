from setuptools import setup, find_packages

setup(
    name="mermaid-generator",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "Pillow",
        "flask",
    ],
    entry_points={
        'console_scripts': [
            'mermaid-gen=mermaid_generator:main',
            'mermaid-gui=mermaid_gui:main',
            'mermaid-web=mermaid_web_gui:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="一个将 Mermaid 语法转换为流程图的工具",
    keywords="mermaid, diagram, flowchart",
    python_requires=">=3.6",
) 