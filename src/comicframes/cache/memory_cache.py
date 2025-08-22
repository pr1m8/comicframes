"""In-memory caching implementation."""

import time
from typing import Any, Dict, Optional, Tuple
from threading import RLock


class MemoryCache:
    """Thread-safe in-memory cache with TTL support."""
    
    def __init__(self, ttl: int = 3600, max_size: int = 1000):
        """
        Initialize memory cache.
        
        Args:
            ttl: Time to live in seconds
            max_size: Maximum number of entries
        """
        self.ttl = ttl
        self.max_size = max_size
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._lock = RLock()
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from cache."""
        with self._lock:
            if key not in self._cache:
                return default
            
            value, timestamp = self._cache[key]
            
            # Check if expired
            if time.time() - timestamp > self.ttl:
                del self._cache[key]
                return default
            
            return value
    
    def set(self, key: str, value: Any) -> None:
        """Set a value in cache."""
        with self._lock:
            # Remove oldest entries if cache is full
            if len(self._cache) >= self.max_size and key not in self._cache:
                self._evict_oldest()
            
            self._cache[key] = (value, time.time())
    
    def delete(self, key: str) -> None:
        """Delete a value from cache."""
        with self._lock:
            self._cache.pop(key, None)
    
    def clear(self) -> None:
        """Clear all cache entries."""
        with self._lock:
            self._cache.clear()
    
    def _evict_oldest(self) -> None:
        """Evict the oldest cache entry."""
        if not self._cache:
            return
        
        oldest_key = min(self._cache.keys(), key=lambda k: self._cache[k][1])
        del self._cache[oldest_key]
    
    def cleanup_expired(self) -> None:
        """Remove all expired cache entries."""
        current_time = time.time()
        with self._lock:
            expired_keys = [
                key for key, (_, timestamp) in self._cache.items()
                if current_time - timestamp > self.ttl
            ]
            
            for key in expired_keys:
                del self._cache[key]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self._lock:
            current_time = time.time()
            expired_count = sum(
                1 for _, timestamp in self._cache.values()
                if current_time - timestamp > self.ttl
            )
            
            return {
                'total_entries': len(self._cache),
                'expired_entries': expired_count,
                'active_entries': len(self._cache) - expired_count,
                'max_size': self.max_size,
                'usage_percent': round((len(self._cache) / self.max_size) * 100, 1)
            }
