from pathlib import Path
import sys

# Get the absolute path of the current file
FILE = Path(__file__).resolve()
# Get the parent directory of the current file
ROOT = FILE.parent
# Add the root path to the sys.path list if it is not already there
if ROOT not in sys.path:
    sys.path.append(str(ROOT))
# Get the relative path of the root directory with respect to the current working directory
ROOT = ROOT.relative_to(Path.cwd())

# Sources
IMAGE = 'Image'
VIDEO = 'Video'
# WEBCAM = 'Webcam'
# RTSP = 'RTSP'
# YOUTUBE = 'YouTube'

SOURCES_LIST = [IMAGE, VIDEO]

# Images config

# todo :- 이미지 바꾸기

IMAGES_DIR = ROOT / 'images'
DEFAULT_IMAGE = IMAGES_DIR / 'thumb1.png'  
DEFAULT_DETECT_IMAGE = IMAGES_DIR / 'thumb2.png'  

# Videos config
VIDEO_DIR = ROOT / 'videos'
VIDEOS_DICT = {
    'video_1': VIDEO_DIR / 'testVideox264.mp4',
    'video_2': VIDEO_DIR / 'testVideox264.mp4',
    'video_3': VIDEO_DIR / 'testVideox264.mp4',
    'testVideo': VIDEO_DIR / 'testVideox264.mp4',
    'test1': VIDEO_DIR / 'test1x264.mp4',
    'test2': VIDEO_DIR / 'test2x264.mp4',
    'test3': VIDEO_DIR / 'test3x264.mp4',
    'test4': VIDEO_DIR / 'test3x264.mp4',
    'test5': VIDEO_DIR / 'test3x264.mp4',
    'testVideo.mp4': VIDEO_DIR / 'testVidex264.mp4',
    'test1.mp4': VIDEO_DIR / 'test1x264.mp4',
    'test2.mp4': VIDEO_DIR / 'test2x264.mp4',
    'test3.mp4': VIDEO_DIR / 'test3x264.mp4',
    'test4.mp4': VIDEO_DIR / 'testVideox264.mp4',
    'test5.mp4': VIDEO_DIR / 'testVideox264.mp4',
    'test1x264.mp4': VIDEO_DIR / 'test1x264.mp4',
    'test2x264.mp4': VIDEO_DIR / 'test2x264.mp4',
    'test3x264.mp4': VIDEO_DIR / 'test3x264.mp4',
    'testVideox264.mp4': VIDEO_DIR / 'testVideox264.mp4'
}

# ML Model config
MODEL_DIR = ROOT / 'weights'
DETECTION_MODEL = MODEL_DIR / 'best_50.pt'
# In case of your custome model comment out the line above and
# Place your custom model pt file name at the line below 
# DETECTION_MODEL = MODEL_DIR / 'my_detection_model.pt'

# SEGMENTATION_MODEL = MODEL_DIR / 'yolov8n-seg.pt'

# Webcam
# WEBCAM_PATH = 0
