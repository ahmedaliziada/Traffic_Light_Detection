"""
Image processing utilities for detection results.
"""

import numpy as np
from typing import List, Dict, Tuple
import logging

from config.config import TARGET_CLASS, CONFIDENCE_THRESHOLD
from .detection import detect_traffic_light_color

logger = logging.getLogger(__name__)


class DetectionResult:
    """Class to store detection results for a single traffic light."""
    
    def __init__(self, box: List[float], confidence: float, color: str, index: int):
        """
        Initialize detection result.
        
        Args:
            box (List[float]): Bounding box coordinates [x1, y1, x2, y2]
            confidence (float): Detection confidence score
            color (str): Detected traffic light color
            index (int): Traffic light index in the image
        """
        self.box = box
        self.confidence = confidence
        self.color = color
        self.index = index
    
    def to_dict(self) -> dict:
        """Convert result to dictionary format."""
        return {
            'index': self.index,
            'color': self.color,
            'confidence': self.confidence,
            'box': self.box
        }


def process_detection_results(detection_output, image: np.ndarray) -> List[DetectionResult]:
    """
    Process YOLO detection results and extract traffic light information.
    
    Args:
        detection_output: YOLO model output containing detection results
        image (np.ndarray): Input image for color analysis
    
    Returns:
        List[DetectionResult]: List of processed detection results
    """
    results = []
    
    try:
        # Extract bounding boxes from YOLO output
        boxes = detection_output.xyxy[0].numpy()
        
        traffic_light_count = 0
        
        for box in boxes:
            # Extract detection information
            label = detection_output.names[int(box[5])]
            confidence = float(box[4])
            
            # Filter for traffic lights with sufficient confidence
            if label == TARGET_CLASS and confidence >= CONFIDENCE_THRESHOLD:
                traffic_light_count += 1
                
                # Detect the color of the traffic light
                color = detect_traffic_light_color(image, box[:4])
                
                # Create detection result object
                result = DetectionResult(
                    box=box[:4].tolist(),
                    confidence=confidence,
                    color=color,
                    index=traffic_light_count
                )
                
                results.append(result)
                
                logger.info(f"Traffic Light #{traffic_light_count}: {color} (confidence: {confidence:.2%})")
        
        logger.info(f"Total traffic lights detected: {len(results)}")
        
    except Exception as e:
        logger.error(f"Error processing detection results: {str(e)}")
    
    return results


def get_detection_summary(results: List[DetectionResult]) -> Dict[str, int]:
    """
    Generate summary statistics from detection results.
    
    Args:
        results (List[DetectionResult]): List of detection results
    
    Returns:
        Dict[str, int]: Summary containing counts for each color and total
    """
    summary = {
        'total': len(results),
        'red': 0,
        'yellow': 0,
        'green': 0,
        'unknown': 0
    }
    
    for result in results:
        color = result.color.lower()
        if color in ['red', 'yellow', 'green']:
            summary[color] += 1
        else:
            summary['unknown'] += 1
    
    return summary


def filter_results_by_color(results: List[DetectionResult], color: str) -> List[DetectionResult]:
    """
    Filter detection results by specific color.
    
    Args:
        results (List[DetectionResult]): List of all detection results
        color (str): Color to filter by ('red', 'yellow', or 'green')
    
    Returns:
        List[DetectionResult]: Filtered results
    """
    return [r for r in results if r.color.lower() == color.lower()]


def get_highest_confidence_detection(results: List[DetectionResult]) -> DetectionResult:
    """
    Get the detection with the highest confidence score.
    
    Args:
        results (List[DetectionResult]): List of detection results
    
    Returns:
        DetectionResult: Detection with highest confidence, or None if empty
    """
    if not results:
        return None
    
    return max(results, key=lambda r: r.confidence)
