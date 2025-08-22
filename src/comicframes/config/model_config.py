"""Model configuration and registry."""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, Optional
from enum import Enum


class ModelType(Enum):
    """Available model types."""
    FRAME_DETECTION = "frame_detection"
    FRAME_INTERPOLATION = "frame_interpolation"
    OBJECT_DETECTION = "object_detection"
    SPEECH_BUBBLE_DETECTION = "speech_bubble_detection"


@dataclass
class ModelConfig:
    """Configuration for a specific model."""
    
    name: str
    model_type: ModelType
    model_path: Optional[Path] = None
    download_url: Optional[str] = None
    config_path: Optional[Path] = None
    
    # Model parameters
    input_size: tuple = (640, 640)
    batch_size: int = 1
    device: str = "auto"
    
    # Model-specific settings
    settings: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.settings is None:
            self.settings = {}


class ModelRegistry:
    """Registry of available models."""
    
    def __init__(self):
        self._models: Dict[str, ModelConfig] = {}
        self._setup_default_models()
    
    def _setup_default_models(self):
        """Set up default model configurations."""
        # RIFE frame interpolation
        self.register_model(ModelConfig(
            name="rife_v4.6",
            model_type=ModelType.FRAME_INTERPOLATION,
            download_url="https://github.com/megvii-research/ECCV2022-RIFE/releases/download/v4.6/flownet.pkl",
            settings={
                "scale": 1.0,
                "fps_multiplier": 2,
                "uhd": False
            }
        ))
        
        # Google Frame Interpolation
        self.register_model(ModelConfig(
            name="film_net",
            model_type=ModelType.FRAME_INTERPOLATION,
            settings={
                "model_path": "google/frame-interpolation",
                "model_type": "film_net"
            }
        ))
        
        # YOLO for object detection
        self.register_model(ModelConfig(
            name="yolov3",
            model_type=ModelType.OBJECT_DETECTION,
            input_size=(416, 416),
            settings={
                "confidence_threshold": 0.5,
                "nms_threshold": 0.4
            }
        ))
        
        # Basic frame detection (OpenCV-based)
        self.register_model(ModelConfig(
            name="opencv_contours",
            model_type=ModelType.FRAME_DETECTION,
            settings={
                "method": "threshold",
                "min_area": 1000,
                "max_area": 1000000
            }
        ))
    
    def register_model(self, config: ModelConfig) -> None:
        """Register a new model configuration."""
        self._models[config.name] = config
    
    def get_model(self, name: str) -> Optional[ModelConfig]:
        """Get a model configuration by name."""
        return self._models.get(name)
    
    def list_models(self, model_type: Optional[ModelType] = None) -> Dict[str, ModelConfig]:
        """List all models, optionally filtered by type."""
        if model_type is None:
            return self._models.copy()
        return {
            name: config for name, config in self._models.items()
            if config.model_type == model_type
        }
    
    def get_default_model(self, model_type: ModelType) -> Optional[ModelConfig]:
        """Get the default model for a given type."""
        defaults = {
            ModelType.FRAME_DETECTION: "opencv_contours",
            ModelType.FRAME_INTERPOLATION: "rife_v4.6",
            ModelType.OBJECT_DETECTION: "yolov3",
        }
        
        default_name = defaults.get(model_type)
        if default_name:
            return self.get_model(default_name)
        return None


# Global model registry
_model_registry: Optional[ModelRegistry] = None


def get_model_registry() -> ModelRegistry:
    """Get the global model registry."""
    global _model_registry
    if _model_registry is None:
        _model_registry = ModelRegistry()
    return _model_registry
