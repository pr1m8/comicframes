"""Base processor class for all processing operations."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import time
import logging

from .data_structures import ProcessingResult
from ..cache import get_cache_manager


logger = logging.getLogger(__name__)


class BaseProcessor(ABC):
    """Base class for all processors."""
    
    def __init__(self, name: str, cache_enabled: bool = True):
        """
        Initialize processor.
        
        Args:
            name: Name of the processor
            cache_enabled: Whether to enable caching for this processor
        """
        self.name = name
        self.cache_enabled = cache_enabled
        self.cache_manager = get_cache_manager() if cache_enabled else None
        self.metrics: Dict[str, Any] = {}
    
    @abstractmethod
    def _process(self, *args, **kwargs) -> Any:
        """
        Perform the actual processing.
        
        This method should be implemented by subclasses.
        """
        pass
    
    def process(self, *args, **kwargs) -> ProcessingResult:
        """
        Process with caching, error handling, and metrics.
        
        Returns:
            ProcessingResult with success status and data
        """
        start_time = time.time()
        
        try:
            # Check cache first
            cache_key = self._generate_cache_key(*args, **kwargs)
            cached_result = None
            
            if self.cache_enabled and cache_key:
                cached_result = self.cache_manager.get_processing_data(cache_key)
                if cached_result is not None:
                    logger.debug(f"Cache hit for {self.name}: {cache_key}")
                    processing_time = time.time() - start_time
                    return ProcessingResult.success_result(
                        data=cached_result,
                        processing_time=processing_time,
                        cache_hit=True,
                        message=f"{self.name} completed (cached)"
                    )
            
            # Perform actual processing
            logger.debug(f"Processing {self.name}")
            result = self._process(*args, **kwargs)
            
            # Cache the result
            if self.cache_enabled and cache_key and result is not None:
                self.cache_manager.set_processing_data(cache_key, result)
            
            processing_time = time.time() - start_time
            self._update_metrics(processing_time, True)
            
            return ProcessingResult.success_result(
                data=result,
                processing_time=processing_time,
                cache_hit=False,
                message=f"{self.name} completed successfully"
            )
            
        except Exception as e:
            processing_time = time.time() - start_time
            self._update_metrics(processing_time, False)
            logger.error(f"Error in {self.name}: {str(e)}")
            
            return ProcessingResult.error_result(
                error=e,
                processing_time=processing_time,
                message=f"Error in {self.name}: {str(e)}"
            )
    
    def _generate_cache_key(self, *args, **kwargs) -> Optional[str]:
        """
        Generate a cache key for the given arguments.
        
        Override this method to provide custom caching logic.
        """
        if not self.cache_enabled:
            return None
        
        try:
            import hashlib
            # Create a simple hash of arguments
            key_data = f"{self.name}:{str(args)}:{str(sorted(kwargs.items()))}"
            return hashlib.md5(key_data.encode()).hexdigest()
        except Exception:
            return None
    
    def _update_metrics(self, processing_time: float, success: bool) -> None:
        """Update processor metrics."""
        if 'total_calls' not in self.metrics:
            self.metrics['total_calls'] = 0
            self.metrics['successful_calls'] = 0
            self.metrics['failed_calls'] = 0
            self.metrics['total_time'] = 0.0
            self.metrics['average_time'] = 0.0
        
        self.metrics['total_calls'] += 1
        self.metrics['total_time'] += processing_time
        
        if success:
            self.metrics['successful_calls'] += 1
        else:
            self.metrics['failed_calls'] += 1
        
        self.metrics['average_time'] = self.metrics['total_time'] / self.metrics['total_calls']
        self.metrics['success_rate'] = self.metrics['successful_calls'] / self.metrics['total_calls']
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get processor metrics."""
        return self.metrics.copy()
    
    def reset_metrics(self) -> None:
        """Reset processor metrics."""
        self.metrics.clear()
    
    def clear_cache(self) -> None:
        """Clear cache for this processor."""
        if self.cache_enabled and self.cache_manager:
            # Note: This clears all processing cache, not just for this processor
            # In a more sophisticated implementation, we'd track processor-specific keys
            logger.info(f"Clearing cache for {self.name}")
            self.cache_manager.processing_cache.clear()
