"""
Color detection utilities for traffic light classification.
"""

import cv2
import numpy as np
from typing import Tuple, List
import logging

from config.config import COLOR_RANGES, MIN_PIXEL_THRESHOLD

logger = logging.getLogger(__name__)


def detect_traffic_light_color(image: np.ndarray, box: List[float]) -> str:
    """
    Detect the active color of a traffic light using HSV color space analysis.
    
    This function crops the traffic light region, converts it to HSV color space,
    and analyzes pixel distribution to determine which light (red, yellow, or green)
    is currently active.
    
    Args:
        image (np.ndarray): Input image in RGB format
        box (List[float]): Bounding box coordinates [x1, y1, x2, y2]
    
    Returns:
        str: Detected color ('red', 'yellow', 'green', or 'Unknown Color')
    
    Examples:
        >>> color = detect_traffic_light_color(image_array, [100, 50, 150, 200])
        >>> print(color)  # 'red', 'yellow', 'green', or 'Unknown Color'
    """
    try:
        # Extract and validate bounding box coordinates
        x1, y1, x2, y2 = map(int, box)
        
        # Ensure valid coordinates
        if x1 >= x2 or y1 >= y2:
            logger.warning(f"Invalid bounding box coordinates: {box}")
            return 'Unknown Color'
        
        # Crop the traffic light region
        cropped_image = image[y1:y2, x1:x2]
        
        if cropped_image.size == 0:
            logger.warning("Cropped image is empty")
            return 'Unknown Color'
        
        # Convert from RGB to HSV color space
        hsv_image = cv2.cvtColor(cropped_image, cv2.COLOR_RGB2HSV)
        
        # Count pixels for each color
        red_pixels = _count_red_pixels(hsv_image)
        green_pixels = _count_green_pixels(hsv_image)
        yellow_pixels = _count_yellow_pixels(hsv_image)
        
        # Determine the dominant color
        color = _determine_dominant_color(red_pixels, green_pixels, yellow_pixels)
        
        logger.info(f"Detected color: {color} (R:{red_pixels}, G:{green_pixels}, Y:{yellow_pixels})")
        return color
        
    except Exception as e:
        logger.error(f"Error in color detection: {str(e)}")
        return 'Unknown Color'


def _count_red_pixels(hsv_image: np.ndarray) -> int:
    """
    Count red pixels in HSV image.
    Red color wraps around in HSV (0-10 and 170-180 degrees).
    
    Args:
        hsv_image (np.ndarray): Image in HSV color space
    
    Returns:
        int: Number of red pixels detected
    """
    red_config = COLOR_RANGES["red"]
    
    # Create masks for both red ranges
    red_mask1 = cv2.inRange(hsv_image, red_config["lower1"], red_config["upper1"])
    red_mask2 = cv2.inRange(hsv_image, red_config["lower2"], red_config["upper2"])
    
    # Combine both red masks
    red_mask = red_mask1 | red_mask2
    
    return cv2.countNonZero(red_mask)


def _count_green_pixels(hsv_image: np.ndarray) -> int:
    """
    Count green pixels in HSV image.
    
    Args:
        hsv_image (np.ndarray): Image in HSV color space
    
    Returns:
        int: Number of green pixels detected
    """
    green_config = COLOR_RANGES["green"]
    green_mask = cv2.inRange(hsv_image, green_config["lower"], green_config["upper"])
    return cv2.countNonZero(green_mask)


def _count_yellow_pixels(hsv_image: np.ndarray) -> int:
    """
    Count yellow pixels in HSV image.
    
    Args:
        hsv_image (np.ndarray): Image in HSV color space
    
    Returns:
        int: Number of yellow pixels detected
    """
    yellow_config = COLOR_RANGES["yellow"]
    yellow_mask = cv2.inRange(hsv_image, yellow_config["lower"], yellow_config["upper"])
    return cv2.countNonZero(yellow_mask)


def _determine_dominant_color(red_pixels: int, green_pixels: int, yellow_pixels: int) -> str:
    """
    Determine the dominant color based on pixel counts.
    Uses a minimum threshold to filter out noise and false positives.
    
    Args:
        red_pixels (int): Count of red pixels
        green_pixels (int): Count of green pixels
        yellow_pixels (int): Count of yellow pixels
    
    Returns:
        str: Dominant color ('red', 'yellow', 'green', or 'Unknown Color')
    """
    max_pixels = max(red_pixels, green_pixels, yellow_pixels)
    
    # If no significant color detected (below threshold)
    if max_pixels < MIN_PIXEL_THRESHOLD:
        return 'Unknown Color'
    
    # Return the color with maximum pixels (must be significantly higher)
    if max_pixels == red_pixels:
        return 'red'
    elif max_pixels == green_pixels:
        return 'green'
    else:
        return 'yellow'


def validate_color_ranges() -> bool:
    """
    Validate that all color ranges are properly configured.
    
    Returns:
        bool: True if all ranges are valid, False otherwise
    """
    try:
        required_colors = ["red", "green", "yellow"]
        for color in required_colors:
            if color not in COLOR_RANGES:
                logger.error(f"Missing color range configuration for: {color}")
                return False
        return True
    except Exception as e:
        logger.error(f"Error validating color ranges: {str(e)}")
        return False
