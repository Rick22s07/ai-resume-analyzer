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


with st.form("resume_form"):
    left, right = st.columns(2)

    with left:
        resume_text = st.text_area(
            "你的简历",
            height=300,
            placeholder="把简历内容粘贴到这里"
        )

    with right:
        job_text = st.text_area(
            "岗位描述",
            height=300,
            placeholder="把岗位描述粘贴到这里"
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