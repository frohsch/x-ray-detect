# Python In-built packages
from pathlib import Path
import PIL
import os

# External packages
import streamlit as st
from st_pages import Page, show_pages, add_page_title

# Local Modules
import settings
import helper

#s3 연결
import boto3

#코드 수정중!!
access_key_id = 'orangeorange'
secret_access_key = 'orangeisyummy'
bucket_name = 'orangestreamlit'
def get_s3():
    s3 = boto3.resource('s3', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)  
    return s3
def save_file(fl):
    file_name = fl.name
    s3 = get_s3()
    s3.Bucket(bucket_name).put_object(Key=file_name, Body=fl)
    st.write('Success! File Saved!')
#파일 오픈하는 코드 작성해야함
#여기가 수정한코드!!!!!!!!!!!!!!!!

# Setting page layout
st.set_page_config(
    page_title="Orange",
    page_icon="🍊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page heading
st.title("Object Detection with 🍊ORANGE🍊")


show_pages(
    [
        Page("app.py", "Home", "🏠"),
        Page("database.py", "Database", "📑"),
    ]
)

st.sidebar.header("Model")
# Model Options
model_type = st.sidebar.radio(
    "Select Task", ['Detection'])

confidence = float(st.sidebar.slider(
    "Select Model Confidence", 25, 100, 40)) / 100

# Selecting Detection Or Segmentation
# if model_type == 'Detection':
model_path = Path(settings.DETECTION_MODEL)
# elif model_type == 'Segmentation':
    # model_path = Path(settings.SEGMENTATION_MODEL)

# Load Pre-trained ML Model
try:
    model = helper.load_model(model_path)
except Exception as ex:
    st.error(f"Unable to load model. Check the specified path: {model_path}")
    st.error(ex)

st.sidebar.header("Image/Video Config")
source_radio = st.sidebar.radio(
    "Select Source", settings.SOURCES_LIST)

source_img = None
# If image is selected
if source_radio == settings.IMAGE:
    source_img = st.sidebar.file_uploader(
        "Choose an image...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))

    col1, col2 = st.columns(2)

    with col1:
        try:
            if source_img is None:
                default_image_path = str(settings.DEFAULT_IMAGE)
                default_image = PIL.Image.open(default_image_path)
                st.image(default_image_path, caption="Default Image",
                         use_column_width=True)
            else:
                uploaded_image = PIL.Image.open(source_img)
                st.image(source_img, caption="Uploaded Image",
                         use_column_width=True)
        except Exception as ex:
            st.error("Error occurred while opening the image.")
            st.error(ex)

    with col2:
        if source_img is None:
            default_detected_image_path = str(settings.DEFAULT_DETECT_IMAGE)
            default_detected_image = PIL.Image.open(
                default_detected_image_path)
            st.image(default_detected_image_path, caption='Detected Image',
                     use_column_width=True)
        else:
            if st.sidebar.button('Detect Objects'):
                res = model.predict(uploaded_image,
                                    conf=confidence
                                    )
                # todo :- db로 저장하기
                
                boxes = res[0].boxes
                res_plotted = res[0].plot()[:, :, ::-1]
                st.image(res_plotted, caption='Detected Image',
                         use_column_width=True)
                
                try:
                    with st.expander("Detection Results"):
                        for box in boxes:
                            st.write(box.data)
                except Exception as ex:
                    st.write(ex)
                    st.write("No image is uploaded yet!")

elif source_radio == settings.VIDEO:
    source_video = st.sidebar.file_uploader(
        "Choose an video...", type=("mp4"))
        
    # todo :- 수정하기 
    # source_video s3에 저장하기 
    # s3에서 불러와서 경로 아래 source_video에 파라미터로 넣기
    
    if source_video is not None: 
        input_path = source_video.name
        save_path = "uploaded_videos"
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        file_path = os.path.join(save_path, input_path)
        print(input_path)
        file_binary = source_video.read()
        with open(file_path, "wb") as temp_file:
            temp_file.write(source_video.getbuffer())
        st.video(source_video)
        helper.play_stored_video(confidence, model, input_path, source_video)
    
else:
    st.error("Please select a valid source type!")
