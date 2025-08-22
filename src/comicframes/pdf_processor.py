"""PDF processing module for converting comic books to images."""

import fitz  # PyMuPDF
import os
from PIL import Image
from .frame_detector import detect_frames


def pdf_to_images(pdf_path, output_base_dir=None, detect_frames_enabled=True):
    """
    Convert PDF comic book to individual page images.
    
    Args:
        pdf_path (str): Path to the PDF file
        output_base_dir (str, optional): Base directory for output. Defaults to Data/Augmented_Data
        detect_frames_enabled (bool): Whether to run frame detection on extracted pages
        
    Returns:
        str: Path to the directory containing extracted images
    """
    if output_base_dir is None:
        # Default to current working directory structure
        output_base_dir = os.path.join(os.getcwd(), 'Data', 'Augmented_Data')
    
    pdf_name = os.path.basename(pdf_path).replace('.pdf', '')
    pdf_dir = os.path.join(output_base_dir, pdf_name)
    
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)
    
    save_dir = os.path.join(pdf_dir, 'raw_image')
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    doc = fitz.open(pdf_path)
    
    try:
        for i, page in enumerate(doc):
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img_path = os.path.join(save_dir, f'comic_page_{i}.png')
            img.save(img_path)
            print(f'Page {i} saved as {img_path}.')
            
            # Perform frame detection on the saved image if enabled
            if detect_frames_enabled:
                detect_frames(img_path)
                
    finally:
        doc.close()
    
    return save_dir
