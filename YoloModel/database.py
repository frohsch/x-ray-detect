import streamlit as st
import pandas as pd
import json
import numpy as np

# Setting page layout
st.set_page_config(
    page_title="Orange",
    page_icon="🍊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Sidebar Settings
st.sidebar.header("Data")

# 전체 기내/위탁 수화물
model_type = st.sidebar.radio(
    "Select Data", ['All', 'Cabin baggage', 'Checked baggage'])

# Main page heading
st.title("Database 📑")
st.subheader("Detection Results")


# 시각화 선택
st.sidebar.header("Visualization")


visual_type = st.sidebar.radio(
    "visualization", ['Table', 'Bar Chart', 'Timing Analysis'])

if visual_type == 'Table':
    # JSON 파일 로드
    with open('data.json', 'r') as file:
        data = json.load(file)
    
    # detections 리스트를 DataFrame으로 변환
    detections = data['detections']
    df_detections = pd.json_normalize(detections)#
    
    # 'timing' 관련 컬럼을 추출하여 앞쪽으로 배치
    resolution_cols = [col for col in df_detections if col.startswith('resolution')]
    timing_cols = [col for col in df_detections if col.startswith('timing.')]
    other_cols = [col for col in df_detections if col.startswith('objects.')]
    new_order = resolution_cols + timing_cols + other_cols  # 새로운 컬럼 순서
    
    # 컬럼 순서를 변경
    df_reordered = df_detections[new_order]
    
    # Streamlit 앱에 변경된 DataFrame 표시
    st.dataframe(df_reordered)
elif visual_type == 'Bar Chart':
    # Json파일 읽고 DataFrame으로 변환
    with open('data_sum.json', 'r') as file:
        data_sum_js = json.load(file)
    
    data_sum = pd.json_normalize(data_sum_js)
    
    st.bar_chart(data_sum)
    
elif visual_type == 'Timing Analysis':
    # Json파일 읽고 DataFrame으로 변환
    with open('time_data.json', 'r') as file:
        time_data_js = json.load(file)
    
    time_data = pd.json_normalize(time_data_js)
    
    st.line_chart(time_data)
