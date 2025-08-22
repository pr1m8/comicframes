"""Core data structures for ComicFrames."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple, Dict, Any, Union
import numpy as np


@dataclass
class BoundingBox:
    """Represents a bounding box with coordinates."""
    x: int
    y: int
    width: int
    height: int
    confidence: float = 1.0
    
    @property
    def x2(self) -> int:
        """Right edge x-coordinate."""
        return self.x + self.width
    
    @property
    def y2(self) -> int:
        """Bottom edge y-coordinate."""
        return self.y + self.height
    
    @property
    def center(self) -> Tuple[int, int]:
        """Center point of the bounding box."""
        return (self.x + self.width // 2, self.y + self.height // 2)
    
    @property
    def area(self) -> int:
        """Area of the bounding box."""
        return self.width * self.height
    
    def to_xyxy(self) -> Tuple[int, int, int, int]:
        """Convert to (x1, y1, x2, y2) format."""
        return (self.x, self.y, self.x2, self.y2)
    
    def to_xywh(self) -> Tuple[int, int, int, int]:
        """Convert to (x, y, width, height) format."""
        return (self.x, self.y, self.width, self.height)


@dataclass
class Frame:
    """Represents a comic frame/panel."""
    
    bbox: BoundingBox
    image: Optional[np.ndarray] = None
    page_number: int = 0
    frame_number: int = 0
    total_frame_number: int = 0
    
    # Detection metadata
    detection_method: str = "unknown"
    confidence: float = 1.0
    
    # Content analysis
    has_text: bool = False
    has_speech_bubbles: bool = False
    character_count: int = 0
    
    # Processing metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def save_to_file(self, file_path: Union[str, Path]) -> None:
        """Save frame image to file."""
        if self.image is not None:
            import cv2
            cv2.imwrite(str(file_path), self.image)
    
    def get_file_name(self, prefix: str = "frame") -> str:
        """Generate a standard filename for this frame."""
        return f"{prefix}_page_{self.page_number}_frame_{self.frame_number}_total_{self.total_frame_number}.png"


@dataclass
class ComicPage:
    """Represents a comic book page."""
    
    page_number: int
    image_path: Optional[Path] = None
    image: Optional[np.ndarray] = None
    frames: List[Frame] = field(default_factory=list)
    
    # Page metadata
    width: int = 0
    height: int = 0
    source_pdf: Optional[Path] = None
    
    # Processing metadata
    processing_metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_frame(self, frame: Frame) -> None:
        """Add a frame to this page."""
        frame.page_number = self.page_number
        self.frames.append(frame)
    
    def get_frame_count(self) -> int:
        """Get the number of frames on this page."""
        return len(self.frames)
    
    def load_image(self) -> Optional[np.ndarray]:
        """Load the page image if not already loaded."""
        if self.image is not None:
            return self.image
        
        if self.image_path and self.image_path.exists():
            import cv2
            self.image = cv2.imread(str(self.image_path))
            if self.image is not None:
                self.height, self.width = self.image.shape[:2]
            return self.image
        
        return None


@dataclass
class ProcessingResult:
    """Result of a processing operation."""
    
    success: bool
    message: str = ""
    data: Any = None
    processing_time: float = 0.0
    cache_hit: bool = False
    
    # Error information
    error: Optional[Exception] = None
    
    # Metrics
    metrics: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def success_result(cls, data: Any = None, message: str = "Success", **kwargs) -> "ProcessingResult":
        """Create a successful result."""
        return cls(success=True, data=data, message=message, **kwargs)
    
    @classmethod
    def error_result(cls, error: Exception, message: str = "", **kwargs) -> "ProcessingResult":
        """Create an error result."""
        return cls(
            success=False, 
            error=error, 
            message=message or str(error), 
            **kwargs
        )


@dataclass
class ModelLoadResult:
    """Result of model loading operation."""
    
    success: bool
    model: Optional[Any] = None
    model_path: Optional[Path] = None
    load_time: float = 0.0
    cached: bool = False
    error: Optional[Exception] = None
    message: str = ""


@dataclass
class InterpolationFrame:
    """Represents an interpolated frame between two source frames."""
    
    source_frame_1: Frame
    source_frame_2: Frame
    interpolated_image: np.ndarray
    interpolation_factor: float  # 0.0 to 1.0
    
    # Interpolation metadata
    method: str = "unknown"
    confidence: float = 1.0
    processing_time: float = 0.0
