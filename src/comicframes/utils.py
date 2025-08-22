"""Utility functions for comic processing."""

import cv2


def sort_contours(contours, method="top-to-bottom"):
    """
    Sort contours based on the specified method.
    
    Args:
        contours: List of contours to sort
        method (str): Sorting method - "top-to-bottom", "left-to-right", etc.
        
    Returns:
        tuple: (sorted_contours, bounding_boxes)
    """
    # Extract the bounding boxes
    bounding_boxes = [cv2.boundingRect(c) for c in contours]
    
    if method == "top-to-bottom":
        # Sort by y-coordinate (top to bottom), then by x-coordinate (left to right)
        sorted_pairs = sorted(zip(contours, bounding_boxes), key=lambda b: (b[1][1], b[1][0]))
    elif method == "left-to-right":
        # Sort by x-coordinate (left to right), then by y-coordinate (top to bottom)
        sorted_pairs = sorted(zip(contours, bounding_boxes), key=lambda b: (b[1][0], b[1][1]))
    else:
        # Default to top-to-bottom
        sorted_pairs = sorted(zip(contours, bounding_boxes), key=lambda b: (b[1][1], b[1][0]))
    
    # Separate the sorted contours and bounding boxes
    sorted_contours = [pair[0] for pair in sorted_pairs]
    sorted_bounding_boxes = [pair[1] for pair in sorted_pairs]
    
    return sorted_contours, sorted_bounding_boxes
