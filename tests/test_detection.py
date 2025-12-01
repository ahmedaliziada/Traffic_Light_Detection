"""
Unit tests for traffic light detection utilities.
"""

import unittest
import numpy as np
from src.utils.detection import (
    detect_traffic_light_color,
    _count_red_pixels,
    _count_green_pixels,
    _count_yellow_pixels,
    _determine_dominant_color
)


class TestColorDetection(unittest.TestCase):
    """Test cases for color detection functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a simple test image (100x100 pixels)
        self.test_image = np.zeros((100, 100, 3), dtype=np.uint8)
        self.test_box = [0, 0, 100, 100]
    
    def test_determine_dominant_color_red(self):
        """Test that red is correctly identified as dominant."""
        result = _determine_dominant_color(100, 50, 30)
        self.assertEqual(result, 'red')
    
    def test_determine_dominant_color_green(self):
        """Test that green is correctly identified as dominant."""
        result = _determine_dominant_color(30, 100, 50)
        self.assertEqual(result, 'green')
    
    def test_determine_dominant_color_yellow(self):
        """Test that yellow is correctly identified as dominant."""
        result = _determine_dominant_color(30, 50, 100)
        self.assertEqual(result, 'yellow')
    
    def test_determine_dominant_color_no_pixels(self):
        """Test that 'Unknown Color' is returned when no pixels match."""
        result = _determine_dominant_color(0, 0, 0)
        self.assertEqual(result, 'Unknown Color')
    
    def test_invalid_bounding_box(self):
        """Test handling of invalid bounding box coordinates."""
        invalid_box = [100, 100, 0, 0]  # x1 > x2, y1 > y2
        result = detect_traffic_light_color(self.test_image, invalid_box)
        self.assertEqual(result, 'Unknown Color')


class TestImageProcessing(unittest.TestCase):
    """Test cases for image processing functionality."""
    
    def test_detection_result_to_dict(self):
        """Test DetectionResult conversion to dictionary."""
        from src.utils.image_processing import DetectionResult
        
        result = DetectionResult(
            box=[10, 20, 30, 40],
            confidence=0.95,
            color='red',
            index=1
        )
        
        result_dict = result.to_dict()
        
        self.assertEqual(result_dict['index'], 1)
        self.assertEqual(result_dict['color'], 'red')
        self.assertEqual(result_dict['confidence'], 0.95)
        self.assertEqual(result_dict['box'], [10, 20, 30, 40])


if __name__ == '__main__':
    unittest.main()
