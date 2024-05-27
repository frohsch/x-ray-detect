from ultralytics import YOLO
import time
import streamlit as st
import cv2
from pytube import YouTube
from collections import defaultdict
import numpy as np

import settings


def load_model(model_path):
    """
    Loads a YOLO object detection model from the specified model_path.

    Parameters:
        model_path (str): The path to the YOLO model file.

    Returns:
        A YOLO object detection model.
    """
    model = YOLO(model_path)
    return model



def _display_detected_frames(conf, model, st_frame, image, is_display_tracking=None, tracker=None):
    """
    Display the detected objects on a video frame using the YOLOv8 model.

    Args:
    - conf (float): Confidence threshold for object detection.
    - model (YoloV8): A YOLOv8 object detection model.
    - st_frame (Streamlit object): A Streamlit object to display the detected video.
    - image (numpy array): A numpy array representing the video frame.
    - is_display_tracking (bool): A flag indicating whether to display object tracking (default=None).

    Returns:
    None
    """

    # Resize the image to a standard size
    image = cv2.resize(image, (720, int(720*(9/16))))

    # Display object tracking, if specified
    if is_display_tracking:
        # 여기가 실행됨
        res = model.track(image, conf=conf, persist=True, tracker=tracker)
        
    else:
        # Predict the objects in the image using the YOLOv8 model
        res = model.predict(image, conf=conf)

def play_stored_video(conf, model, video, source_video):
    """
    Plays a stored video file. Tracks and detects objects in real-time using the YOLOv8 object detection model.

    Parameters:
        conf: Confidence of YOLOv8 model.
        model: An instance of the `YOLOv8` class containing the YOLOv8 model.

    Returns:
        None

    Raises:
        None
    """
    # 동영상 업로드 부분
    # if(video != None): 
    #     source_vid = video
    #     is_display_tracker, tracker = True, "bytetrack.yaml"
    #     print("💚💚💚💚💚💚💚💚💚💚💚💚💚💚", source_vid, "💚💚💚💚💚💚💚💚💚💚💚💚💚💚")
    #     get = "uploaded_videos/" + source_vid
        
    # else:
    # 내장된 동영상
    # source_vid = st.sidebar.selectbox("Choose a video...", settings.VIDEOS_DICT.keys())
    is_display_tracker, tracker = True, "bytetrack.yaml"
    get = settings.VIDEOS_DICT.get(video)
    # print("💚💚💚💚💚💚💚💚💚💚💚💚💚💚", get, "💚💚💚💚💚💚💚💚💚💚💚💚💚💚")
    with open(get, 'rb') as video_file:
        video_bytes = video_file.read()
    if video_bytes:
        st.video(video_bytes)

    if st.sidebar.button('Detect Video Objects'):
        print("1")
        try:
            print("2")
            vid_cap = cv2.VideoCapture(
                str(settings.VIDEOS_DICT.get(video)))
            print("3" + str(vid_cap))
            st_frame = st.empty()
            while (vid_cap.isOpened()):
                success, image = vid_cap.read()
                if success:
                    _display_detected_frames(conf,
                                             model,
                                             st_frame,
                                             image,
                                             is_display_tracker,
                                             tracker
                                             )
                else:
                    vid_cap.release()
                    break
        except Exception as e:
            st.sidebar.error("Error loading video: " + str(e))
