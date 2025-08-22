"""PDF processing with the new architecture."""

import fitz
from pathlib import Path
from typing import List, Optional
from PIL import Image

from ..core.base_processor import BaseProcessor
from ..core.data_structures import ComicPage, ProcessingResult
from ..config import get_settings


class PDFProcessor(BaseProcessor):
    """PDF processor using the new architecture."""
    
    def __init__(self, cache_enabled: bool = True):
        """Initialize PDF processor."""
        super().__init__("pdf_processor", cache_enabled)
        self.settings = get_settings()
    
    def _process(self, pdf_path: str, output_base_dir: Optional[str] = None) -> List[ComicPage]:
        """
        Process PDF to extract pages.
        
        Args:
            pdf_path: Path to PDF file
            output_base_dir: Base directory for output
            
        Returns:
            List of ComicPage objects
        """
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        if output_base_dir is None:
            output_base_dir = self.settings.augmented_data_dir
        else:
            output_base_dir = Path(output_base_dir)
        
        # Create output directory structure
        pdf_name = pdf_path.stem
        pdf_dir = output_base_dir / pdf_name
        pdf_dir.mkdir(parents=True, exist_ok=True)
        
        raw_image_dir = pdf_dir / "raw_image"
        raw_image_dir.mkdir(exist_ok=True)
        
        pages = []
        doc = fitz.open(str(pdf_path))
        
        try:
            for page_num, page in enumerate(doc):
                # Extract page image
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                
                # Save image
                img_path = raw_image_dir / f'comic_page_{page_num}.png'
                img.save(img_path)
                
                # Create ComicPage object
                comic_page = ComicPage(
                    page_number=page_num,
                    image_path=img_path,
                    width=pix.width,
                    height=pix.height,
                    source_pdf=pdf_path
                )
                
                pages.append(comic_page)
                
        finally:
            doc.close()
        
        return pages
    
    def _generate_cache_key(self, pdf_path: str, output_base_dir: Optional[str] = None) -> Optional[str]:
        """Generate cache key for PDF processing."""
        import hashlib
        
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            return None
        
        # Include file modification time in cache key
        mtime = pdf_path.stat().st_mtime
        key_data = f"pdf:{pdf_path}:{output_base_dir}:{mtime}"
        return hashlib.md5(key_data.encode()).hexdigest()
