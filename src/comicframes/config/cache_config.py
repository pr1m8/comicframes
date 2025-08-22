"""Cache configuration and management."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class CacheConfig:
    """Configuration for caching system."""
    
    cache_dir: Path
    enable_frame_cache: bool = True
    enable_model_cache: bool = True
    enable_processing_cache: bool = True
    
    # Cache size limits (in MB)
    max_frame_cache_size: int = 500
    max_model_cache_size: int = 2000
    max_processing_cache_size: int = 1000
    
    # TTL settings (in seconds)
    frame_cache_ttl: int = 3600 * 24  # 24 hours
    model_cache_ttl: int = 3600 * 24 * 7  # 1 week
    processing_cache_ttl: int = 3600 * 6  # 6 hours
    
    # Cleanup settings
    cleanup_interval: int = 3600  # 1 hour
    cleanup_threshold: float = 0.8  # Clean when 80% full
    
    def get_frame_cache_dir(self) -> Path:
        """Get the frame cache directory."""
        cache_dir = self.cache_dir / "frames"
        cache_dir.mkdir(parents=True, exist_ok=True)
        return cache_dir
    
    def get_model_cache_dir(self) -> Path:
        """Get the model cache directory."""
        cache_dir = self.cache_dir / "models"
        cache_dir.mkdir(parents=True, exist_ok=True)
        return cache_dir
    
    def get_processing_cache_dir(self) -> Path:
        """Get the processing cache directory."""
        cache_dir = self.cache_dir / "processing"
        cache_dir.mkdir(parents=True, exist_ok=True)
        return cache_dir
