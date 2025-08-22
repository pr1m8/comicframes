"""
ComicFrames - A Python package for comic book frame detection and processing.

This package provides tools for:
- Converting PDF comic books to images
- Detecting and extracting frames from comic pages
- Processing comic book layouts
- Frame interpolation for animations
- Advanced caching and model management
"""

# Legacy imports for backward compatibility
from .pdf_processor import pdf_to_images
from .frame_detector import detect_frames, extract_and_save_frames
from .utils import sort_contours

# New structured imports
from .config import Settings, get_settings
from .config.settings import set_settings
from .cache import CacheManager, get_cache_manager
from .core import Frame, ComicPage, ProcessingResult
from .models import ModelFactory

__version__ = "0.1.0"
__author__ = "ComicFrames Project"

# Backward compatibility
__all__ = [
    "pdf_to_images",
    "detect_frames", 
    "extract_and_save_frames",
    "sort_contours",
    # New exports
    "Settings",
    "get_settings",
    "set_settings",
    "CacheManager", 
    "get_cache_manager",
    "Frame",
    "ComicPage",
    "ProcessingResult",
    "ModelFactory"
]
