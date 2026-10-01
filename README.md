AI 简历匹配分析器

一个基于 Streamlit 和 DeepSeek API 的 AI 应用，用于分析简历与岗位描述的匹配程度，并给出针对性的修改建议。

在线体验

https://ai-resume-analyzer-76y824854dytydvgxoqysy.streamlit.app/

项目功能

输入简历内容

输入目标岗位描述

生成 0-100 分的岗位匹配评分

展示简历与岗位的匹配优点

指出关键能力缺口

给出简历优化建议

支持部署为公网应用，方便随时访问

技术栈

Python

Streamlit

OpenAI Python SDK

DeepSeek Chat API

Streamlit Community Cloud

实现思路

使用 Streamlit 构建双栏输入界面。

将简历与岗位描述组织成结构化提示词，发送给 DeepSeek API。

要求模型返回固定 JSON 格式，保证结果可以稳定展示。

解析返回结果，并通过评分条、评价、优点、缺口和建议等模块展示。

使用 Streamlit Secrets 管理 API Key，避免将密钥上传到 GitHub。

将项目部署到 Streamlit Community Cloud，生成可公开访问的演示地址。

本地运行

python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py

本地运行时，需要在 .streamlit/secrets.toml 中配置：

DEEPSEEK_API_KEY = "你的API Key"

项目结构

ai-resume-analyzer/
├── .streamlit/
│   └── secrets.toml
├── app.py
├── requirements.txt
├── .gitignore
└── README.md

后续可以继续完善

支持上传 PDF 或 Word 简历

保存历史分析记录

支持导出分析报告

增加多个岗位对比功能

优化移动端显示效果