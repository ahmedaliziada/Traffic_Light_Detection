"""
Traffic Light Detection System - Main Application
A professional Computer Vision application for real-time traffic light detection and classification.

Author: Traffic Light Detection Team
Version: 1.0.0
"""

import streamlit as st
from PIL import Image
import numpy as np
import logging

# Import custom modules
from src.models.yolo_model import YOLOModelHandler
from src.utils.image_processing import process_detection_results, get_detection_summary
from src.ui.styles import apply_custom_styles
from src.ui.components import (
    render_header,
    render_about_section,
    render_sidebar,
    render_upload_section,
    render_detection_results,
    render_summary_statistics,
    render_annotated_image
)
from config.config import (
    APP_TITLE,
    APP_ICON,
    PAGE_LAYOUT,
    THUMBNAIL_WIDTH,
    RESULT_IMAGE_WIDTH
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def configure_page():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=APP_ICON,
        layout=PAGE_LAYOUT,
        initial_sidebar_state="expanded"
    )


def initialize_model() -> YOLOModelHandler:
    """
    Initialize the YOLO model handler.
    
    Returns:
        YOLOModelHandler: Initialized model handler instance
    """
    logger.info("Initializing YOLO model...")
    model_handler = YOLOModelHandler()
    
    if model_handler.is_loaded():
        logger.info("Model loaded successfully!")
    else:
        logger.error("Failed to load model")
        st.error("❌ Failed to load the YOLOv5 model. Please check your internet connection and try again.")
    
    return model_handler


def process_uploaded_image(upload, model_handler: YOLOModelHandler):
    """
    Process the uploaded image and perform traffic light detection.
    
    Args:
        upload: Streamlit uploaded file object
        model_handler (YOLOModelHandler): Initialized model handler
    """
    # Load and display uploaded image
    col1, col2 = st.columns([1, 1])
    
    with col1:
        img = Image.open(upload)
        image_array = np.array(img)
        st.image(image_array, caption='Uploaded Image', width=THUMBNAIL_WIDTH)
    
    with col2:
        # Perform detection
        with st.spinner("🔄 Detecting traffic lights..."):
            try:
                # Run YOLO detection
                detection_output = model_handler.detect(image_array)
                
                # Process detection results
                results = process_detection_results(detection_output, image_array)
                
                # Display individual detection results
                render_detection_results(results)
                
                # Display summary statistics if detections found
                if results:
                    summary = get_detection_summary(results)
                    render_summary_statistics(summary)
                
            except Exception as e:
                logger.error(f"Error during detection: {str(e)}")
                st.error(f"❌ An error occurred during detection: {str(e)}")
                return
    
    # Display annotated image with bounding boxes
    if results:
        rendered_image = detection_output.render()[0]
        render_annotated_image(rendered_image, width=RESULT_IMAGE_WIDTH)
        st.success("✅ Detection completed successfully!")


def main():
    """Main application entry point."""
    # Configure page
    configure_page()
    
    # Apply custom styles
    apply_custom_styles()
    
    # Render UI components
    render_header()
    render_about_section()
    render_sidebar()
    
    # Initialize model
    model_handler = initialize_model()
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        upload = render_upload_section()
    
    # Process uploaded image if available
    if upload is not None and model_handler.is_loaded():
        process_uploaded_image(upload, model_handler)
    elif upload is None:
        with col2:
            st.markdown("#### 🔍 Detection Results")
            st.info("👈 Upload an image to start detection")


if __name__ == "__main__":
    main()
