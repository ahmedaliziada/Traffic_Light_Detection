"""Utility modules for traffic light detection."""

from .detection import detect_traffic_light_color
from .image_processing import process_detection_results

__all__ = ['detect_traffic_light_color', 'process_detection_results']
