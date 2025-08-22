"""Frame interpolation processing with the new architecture."""

from typing import List, Optional
from ..core.base_processor import BaseProcessor
from ..core.data_structures import Frame, InterpolationFrame
from ..models import ModelFactory
from ..config import ModelType


class InterpolationProcessor(BaseProcessor):
    """Frame interpolation processor using the new architecture."""
    
    def __init__(self, model_name: Optional[str] = None, cache_enabled: bool = True):
        """
        Initialize interpolation processor.
        
        Args:
            model_name: Name of the interpolation model to use
            cache_enabled: Whether to enable caching
        """
        super().__init__("interpolation_processor", cache_enabled)
        
        # Load interpolation model
        if model_name is None:
            self.model = ModelFactory.create_default_model(ModelType.FRAME_INTERPOLATION)
        else:
            self.model = ModelFactory.create_model(model_name)
    
    def _process(
        self, 
        frame_pair: tuple[Frame, Frame], 
        num_interpolations: int = 1
    ) -> List[InterpolationFrame]:
        """
        Process frame pair to generate interpolated frames.
        
        Args:
            frame_pair: Tuple of (frame1, frame2) to interpolate between
            num_interpolations: Number of frames to interpolate
            
        Returns:
            List of interpolated frames
        """
        frame1, frame2 = frame_pair
        
        # Use the model to generate interpolated frames
        interpolated_frames = self.model.predict(frame1, frame2, num_interpolations)
        
        return interpolated_frames
