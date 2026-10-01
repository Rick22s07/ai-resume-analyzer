import json
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="AI 简历匹配分析器")
st.title("AI 简历匹配分析器")
st.write("输入简历和岗位描述，生成匹配分析。")

client = OpenAI(
    api_key=st.secrets["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com",
)


def analyze_resume(resume_text, job_text):
    prompt = f"""
你是一名资深招聘专家。请分析下面的简历和岗位描述。

简历：
{resume_text}

岗位描述：
{job_text}

请只返回一个 JSON 对象，不要 Markdown，不要额外解释。
JSON 格式必须是这样：
{{
  "score": 0到100之间的整数,
  "summary": "总体评价",
  "strengths": ["匹配优点1", "匹配优点2", "匹配优点3"],
  "gaps": ["能力缺口1", "能力缺口2", "能力缺口3"],
  "suggestions": ["简历修改建议1", "简历修改建议2", "简历修改建议3"]
}}
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": "你擅长分析简历与岗位的匹配程度，回答必须准确、简洁、可执行。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    content = response.choices[0].message.content.strip()
    if content.startswith("```"):
        content = content.replace("```json", "").replace("```", "").strip()

    return json.loads(content)

sample_resume = """
张三
求职方向：Python 后端开发

技能：
- Python
- FastAPI
- MySQL
- Git

项目经历：
- 开发过一个个人博客 API，支持文章增删改查和用户登录
- 使用 FastAPI 和 MySQL 完成数据接口
- 将项目部署到云服务器，并使用 Git 管理代码
"""

sample_job = """
岗位：Python 后端开发工程师

岗位职责：
- 负责后端接口设计和开发
- 参与数据库设计和性能优化
- 与前端工程师协作完成产品功能

任职要求：
- 熟悉 Python
- 熟悉至少一种 Web 框架，如 FastAPI 或 Django
- 了解 MySQL 和 Redis
- 熟悉 Git 和 Linux
- 有云服务器部署经验优先
"""

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "job_text" not in st.session_state:
    st.session_state.job_text = ""

if st.button("加载示例"):
    st.session_state.resume_text = sample_resume
    st.session_state.job_text = sample_job

with st.form("resume_form"):
    left, right = st.columns(2)

    with left:
        resume_text = st.text_area(
            "你的简历",
            height=300,
            placeholder="把简历内容粘贴到这里",
            key="resume_text"
        )

    with right:
        job_text = st.text_area(
            "岗位描述",
            height=300,
            placeholder="把岗位描述粘贴到这里",
            key="job_text"
        )

    submitted = st.form_submit_button("开始分析", use_container_width=True)

if submitted:
    if not resume_text.strip() or not job_text.strip():
        st.warning("请同时填写简历和岗位描述")
    else:
        try:
            with st.spinner("正在分析，请稍等..."):
                result = analyze_resume(resume_text, job_text)

            st.metric("匹配分数", f"{result['score']} / 100")
            st.progress(result["score"] / 100)

            st.subheader("总体评价")
            st.info(result["summary"])

            left_col, middle_col, right_col = st.columns(3)

            with left_col:
                st.subheader("匹配优点")
                for item in result["strengths"]:
                    st.markdown(f"- {item}")

            with middle_col:
                st.subheader("能力缺口")
                for item in result["gaps"]:
                    st.markdown(f"- {item}")

            with right_col:
                st.subheader("修改建议")
                for item in result["suggestions"]:
                    st.markdown(f"- {item}")

        except Exception as error:
            st.error(f"分析失败：{error}")