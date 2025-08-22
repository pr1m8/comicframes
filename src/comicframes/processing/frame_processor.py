"""Frame detection and processing with the new architecture."""

import cv2
from pathlib import Path
from typing import List, Optional, Union

from ..core.base_processor import BaseProcessor
from ..core.data_structures import ComicPage, Frame
from ..models import ModelFactory
from ..config import ModelType, get_settings


class FrameProcessor(BaseProcessor):
    """Frame detection processor using the new architecture."""
    
    def __init__(self, model_name: Optional[str] = None, cache_enabled: bool = True):
        """
        Initialize frame processor.
        
        Args:
            model_name: Name of the detection model to use
            cache_enabled: Whether to enable caching
        """
        super().__init__("frame_processor", cache_enabled)
        self.settings = get_settings()
        
        # Load detection model
        if model_name is None:
            self.model = ModelFactory.create_default_model(ModelType.FRAME_DETECTION)
        else:
            self.model = ModelFactory.create_model(model_name)
    
    def _process(
        self, 
        input_data: Union[str, Path, ComicPage], 
        min_width: Optional[int] = None,
        min_height: Optional[int] = None,
        save_frames: bool = True
    ) -> ComicPage:
        """
        Process input to detect frames.
        
        Args:
            input_data: Image path, ComicPage, or image array
            min_width: Minimum frame width
            min_height: Minimum frame height
            save_frames: Whether to save detected frames to files
            
        Returns:
            ComicPage with detected frames
        """
        # Set defaults
        if min_width is None:
            min_width = self.settings.min_frame_width
        if min_height is None:
            min_height = self.settings.min_frame_height
        
        # Handle different input types
        if isinstance(input_data, (str, Path)):
            # Input is image path
            image_path = Path(input_data)
            if not image_path.exists():
                raise FileNotFoundError(f"Image not found: {image_path}")
            
            # Extract page number from filename
            try:
                page_num = int(image_path.stem.split('_')[-1])
            except (ValueError, IndexError):
                page_num = 0
            
            comic_page = ComicPage(
                page_number=page_num,
                image_path=image_path
            )
            
        elif isinstance(input_data, ComicPage):
            comic_page = input_data
        else:
            raise ValueError(f"Unsupported input type: {type(input_data)}")
        
        # Load image if not already loaded
        image = comic_page.load_image()
        if image is None:
            raise ValueError(f"Could not load image from {comic_page.image_path}")
        
        # Detect frames using the model
        frames = self.model.predict(image, min_width=min_width, min_height=min_height)
        
        # Update frame metadata
        total_frame_count = self._get_next_total_frame_count(comic_page)
        
        for i, frame in enumerate(frames):
            frame.page_number = comic_page.page_number
            frame.frame_number = i + 1
            frame.total_frame_number = total_frame_count + i + 1
            comic_page.add_frame(frame)
        
        # Save frames if requested
        if save_frames and frames:
            self._save_frames(comic_page)
        
        return comic_page
    
    def _get_next_total_frame_count(self, comic_page: ComicPage) -> int:
        """Get the next total frame count by checking existing files."""
        if not comic_page.image_path:
            return 0
        
        # Look for frame_data directory
        base_dir = comic_page.image_path.parent.parent
        frame_data_dir = base_dir / "frame_data"
        
        if not frame_data_dir.exists():
            return 0
        
        max_total = 0
        for frame_file in frame_data_dir.glob("page_*_frame_*_total_*.png"):
            try:
                total_num = int(frame_file.stem.split("_total_")[1])
                max_total = max(max_total, total_num)
            except (ValueError, IndexError):
                continue
        
        return max_total
    
    def _save_frames(self, comic_page: ComicPage) -> None:
        """Save detected frames to files."""
        if not comic_page.image_path or not comic_page.frames:
            return
        
        # Create frame_data directory
        base_dir = comic_page.image_path.parent.parent
        frame_data_dir = base_dir / "frame_data"
        frame_data_dir.mkdir(exist_ok=True)
        
        # Save each frame
        for frame in comic_page.frames:
            if frame.image is not None:
                filename = frame.get_file_name()
                frame_path = frame_data_dir / filename
                cv2.imwrite(str(frame_path), frame.image)
    
    def process_directory(
        self, 
        images_dir: Union[str, Path], 
        **kwargs
    ) -> List[ComicPage]:
        """
        Process all images in a directory.
        
        Args:
            images_dir: Directory containing comic page images
            **kwargs: Arguments passed to _process
            
        Returns:
            List of processed ComicPages
        """
        images_dir = Path(images_dir)
        if not images_dir.exists():
            raise FileNotFoundError(f"Directory not found: {images_dir}")
        
        pages = []
        
        # Process all PNG images in the directory
        for image_file in sorted(images_dir.glob("*.png")):
            try:
                result = self.process(image_file, **kwargs)
                if result.success:
                    pages.append(result.data)
                else:
                    print(f"Failed to process {image_file}: {result.message}")
            except Exception as e:
                print(f"Error processing {image_file}: {str(e)}")
        
        return pages
