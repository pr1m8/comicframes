"""Tests for utility functions."""

import pytest
import numpy as np
from comicframes.utils import sort_contours


def test_sort_contours_top_to_bottom():
    """Test sorting contours from top to bottom."""
    # Create mock contours at different positions
    contours = [
        np.array([[0, 100], [50, 100], [50, 150], [0, 150]]),  # Bottom
        np.array([[0, 0], [50, 0], [50, 50], [0, 50]]),        # Top
        np.array([[0, 50], [50, 50], [50, 100], [0, 100]]),    # Middle
    ]
    
    sorted_contours, bboxes = sort_contours(contours, method="top-to-bottom")
    
    # Check that y-coordinates are in ascending order
    y_coords = [bbox[1] for bbox in bboxes]
    assert y_coords == [0, 50, 100]


def test_sort_contours_left_to_right():
    """Test sorting contours from left to right."""
    # Create mock contours at different positions
    contours = [
        np.array([[100, 0], [150, 0], [150, 50], [100, 50]]),  # Right
        np.array([[0, 0], [50, 0], [50, 50], [0, 50]]),        # Left
        np.array([[50, 0], [100, 0], [100, 50], [50, 50]]),    # Middle
    ]
    
    sorted_contours, bboxes = sort_contours(contours, method="left-to-right")
    
    # Check that x-coordinates are in ascending order
    x_coords = [bbox[0] for bbox in bboxes]
    assert x_coords == [0, 50, 100]


def test_sort_contours_empty_list():
    """Test sorting with empty contour list."""
    sorted_contours, bboxes = sort_contours([], method="top-to-bottom")
    assert sorted_contours == []
    assert bboxes == []


if __name__ == "__main__":
    pytest.main([__file__])
