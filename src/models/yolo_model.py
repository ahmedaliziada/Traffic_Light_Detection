"""
YOLO Model Handler for Traffic Light Detection.
Manages model loading, caching, and inference.
"""

import torch
import streamlit as st
from typing import Optional
import logging

from config.config import MODEL_NAME, MODEL_REPO

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@st.cache_resource
def _load_yolo_model():
    """
    Load the YOLOv5 model with caching for performance.
    
    Returns:
        torch.nn.Module: Loaded YOLOv5 model or None if loading fails
    """
    try:
        logger.info(f"Loading {MODEL_NAME} model from {MODEL_REPO}...")
        model = torch.hub.load(MODEL_REPO, MODEL_NAME)
        logger.info("Model loaded successfully!")
        return model
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        st.error(f"Failed to load YOLOv5 model: {str(e)}")
        return None


class YOLOModelHandler:
    """Handler class for YOLOv5 model operations."""
    
    def __init__(self):
        """Initialize the model handler."""
        self.model = _load_yolo_model()
    
    def detect(self, image):
        """
        Perform object detection on an image.
        
        Args:
            image: Input image (numpy array or PIL Image)
        
        Returns:
            Detection results from YOLOv5
        """
        if self.model is None:
            raise RuntimeError("Model not loaded. Cannot perform detection.")
        
        try:
            results = self.model(image)
            return results
        except Exception as e:
            logger.error(f"Error during detection: {str(e)}")
            raise
    
    def is_loaded(self) -> bool:
        """
        Check if the model is successfully loaded.
        
        Returns:
            bool: True if model is loaded, False otherwise
        """
        return self.model is not None
    
    def get_model_info(self) -> dict:
        """
        Get information about the loaded model.
        
        Returns:
            dict: Model information
        """
        return {
            "name": MODEL_NAME,
            "repository": MODEL_REPO,
            "loaded": self.is_loaded()
        }
