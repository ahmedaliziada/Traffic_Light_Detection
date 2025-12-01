"""
Streamlit UI components for Traffic Light Detection application.
"""

import streamlit as st
from typing import List
from src.utils.image_processing import DetectionResult
from config.config import COLOR_EMOJIS, COLOR_MESSAGES


def render_header():
    """Render the application header."""
    st.title('🚦 Traffic Light Detection System')
    st.markdown("### AI-Powered Smart Traffic Monitoring")
    st.markdown("---")


def render_about_section():
    """Render the expandable about section with project information."""
    with st.expander("ℹ️ About This Project", expanded=False):
        st.markdown("""
        #### Computer Vision & Deep Learning for Traffic Light Recognition
        
        This application uses **YOLOv5 (You Only Look Once)** object detection combined with color analysis 
        to detect and classify traffic lights in images. This technology is fundamental for autonomous 
        vehicles and intelligent transportation systems.
        
        **Key Technologies:**
        
        - **YOLOv5**: State-of-the-art real-time object detection
        - **Deep Learning**: Pre-trained convolutional neural networks
        - **Computer Vision**: OpenCV for color analysis
        - **HSV Color Space**: More robust color detection than RGB
        - **PyTorch**: Deep learning framework
        
        **How It Works:**
        1. **Object Detection**: YOLOv5 identifies traffic lights in the image
        2. **Region Extraction**: Crops detected traffic light regions
        3. **Color Space Conversion**: Converts RGB to HSV for better color detection
        4. **Color Analysis**: Analyzes pixel distribution for red, yellow, and green
        5. **Classification**: Determines the active light color
        
        **Detection Capabilities:**
        - 🔴 Red Light - Stop signal
        - 🟡 Yellow Light - Caution signal
        - 🟢 Green Light - Go signal
        - Multiple traffic lights in one image
        
        **Real-World Applications:**
        - Autonomous vehicle navigation
        - Smart city traffic management
        - Traffic violation detection systems
        - Driver assistance systems (ADAS)
        - Traffic flow analysis and optimization
        - Road safety monitoring
        """)


def render_sidebar():
    """Render the sidebar with configuration and information."""
    with st.sidebar:
        st.header("⚙️ Configuration")
        st.markdown("#### Model Information")
        st.info("""
        **Model**: YOLOv5s (Small)
        
        **Framework**: PyTorch
        
        **Detection Classes**: 80 COCO objects
        
        **Traffic Light Colors**:
        - 🔴 Red
        - 🟡 Yellow
        - 🟢 Green
        """)
        
        st.markdown("---")
        st.markdown("### 📊 Detection Process")
        st.markdown("""
        1. Upload traffic image
        2. YOLOv5 object detection
        3. HSV color analysis
        4. Color classification
        5. Results visualization
        """)
        
        st.markdown("---")
        st.markdown("### 🎯 Tips")
        st.info("""
        - Use clear, daylight images
        - Ensure traffic lights are visible
        - Works with multiple lights
        - Best with front-facing shots
        """)


def render_upload_section():
    """
    Render the file upload section.
    
    Returns:
        UploadedFile: The uploaded file object or None
    """
    st.markdown("#### 📤 Upload Image")
    upload = st.file_uploader(
        'Choose an image file',
        type=['png', 'jpeg', 'jpg'],
        help="Upload an image containing traffic lights"
    )
    return upload


def render_detection_result(result: DetectionResult):
    """
    Render a single detection result with color-coded styling.
    
    Args:
        result (DetectionResult): The detection result to display
    """
    color = result.color.lower()
    emoji = COLOR_EMOJIS.get(color, "⚪")
    message = COLOR_MESSAGES.get(color, "UNKNOWN COLOR")
    
    if color == 'red':
        css_class = 'traffic-light-red'
    elif color == 'yellow':
        css_class = 'traffic-light-yellow'
    elif color == 'green':
        css_class = 'traffic-light-green'
    else:
        st.warning(f"⚠️ Traffic Light #{result.index}: {result.color} (Confidence: {result.confidence:.2%})")
        return
    
    st.markdown(
        f'<div class="{css_class}">'
        f'<h3>{emoji} Traffic Light #{result.index}</h3>'
        f'<h2>{message}</h2>'
        f'<p>Confidence: {result.confidence:.2%}</p>'
        f'</div>',
        unsafe_allow_html=True
    )


def render_detection_results(results: List[DetectionResult]):
    """
    Render all detection results.
    
    Args:
        results (List[DetectionResult]): List of detection results to display
    """
    st.markdown("#### 🔍 Detection Results")
    
    if not results:
        st.warning("⚠️ No traffic lights detected in the image.")
        return
    
    for result in results:
        render_detection_result(result)


def render_summary_statistics(summary: dict):
    """
    Render summary statistics of detections.
    
    Args:
        summary (dict): Dictionary containing detection counts
    """
    st.markdown("---")
    st.markdown("##### 📊 Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Traffic Lights", summary['total'])
    with col2:
        st.metric("🔴 Red", summary['red'])
    with col3:
        st.metric("🟡 Yellow", summary['yellow'])
    with col4:
        st.metric("🟢 Green", summary['green'])


def render_annotated_image(rendered_image, width: int = 800):
    """
    Render the annotated image with bounding boxes.
    
    Args:
        rendered_image: The image with detection annotations
        width (int): Display width in pixels
    """
    st.markdown("---")
    st.markdown("#### 🎨 Annotated Image")
    st.image(rendered_image, caption="Detection Results", width=width)
