"""
Basic usage examples for the comicframes package.
"""

import os
from comicframes import pdf_to_images, extract_and_save_frames


def example_pdf_processing():
    """Example of converting a PDF to images with frame detection."""
    pdf_path = "data_samples/Data/Train_Data/watchmen-ch.-1.pdf"
    
    if os.path.exists(pdf_path):
        print("Converting PDF to images...")
        output_dir = pdf_to_images(pdf_path)
        print(f"Images saved to: {output_dir}")
    else:
        print(f"PDF file not found: {pdf_path}")


def example_frame_extraction():
    """Example of extracting frames from existing page images."""
    pages_dir = "data_samples/Data/Augmented_Data/watchmen-ch.-1/raw_image"
    output_dir = "data_samples/Data/Augmented_Data/watchmen-ch.-1"
    
    if os.path.exists(pages_dir):
        print("Extracting frames from images...")
        total_frames = extract_and_save_frames(pages_dir, output_dir)
        print(f"Extracted {total_frames} frames")
    else:
        print(f"Pages directory not found: {pages_dir}")


if __name__ == "__main__":
    print("ComicFrames Package Usage Examples")
    print("=" * 40)
    
    # Example 1: PDF processing
    example_pdf_processing()
    
    print()
    
    # Example 2: Frame extraction
    example_frame_extraction()
