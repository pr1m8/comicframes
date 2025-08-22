"""Processing modules for ComicFrames."""

from .pdf_processor import PDFProcessor
from .frame_processor import FrameProcessor
from .interpolation_processor import InterpolationProcessor

__all__ = [
    "PDFProcessor",
    "FrameProcessor", 
    "InterpolationProcessor"
]
