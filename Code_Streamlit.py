import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px

# -----------------------
# 기본 설정
# -----------------------
st.set_page_config(page_title="Job Crawling Summary", layout="wide")

st.title("Title")

# -----------------------
# 데이터 불러오기
# -----------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data_tmp"

saramin = pd.read_csv(DATA_DIR / "data_saramin.csv")
jobkorea = pd.read_csv(DATA_DIR / "data_jobkorea.csv")

# site 컬럼 통일
if "site" in saramin.columns:
    saramin = saramin.rename(columns={"site": "Site"})
if "site" in jobkorea.columns:
    jobkorea = jobkorea.rename(columns={"site": "Site"})

# 혹시 값이 없다면 명시적으로 채우기
saramin["Site"] = saramin.get("Site", "Saramin")
jobkorea["Site"] = jobkorea.get("Site", "Job_Korea")

# 두 사이트 데이터 합치기
data = pd.concat([jobkorea, saramin], ignore_index=True)

# 우리가 보여 줄 컬럼만 사용
display_cols = ["Site", "Col_Company", "Col_Recruit"]
data_display = data[display_cols].copy()

# -----------------------
# 버튼
# -----------------------
clicked = st.button("Recruit Searching")

st.markdown("---")

# -----------------------
# 버튼 눌렀을 때 화면
# -----------------------
if clicked:
    # 두 번째 Title (예시 화면과 동일하게)
    st.title("Title")

    # 위쪽에 버튼 한 번 더 (모양만 필요)
    st.button("Recruit Searching", key="second_button")

    # ----- 메인 테이블 -----
    def highlight_site(row):
        """Site 값에 따라 행 색깔 다르게"""
        if row["Site"] == "Job_Korea":
            return ["background-color: #e6f2ff"] * len(row)  # 연한 파랑
        elif row["Site"].lower().startswith("saram"):
            return ["background-color: #f2ffe6"] * len(row)  # 연한 초록
        else:
            return [""] * len(row)

    styled_table = data_display.style.apply(highlight_site, axis=1)

    st.dataframe(styled_table, use_container_width=True)

    # ----- 사이트별 개수 / 비율 테이블 -----
    summary = (
        data_display.groupby("Site")
        .size()
        .reset_index(name="Count")
        .sort_values("Site")
    )
    total = summary["Count"].sum()
    summary["Ratio"] = (summary["Count"] / total * 100).round(2)

    st.dataframe(summary, use_container_width=False)

    # ----- 파이 차트 -----
    fig = px.pie(
        summary,
        names="Site",
        values="Count",
        title="Recruitment Ratio",
        hole=0,  # 일반 원형
    )
    st.plotly_chart(fig, use_container_width=True)
