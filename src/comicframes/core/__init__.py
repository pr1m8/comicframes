"""Core classes and interfaces for ComicFrames."""

from .base_processor import BaseProcessor
from .base_model import BaseModel
from .pipeline import ProcessingPipeline
from .data_structures import Frame, ComicPage, ProcessingResult

__all__ = [
    "BaseProcessor", 
    "BaseModel", 
    "ProcessingPipeline", 
    "Frame", 
    "ComicPage", 
    "ProcessingResult"
]
