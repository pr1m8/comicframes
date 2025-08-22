"""Central cache management system."""

from typing import Any, Optional
from ..config import get_settings, CacheConfig
from .file_cache import FileCache
from .memory_cache import MemoryCache


class CacheManager:
    """Central manager for all caching operations."""
    
    def __init__(self, cache_config: Optional[CacheConfig] = None):
        """Initialize cache manager."""
        if cache_config is None:
            settings = get_settings()
            cache_config = CacheConfig(cache_dir=settings.cache_dir)
        
        self.config = cache_config
        
        # Initialize different cache types
        self.frame_cache = FileCache(
            cache_dir=cache_config.get_frame_cache_dir(),
            ttl=cache_config.frame_cache_ttl,
            max_size_mb=cache_config.max_frame_cache_size
        ) if cache_config.enable_frame_cache else None
        
        self.model_cache = FileCache(
            cache_dir=cache_config.get_model_cache_dir(),
            ttl=cache_config.model_cache_ttl,
            max_size_mb=cache_config.max_model_cache_size
        ) if cache_config.enable_model_cache else None
        
        self.processing_cache = FileCache(
            cache_dir=cache_config.get_processing_cache_dir(),
            ttl=cache_config.processing_cache_ttl,
            max_size_mb=cache_config.max_processing_cache_size
        ) if cache_config.enable_processing_cache else None
        
        # In-memory cache for frequently accessed data
        self.memory_cache = MemoryCache(ttl=300, max_size=100)  # 5 minutes, 100 items
    
    def get_frame_data(self, key: str, default: Any = None) -> Any:
        """Get cached frame data."""
        if self.frame_cache is None:
            return default
        return self.frame_cache.get(key, default)
    
    def set_frame_data(self, key: str, value: Any) -> None:
        """Cache frame data."""
        if self.frame_cache is not None:
            self.frame_cache.set(key, value)
    
    def get_model_data(self, key: str, default: Any = None) -> Any:
        """Get cached model data."""
        if self.model_cache is None:
            return default
        return self.model_cache.get(key, default)
    
    def set_model_data(self, key: str, value: Any) -> None:
        """Cache model data."""
        if self.model_cache is not None:
            self.model_cache.set(key, value)
    
    def get_processing_data(self, key: str, default: Any = None) -> Any:
        """Get cached processing data."""
        if self.processing_cache is None:
            return default
        return self.processing_cache.get(key, default)
    
    def set_processing_data(self, key: str, value: Any) -> None:
        """Cache processing data."""
        if self.processing_cache is not None:
            self.processing_cache.set(key, value)
    
    def get_memory_data(self, key: str, default: Any = None) -> Any:
        """Get data from memory cache."""
        return self.memory_cache.get(key, default)
    
    def set_memory_data(self, key: str, value: Any) -> None:
        """Set data in memory cache."""
        self.memory_cache.set(key, value)
    
    def clear_all(self) -> None:
        """Clear all caches."""
        if self.frame_cache:
            self.frame_cache.clear()
        if self.model_cache:
            self.model_cache.clear()
        if self.processing_cache:
            self.processing_cache.clear()
        self.memory_cache.clear()
    
    def cleanup_expired(self) -> None:
        """Clean up expired entries from all caches."""
        if self.frame_cache:
            self.frame_cache.cleanup_expired()
        if self.model_cache:
            self.model_cache.cleanup_expired()
        if self.processing_cache:
            self.processing_cache.cleanup_expired()
        self.memory_cache.cleanup_expired()
    
    def get_cache_stats(self) -> dict:
        """Get statistics for all caches."""
        stats = {
            'memory_cache': self.memory_cache.get_stats()
        }
        
        if self.frame_cache:
            stats['frame_cache'] = self.frame_cache.get_stats()
        if self.model_cache:
            stats['model_cache'] = self.model_cache.get_stats()
        if self.processing_cache:
            stats['processing_cache'] = self.processing_cache.get_stats()
        
        return stats


# Global cache manager instance
_cache_manager: Optional[CacheManager] = None


def get_cache_manager() -> CacheManager:
    """Get the global cache manager instance."""
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager()
    return _cache_manager


def set_cache_manager(cache_manager: CacheManager) -> None:
    """Set the global cache manager instance."""
    global _cache_manager
    _cache_manager = cache_manager
