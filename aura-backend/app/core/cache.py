"""Simple in-memory caching layer with TTL support"""
from typing import Any, Optional
from datetime import datetime, timedelta
import threading


class CacheEntry:
    """Cache entry with value and expiration time"""
    def __init__(self, value: Any, ttl_seconds: int):
        self.value = value
        self.expires_at = datetime.utcnow() + timedelta(seconds=ttl_seconds)
    
    def is_expired(self) -> bool:
        """Check if cache entry has expired"""
        return datetime.utcnow() > self.expires_at


class InMemoryCache:
    """
    Simple in-memory cache with TTL support
    
    This is a basic implementation for development. In production,
    use Redis or Memcached for distributed caching.
    """
    
    def __init__(self):
        self._cache = {}
        self._lock = threading.Lock()
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache
        
        Args:
            key: Cache key
            
        Returns:
            Cached value if exists and not expired, None otherwise
        """
        with self._lock:
            entry = self._cache.get(key)
            
            if entry is None:
                return None
            
            if entry.is_expired():
                # Remove expired entry
                del self._cache[key]
                return None
            
            return entry.value
    
    def set(self, key: str, value: Any, ttl_seconds: int = 300):
        """
        Set value in cache with TTL
        
        Args:
            key: Cache key
            value: Value to cache
            ttl_seconds: Time to live in seconds (default: 300 = 5 minutes)
        """
        with self._lock:
            self._cache[key] = CacheEntry(value, ttl_seconds)
    
    def delete(self, key: str):
        """
        Delete value from cache
        
        Args:
            key: Cache key to delete
        """
        with self._lock:
            if key in self._cache:
                del self._cache[key]
    
    def clear(self):
        """Clear all cache entries"""
        with self._lock:
            self._cache.clear()
    
    def invalidate_pattern(self, pattern: str):
        """
        Invalidate all keys matching pattern
        
        Args:
            pattern: Pattern to match (simple prefix matching)
        """
        with self._lock:
            keys_to_delete = [
                key for key in self._cache.keys()
                if key.startswith(pattern)
            ]
            for key in keys_to_delete:
                del self._cache[key]
    
    def cleanup_expired(self):
        """Remove all expired entries"""
        with self._lock:
            expired_keys = [
                key for key, entry in self._cache.items()
                if entry.is_expired()
            ]
            for key in expired_keys:
                del self._cache[key]
    
    def size(self) -> int:
        """Get number of entries in cache"""
        with self._lock:
            return len(self._cache)


# Global cache instance
cache = InMemoryCache()
