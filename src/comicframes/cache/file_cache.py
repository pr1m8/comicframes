"""File-based caching implementation."""

import hashlib
import json
import pickle
import time
from pathlib import Path
from typing import Any, Optional, Union, Dict
import shutil


class FileCache:
    """File-based cache for storing processed data."""
    
    def __init__(self, cache_dir: Path, ttl: int = 3600, max_size_mb: int = 1000):
        """
        Initialize file cache.
        
        Args:
            cache_dir: Directory to store cache files
            ttl: Time to live in seconds
            max_size_mb: Maximum cache size in MB
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = ttl
        self.max_size_mb = max_size_mb
        self.metadata_file = self.cache_dir / "metadata.json"
        self._load_metadata()
    
    def _load_metadata(self) -> None:
        """Load cache metadata."""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r') as f:
                    self.metadata = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.metadata = {}
        else:
            self.metadata = {}
    
    def _save_metadata(self) -> None:
        """Save cache metadata."""
        try:
            with open(self.metadata_file, 'w') as f:
                json.dump(self.metadata, f, indent=2)
        except IOError:
            pass  # Fail silently for metadata writes
    
    def _get_cache_key(self, key: str) -> str:
        """Generate a cache key hash."""
        return hashlib.md5(key.encode()).hexdigest()
    
    def _get_cache_path(self, cache_key: str) -> Path:
        """Get the file path for a cache key."""
        return self.cache_dir / f"{cache_key}.cache"
    
    def _is_expired(self, cache_key: str) -> bool:
        """Check if a cache entry is expired."""
        if cache_key not in self.metadata:
            return True
        
        created_time = self.metadata[cache_key].get('created_time', 0)
        return time.time() - created_time > self.ttl
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from cache."""
        cache_key = self._get_cache_key(key)
        cache_path = self._get_cache_path(cache_key)
        
        if not cache_path.exists() or self._is_expired(cache_key):
            return default
        
        try:
            with open(cache_path, 'rb') as f:
                return pickle.load(f)
        except (pickle.PickleError, IOError):
            # Remove corrupted cache file
            self._remove_entry(cache_key)
            return default
    
    def set(self, key: str, value: Any) -> None:
        """Set a value in cache."""
        cache_key = self._get_cache_key(key)
        cache_path = self._get_cache_path(cache_key)
        
        try:
            with open(cache_path, 'wb') as f:
                pickle.dump(value, f)
            
            # Update metadata
            self.metadata[cache_key] = {
                'key': key,
                'created_time': time.time(),
                'size': cache_path.stat().st_size
            }
            self._save_metadata()
            
            # Check cache size and cleanup if needed
            self._cleanup_if_needed()
            
        except (pickle.PickleError, IOError):
            pass  # Fail silently for cache writes
    
    def delete(self, key: str) -> None:
        """Delete a value from cache."""
        cache_key = self._get_cache_key(key)
        self._remove_entry(cache_key)
    
    def _remove_entry(self, cache_key: str) -> None:
        """Remove a cache entry."""
        cache_path = self._get_cache_path(cache_key)
        if cache_path.exists():
            cache_path.unlink()
        if cache_key in self.metadata:
            del self.metadata[cache_key]
            self._save_metadata()
    
    def clear(self) -> None:
        """Clear all cache entries."""
        for cache_file in self.cache_dir.glob("*.cache"):
            cache_file.unlink()
        self.metadata.clear()
        self._save_metadata()
    
    def get_cache_size_mb(self) -> float:
        """Get current cache size in MB."""
        total_size = 0
        for cache_file in self.cache_dir.glob("*.cache"):
            total_size += cache_file.stat().st_size
        return total_size / (1024 * 1024)
    
    def _cleanup_if_needed(self) -> None:
        """Cleanup cache if it exceeds size limit."""
        current_size = self.get_cache_size_mb()
        if current_size <= self.max_size_mb:
            return
        
        # Sort by creation time (oldest first)
        sorted_entries = sorted(
            self.metadata.items(),
            key=lambda x: x[1].get('created_time', 0)
        )
        
        # Remove oldest entries until size is acceptable
        target_size = self.max_size_mb * 0.8  # Clean to 80% of limit
        for cache_key, entry in sorted_entries:
            if current_size <= target_size:
                break
            
            cache_path = self._get_cache_path(cache_key)
            if cache_path.exists():
                file_size_mb = cache_path.stat().st_size / (1024 * 1024)
                cache_path.unlink()
                current_size -= file_size_mb
            
            if cache_key in self.metadata:
                del self.metadata[cache_key]
        
        self._save_metadata()
    
    def cleanup_expired(self) -> None:
        """Remove all expired cache entries."""
        expired_keys = []
        for cache_key in self.metadata:
            if self._is_expired(cache_key):
                expired_keys.append(cache_key)
        
        for cache_key in expired_keys:
            self._remove_entry(cache_key)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total_entries = len(self.metadata)
        total_size_mb = self.get_cache_size_mb()
        expired_count = sum(1 for key in self.metadata if self._is_expired(key))
        
        return {
            'total_entries': total_entries,
            'expired_entries': expired_count,
            'active_entries': total_entries - expired_count,
            'total_size_mb': round(total_size_mb, 2),
            'max_size_mb': self.max_size_mb,
            'usage_percent': round((total_size_mb / self.max_size_mb) * 100, 1)
        }
