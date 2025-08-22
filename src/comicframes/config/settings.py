"""Global settings and configuration management."""

import os
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field


@dataclass
class Settings:
    """Global settings for ComicFrames."""
    
    # Paths
    project_root: Path = field(default_factory=lambda: Path.cwd())
    data_dir: Path = field(default_factory=lambda: Path.cwd() / "Data")
    cache_dir: Path = field(default_factory=lambda: Path.cwd() / ".cache")
    models_dir: Path = field(default_factory=lambda: Path.cwd() / "models")
    
    # Data processing
    augmented_data_dir: Optional[Path] = None
    train_data_dir: Optional[Path] = None
    output_dir: Optional[Path] = None
    
    # Frame detection settings
    min_frame_width: int = 75
    min_frame_height: int = 100
    detection_method: str = "threshold"  # "threshold" or "canny"
    
    # Caching
    enable_cache: bool = True
    cache_ttl: int = 3600  # 1 hour
    max_cache_size: int = 1000  # MB
    
    # Model settings
    device: str = "auto"  # "auto", "cpu", "cuda", "mps"
    model_download_timeout: int = 300  # 5 minutes
    
    # Logging
    log_level: str = "INFO"
    log_file: Optional[Path] = None
    
    def __post_init__(self):
        """Set up derived paths after initialization."""
        if self.augmented_data_dir is None:
            self.augmented_data_dir = self.data_dir / "Augmented_Data"
        if self.train_data_dir is None:
            self.train_data_dir = self.data_dir / "Train_Data"
        if self.output_dir is None:
            self.output_dir = self.project_root / "output"
            
        # Ensure directories exist
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.models_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def from_env(cls) -> "Settings":
        """Create settings from environment variables."""
        return cls(
            project_root=Path(os.getenv("COMICFRAMES_PROJECT_ROOT", Path.cwd())),
            cache_dir=Path(os.getenv("COMICFRAMES_CACHE_DIR", Path.cwd() / ".cache")),
            models_dir=Path(os.getenv("COMICFRAMES_MODELS_DIR", Path.cwd() / "models")),
            min_frame_width=int(os.getenv("COMICFRAMES_MIN_WIDTH", "75")),
            min_frame_height=int(os.getenv("COMICFRAMES_MIN_HEIGHT", "100")),
            enable_cache=os.getenv("COMICFRAMES_ENABLE_CACHE", "true").lower() == "true",
            device=os.getenv("COMICFRAMES_DEVICE", "auto"),
            log_level=os.getenv("COMICFRAMES_LOG_LEVEL", "INFO"),
        )


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get the global settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings.from_env()
    return _settings


def set_settings(settings: Settings) -> None:
    """Set the global settings instance."""
    global _settings
    _settings = settings
