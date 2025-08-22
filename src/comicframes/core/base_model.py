"""Base model class for all ML models."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional, Dict
import time
import logging

from .data_structures import ModelLoadResult
from ..config import ModelConfig, get_model_registry
from ..cache import get_cache_manager


logger = logging.getLogger(__name__)


class BaseModel(ABC):
    """Base class for all ML models."""
    
    def __init__(self, model_name: str, config: Optional[ModelConfig] = None):
        """
        Initialize model.
        
        Args:
            model_name: Name of the model
            config: Model configuration (will be loaded from registry if not provided)
        """
        self.model_name = model_name
        self.config = config or get_model_registry().get_model(model_name)
        self.model = None
        self.is_loaded = False
        self.load_time = 0.0
        self.cache_manager = get_cache_manager()
        
        if self.config is None:
            raise ValueError(f"Model configuration not found for: {model_name}")
    
    @abstractmethod
    def _load_model(self) -> Any:
        """
        Load the actual model.
        
        This method should be implemented by subclasses.
        """
        pass
    
    @abstractmethod
    def _predict(self, *args, **kwargs) -> Any:
        """
        Perform model prediction.
        
        This method should be implemented by subclasses.
        """
        pass
    
    def load(self, force_reload: bool = False) -> ModelLoadResult:
        """
        Load the model with caching and error handling.
        
        Args:
            force_reload: Force reload even if already loaded
            
        Returns:
            ModelLoadResult with load status and model
        """
        if self.is_loaded and not force_reload:
            return ModelLoadResult(
                success=True,
                model=self.model,
                model_path=self.config.model_path,
                cached=True,
                message="Model already loaded"
            )
        
        start_time = time.time()
        
        try:
            # Check if model is cached
            cache_key = f"model:{self.model_name}"
            cached_model = self.cache_manager.get_model_data(cache_key)
            
            if cached_model is not None and not force_reload:
                self.model = cached_model
                self.is_loaded = True
                load_time = time.time() - start_time
                
                logger.info(f"Loaded {self.model_name} from cache")
                return ModelLoadResult(
                    success=True,
                    model=self.model,
                    model_path=self.config.model_path,
                    load_time=load_time,
                    cached=True,
                    message=f"Model {self.model_name} loaded from cache"
                )
            
            # Download model if needed
            if self.config.model_path and not self.config.model_path.exists():
                if self.config.download_url:
                    self._download_model()
                else:
                    raise FileNotFoundError(f"Model file not found: {self.config.model_path}")
            
            # Load the model
            logger.info(f"Loading {self.model_name}")
            self.model = self._load_model()
            self.is_loaded = True
            self.load_time = time.time() - start_time
            
            # Cache the loaded model
            self.cache_manager.set_model_data(cache_key, self.model)
            
            logger.info(f"Successfully loaded {self.model_name} in {self.load_time:.2f}s")
            return ModelLoadResult(
                success=True,
                model=self.model,
                model_path=self.config.model_path,
                load_time=self.load_time,
                cached=False,
                message=f"Model {self.model_name} loaded successfully"
            )
            
        except Exception as e:
            load_time = time.time() - start_time
            logger.error(f"Failed to load {self.model_name}: {str(e)}")
            
            return ModelLoadResult(
                success=False,
                error=e,
                load_time=load_time,
                message=f"Failed to load {self.model_name}: {str(e)}"
            )
    
    def predict(self, *args, **kwargs) -> Any:
        """
        Make predictions with the model.
        
        Automatically loads the model if not already loaded.
        """
        if not self.is_loaded:
            load_result = self.load()
            if not load_result.success:
                raise RuntimeError(f"Failed to load model {self.model_name}: {load_result.message}")
        
        return self._predict(*args, **kwargs)
    
    def unload(self) -> None:
        """Unload the model from memory."""
        self.model = None
        self.is_loaded = False
        logger.info(f"Unloaded {self.model_name}")
    
    def _download_model(self) -> None:
        """Download model from URL if configured."""
        if not self.config.download_url or not self.config.model_path:
            return
        
        import urllib.request
        from urllib.error import URLError
        
        logger.info(f"Downloading {self.model_name} from {self.config.download_url}")
        
        # Ensure model directory exists
        self.config.model_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            urllib.request.urlretrieve(
                self.config.download_url, 
                self.config.model_path
            )
            logger.info(f"Successfully downloaded {self.model_name}")
        except URLError as e:
            raise RuntimeError(f"Failed to download model {self.model_name}: {str(e)}")
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the model."""
        return {
            'name': self.model_name,
            'type': self.config.model_type.value,
            'loaded': self.is_loaded,
            'load_time': self.load_time,
            'model_path': str(self.config.model_path) if self.config.model_path else None,
            'input_size': self.config.input_size,
            'device': self.config.device,
            'settings': self.config.settings
        }
