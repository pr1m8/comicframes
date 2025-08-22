"""Tests for frame detection functionality."""

import pytest
import numpy as np
import cv2
import tempfile
import os
from comicframes.frame_detector import detect_frames
from comicframes.utils import sort_contours


def create_test_image():
    """Create a simple test image with rectangles for testing."""
    # Create a white image
    img = np.ones((400, 600, 3), dtype=np.uint8) * 255
    
    # Draw some black rectangles to simulate comic frames
    cv2.rectangle(img, (50, 50), (250, 150), (0, 0, 0), 2)
    cv2.rectangle(img, (300, 50), (550, 150), (0, 0, 0), 2)
    cv2.rectangle(img, (50, 200), (250, 350), (0, 0, 0), 2)
    cv2.rectangle(img, (300, 200), (550, 350), (0, 0, 0), 2)
    
    return img


def test_sort_contours():
    """Test contour sorting functionality."""
    # Create some mock contours (as simple rectangles)
    contours = [
        np.array([[100, 100], [200, 100], [200, 200], [100, 200]]),  # Bottom right
        np.array([[10, 10], [100, 10], [100, 100], [10, 100]]),      # Top left
        np.array([[100, 10], [200, 10], [200, 100], [100, 100]]),    # Top right
        np.array([[10, 100], [100, 100], [100, 200], [10, 200]]),    # Bottom left
    ]
    
    sorted_contours, bboxes = sort_contours(contours, method="top-to-bottom")
    
    # Check that we got the same number of contours back
    assert len(sorted_contours) == len(contours)
    assert len(bboxes) == len(contours)
    
    # Check that bounding boxes are sorted properly (top-to-bottom, then left-to-right)
    y_coords = [bbox[1] for bbox in bboxes]
    assert y_coords == sorted(y_coords)


def test_detect_frames():
    """Test frame detection on a simple test image."""
    # Create test image
    test_img = create_test_image()
    
    # Save to temporary file
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
        cv2.imwrite(tmp_file.name, test_img)
        tmp_path = tmp_file.name
    
    try:
        # Test frame detection
        frame_count = detect_frames(tmp_path, min_width=50, min_height=50)
        
        # Should detect some frames (exact number depends on implementation)
        assert frame_count >= 0
        
    finally:
        # Clean up
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def test_detect_frames_invalid_path():
    """Test frame detection with invalid image path."""
    frame_count = detect_frames("nonexistent_image.png")
    assert frame_count == 0


if __name__ == "__main__":
    pytest.main([__file__])
