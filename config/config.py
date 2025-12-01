"""
Configuration settings for Traffic Light Detection System.
"""

import numpy as np

# Application Settings
APP_TITLE = "Traffic Light Detection System"
APP_ICON = "🚦"
PAGE_LAYOUT = "wide"

# Model Configuration
MODEL_NAME = "yolov5s"
MODEL_REPO = "ultralytics/yolov5"
CONFIDENCE_THRESHOLD = 0.25 # Minimum confidence for detections

# Traffic Light Detection
TARGET_CLASS = "traffic light"

# Minimum pixel threshold to consider a color as present (reduces false positives)
MIN_PIXEL_THRESHOLD = 50

# Color Detection Ranges (HSV Color Space)
# H (Hue): 0-180, S (Saturation): 0-255, V (Value/Brightness): 0-255
COLOR_RANGES = {
    "red": {
        "lower1": np.array([0, 100, 100]),      # Brighter red (increased V from 50 to 100)
        "upper1": np.array([10, 255, 255]),
        "lower2": np.array([170, 100, 100]),    # Brighter red (increased V from 50 to 100)
        "upper2": np.array([180, 255, 255])
    },
    "green": {
        "lower": np.array([40, 50, 50]),        # More saturated green (increased S and V)
        "upper": np.array([90, 255, 255])       # Wider hue range for green
    },
    "yellow": {
        "lower": np.array([15, 100, 100]),      # Adjusted hue range
        "upper": np.array([35, 255, 255])       # Wider to catch amber lights
    }
}

# Image Upload Settings
ALLOWED_IMAGE_TYPES = ['png', 'jpeg', 'jpg']
MAX_IMAGE_WIDTH = 800

# Display Settings
THUMBNAIL_WIDTH = 500
RESULT_IMAGE_WIDTH = 800

# Color Display Configuration
COLOR_EMOJIS = {
    "red": "🔴",
    "yellow": "🟡",
    "green": "🟢"
}

COLOR_MESSAGES = {
    "red": "RED LIGHT - STOP",
    "yellow": "YELLOW LIGHT - CAUTION",
    "green": "GREEN LIGHT - GO"
}
