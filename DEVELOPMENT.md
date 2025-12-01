# Development Guide

## 🛠️ Developer Documentation

This guide helps developers understand, modify, and extend the Traffic Light Detection System.

## 📋 Table of Contents

1. [Setup Development Environment](#setup-development-environment)
2. [Project Structure](#project-structure)
3. [Adding New Features](#adding-new-features)
4. [Testing](#testing)
5. [Code Style](#code-style)
6. [Common Tasks](#common-tasks)

## 🚀 Setup Development Environment

### Prerequisites

```bash
# Required
Python 3.8+
pip
git

# Recommended
Visual Studio Code with Python extension
```

### Initial Setup

```bash
# Clone repository
git clone <repository-url>
cd Traffic_Light_Detection

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (optional)
pip install pytest black flake8 mypy
```

### Running in Development Mode

```bash
# Run with auto-reload
streamlit run app.py

# Run with specific configuration
streamlit run app.py --server.port 8080 --logger.level debug
```

## 📁 Project Structure

```
Traffic_Light_Detection/
│
├── app.py                    # Main application entry
├── config/
│   └── config.py            # Configuration constants
│
├── src/
│   ├── models/              # Model management
│   │   └── yolo_model.py
│   ├── utils/               # Business logic
│   │   ├── detection.py
│   │   └── image_processing.py
│   └── ui/                  # User interface
│       ├── components.py
│       └── styles.py
│
└── tests/                   # Test suite
    └── test_detection.py
```

## ✨ Adding New Features

### 1. Adding a New Color Detection

**File**: `config/config.py`

```python
COLOR_RANGES = {
    "red": {...},
    "yellow": {...},
    "green": {...},
    # Add new color
    "blue": {
        "lower": np.array([90, 50, 50]),
        "upper": np.array([130, 255, 255])
    }
}

COLOR_EMOJIS = {
    # ...existing colors...
    "blue": "🔵"
}

COLOR_MESSAGES = {
    # ...existing colors...
    "blue": "BLUE LIGHT - SPECIAL"
}
```

**File**: `src/utils/detection.py`

```python
def _count_blue_pixels(hsv_image: np.ndarray) -> int:
    """Count blue pixels in HSV image."""
    blue_config = COLOR_RANGES["blue"]
    blue_mask = cv2.inRange(hsv_image, blue_config["lower"], blue_config["upper"])
    return cv2.countNonZero(blue_mask)

# Update detect_traffic_light_color function
def detect_traffic_light_color(image, box):
    # ...existing code...
    blue_pixels = _count_blue_pixels(hsv_image)
    
    # Update determination
    color = _determine_dominant_color(red_pixels, green_pixels, yellow_pixels, blue_pixels)
```

### 2. Adding a New Model

**File**: `src/models/new_model.py`

```python
import torch

class NewModelHandler:
    """Handler for custom detection model."""
    
    def __init__(self):
        self.model = self._load_model()
    
    def _load_model(self):
        # Load your custom model
        pass
    
    def detect(self, image):
        # Implement detection logic
        pass
```

**File**: `app.py`

```python
# Import new model
from src.models.new_model import NewModelHandler

# Use in application
model = NewModelHandler()
```

### 3. Adding a New UI Component

**File**: `src/ui/components.py`

```python
def render_statistics_chart(results: List[DetectionResult]):
    """
    Render a chart of detection statistics.
    
    Args:
        results: List of detection results
    """
    import matplotlib.pyplot as plt
    
    # Create chart
    colors = [r.color for r in results]
    counts = {}
    for color in colors:
        counts[color] = counts.get(color, 0) + 1
    
    # Display with Streamlit
    st.bar_chart(counts)
```

**File**: `app.py`

```python
from src.ui.components import render_statistics_chart

# Use in main application
if results:
    render_statistics_chart(results)
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_detection.py

# Run with coverage
python -m pytest tests/ --cov=src

# Run with verbose output
python -m pytest tests/ -v
```

### Writing New Tests

**File**: `tests/test_new_feature.py`

```python
import unittest
from src.utils.detection import new_function

class TestNewFeature(unittest.TestCase):
    """Test cases for new feature."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_data = [1, 2, 3]
    
    def test_basic_functionality(self):
        """Test basic functionality."""
        result = new_function(self.test_data)
        self.assertEqual(result, expected_value)
    
    def test_edge_case(self):
        """Test edge cases."""
        result = new_function([])
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
```

## 📝 Code Style

### Python Style Guide (PEP 8)

```python
# Good: Clear naming, type hints, docstrings
def process_image(image: np.ndarray, threshold: float = 0.5) -> List[DetectionResult]:
    """
    Process image and return detection results.
    
    Args:
        image: Input image array
        threshold: Confidence threshold for detections
    
    Returns:
        List of detection results
    """
    # Implementation
    pass

# Bad: No type hints, unclear naming, no documentation
def proc(img, t=0.5):
    pass
```

### Documentation

```python
def function_name(param1: type, param2: type) -> return_type:
    """
    Brief description of function.
    
    Detailed description if needed. Explain what the function does,
    any important algorithms used, or edge cases handled.
    
    Args:
        param1 (type): Description of first parameter
        param2 (type): Description of second parameter
    
    Returns:
        return_type: Description of return value
    
    Raises:
        ErrorType: Description of when this error is raised
    
    Examples:
        >>> result = function_name(value1, value2)
        >>> print(result)
        expected_output
    """
    pass
```

### Import Organization

```python
# Standard library imports
import os
import sys
from typing import List, Dict

# Third-party imports
import numpy as np
import cv2
import torch
import streamlit as st

# Local application imports
from src.models.yolo_model import YOLOModelHandler
from src.utils.detection import detect_traffic_light_color
from config.config import MODEL_NAME
```

## 🔧 Common Tasks

### Task 1: Adjust Detection Sensitivity

**File**: `config/config.py`

```python
# Increase confidence threshold for stricter detection
CONFIDENCE_THRESHOLD = 0.7  # Default: 0.5

# Adjust color ranges for better detection
COLOR_RANGES = {
    "red": {
        "lower1": np.array([0, 100, 100]),  # Increased saturation
        "upper1": np.array([10, 255, 255]),
        # ...
    }
}
```

### Task 2: Add Logging

```python
import logging

# Configure logger
logger = logging.getLogger(__name__)

# Use throughout code
logger.info("Processing image...")
logger.warning("Low confidence detection")
logger.error(f"Error occurred: {e}")
```

### Task 3: Optimize Performance

```python
# Use caching for expensive operations
@st.cache_data
def expensive_operation(data):
    # Cached result
    return processed_data

# Batch processing
def process_multiple_images(images: List[np.ndarray]):
    """Process multiple images efficiently."""
    results = []
    for image in images:
        result = process_single_image(image)
        results.append(result)
    return results
```

### Task 4: Add Configuration Options

**File**: `config/config.py`

```python
# Add new configuration
DETECTION_MODE = "accurate"  # Options: "fast", "accurate"
BATCH_SIZE = 32
ENABLE_GPU = True
```

**File**: `app.py`

```python
from config.config import DETECTION_MODE, ENABLE_GPU

if DETECTION_MODE == "accurate":
    # Use more thorough detection
    pass
```

### Task 5: Export Results

```python
import json

def export_results(results: List[DetectionResult], filename: str):
    """Export detection results to JSON."""
    data = [r.to_dict() for r in results]
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

# In UI
if st.button("Export Results"):
    export_results(results, "detection_results.json")
    st.success("Results exported!")
```

## 🐛 Debugging

### Enable Debug Mode

```python
# In app.py
import logging
logging.basicConfig(level=logging.DEBUG)

# Or via Streamlit
streamlit run app.py --logger.level debug
```

### Common Issues

**Issue**: Model not loading
```python
# Check model path and internet connection
logger.info(f"Loading model from: {MODEL_REPO}")
```

**Issue**: Color detection inaccurate
```python
# Visualize HSV image
hsv_debug = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
st.image(hsv_debug, caption="HSV Image")
```

**Issue**: Performance slow
```python
# Profile code
import time
start = time.time()
# Your code here
logger.info(f"Execution time: {time.time() - start:.2f}s")
```

## 📚 Resources

### Documentation
- [Streamlit Docs](https://docs.streamlit.io/)
- [YOLOv5 Docs](https://docs.ultralytics.com/)
- [OpenCV Python](https://docs.opencv.org/master/d6/d00/tutorial_py_root.html)
- [PyTorch Docs](https://pytorch.org/docs/stable/index.html)

### Learning
- [Computer Vision Course](https://www.coursera.org/learn/introduction-computer-vision-watson-opencv)
- [Object Detection Tutorial](https://pytorch.org/tutorials/intermediate/torchvision_tutorial.html)
- [Streamlit Tutorial](https://docs.streamlit.io/library/get-started)

## 🤝 Contributing

1. Create feature branch: `git checkout -b feature/amazing-feature`
2. Make changes following code style
3. Add tests for new functionality
4. Update documentation
5. Commit changes: `git commit -m 'Add amazing feature'`
6. Push to branch: `git push origin feature/amazing-feature`
7. Open Pull Request

## 📞 Support

- GitHub Issues: For bug reports and feature requests
- Documentation: Check README.md and ARCHITECTURE.md
- Code Comments: Inline documentation in source files

---

Happy coding! 🚀
