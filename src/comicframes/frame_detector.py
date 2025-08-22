"""Frame detection module for extracting comic panels from images."""

import cv2
import numpy as np
import os
from .utils import sort_contours


def detect_frames(image_path, min_width=75, min_height=100, detection_method="threshold"):
    """
    Detect and extract frames from a comic page image.
    
    Args:
        image_path (str): Path to the comic page image
        min_width (int): Minimum width for valid frames
        min_height (int): Minimum height for valid frames
        detection_method (str): Detection method - "threshold" or "canny"
        
    Returns:
        int: Total number of frames detected
    """
    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not read image from {image_path}")
        return 0
        
    original = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if detection_method == "threshold":
        # Apply a binary threshold to the image
        _, binary = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY_INV)
        contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    else:  # canny method
        # Apply GaussianBlur to reduce noise and improve edge detection
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        # Detect edges using Canny edge detector
        edged = cv2.Canny(blurred, 10, 200)
        
        # Apply morphological operations to close gaps in edges
        kernel = np.ones((5, 5), np.uint8)
        dilation = cv2.dilate(edged, kernel, iterations=1)
        erosion = cv2.erode(dilation, kernel, iterations=1)
        
        contours, hierarchy = cv2.findContours(erosion.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # If no contours are found, return without doing anything
    if not contours or hierarchy is None:
        print("No contours found")
        return 0

    # Sort contours
    sorted_contours, _ = sort_contours(contours, method="top-to-bottom")

    # Filter contours that meet the minimum width and height requirements and are not nested
    valid_contours = []
    for i, contour in enumerate(sorted_contours):
        if hierarchy[0][i][3] == -1:  # Check for no parent contour
            x, y, w, h = cv2.boundingRect(contour)
            if w >= min_width and h >= min_height:
                valid_contours.append(contour)

    # Frame extraction and saving
    base_dir = os.path.dirname(image_path)
    frame_data_dir = os.path.join(base_dir, '..', 'frame_data')
    if not os.path.exists(frame_data_dir):
        os.makedirs(frame_data_dir)

    # Page number extraction from the file name
    page_number = os.path.basename(image_path).split('_')[-1].split('.')[0]

    # Frame count initialization
    frame_count = 0
    total_frame_count = _get_next_total_frame_count(frame_data_dir)

    for contour in valid_contours:
        x, y, w, h = cv2.boundingRect(contour)
        frame = original[y:y + h, x:x + w]
        frame_count += 1
        total_frame_count += 1

        # Frame file name with page, frame order, and total frame number
        frame_file_name = f"page_{page_number}_frame_{frame_count}_total_{total_frame_count}.png"
        frame_file_path = os.path.join(frame_data_dir, frame_file_name)

        cv2.imwrite(frame_file_path, frame)
        print(f"Frame saved as {frame_file_path}")

    return frame_count


def extract_and_save_frames(pages_directory, output_directory, min_width=75, min_height=100):
    """
    Extract frames from all pages in a directory.
    
    Args:
        pages_directory (str): Directory containing comic page images
        output_directory (str): Directory to save extracted frames
        min_width (int): Minimum width for valid frames
        min_height (int): Minimum height for valid frames
        
    Returns:
        int: Total number of frames extracted
    """
    frame_data_path = os.path.join(output_directory, "frame_data")
    if not os.path.exists(frame_data_path):
        os.makedirs(frame_data_path)

    total_frame_count = 0  # Global counter for all frames

    for page_filename in sorted(os.listdir(pages_directory)):
        if not page_filename.endswith('.png'):
            continue  # Skip non-PNG files

        page_path = os.path.join(pages_directory, page_filename)
        image = cv2.imread(page_path)
        
        if image is None:
            print(f"Warning: Could not read {page_path}")
            continue
            
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        sorted_contours = sort_contours(contours)

        page_number = page_filename.split('_')[2].split('.')[0]
        frame_count = 0  # Counter for frames within the current page

        for contour, bbox in sorted_contours:
            x, y, w, h = bbox
            if w < min_width or h < min_height:  # Skip small contours
                continue
                
            frame = image[y:y + h, x:x + w]
            frame_count += 1
            total_frame_count += 1

            frame_filename = f"page_{page_number}_frame_{frame_count}_total_{total_frame_count}.png"
            cv2.imwrite(os.path.join(frame_data_path, frame_filename), frame)
            print(f"Frame saved: {frame_filename}")

    print(f"Total frames saved: {total_frame_count}")
    return total_frame_count


def _get_next_total_frame_count(frame_data_dir):
    """
    Get the next total frame count by checking existing files.
    
    Args:
        frame_data_dir (str): Directory containing frame data
        
    Returns:
        int: Next total frame count
    """
    if not os.path.exists(frame_data_dir):
        return 0
        
    max_total = 0
    for filename in os.listdir(frame_data_dir):
        if filename.startswith("page_") and "_total_" in filename:
            try:
                total_num = int(filename.split("_total_")[1].split(".")[0])
                max_total = max(max_total, total_num)
            except (ValueError, IndexError):
                continue
                
    return max_total
