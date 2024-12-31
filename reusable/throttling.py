import time

from django.core.cache import cache
from rest_framework.throttling import BaseThrottle


class BaseCustomThrottle(BaseThrottle):
    scope = None
    rate = None
    num_requests = 5
    duration = 5 * 60

    CACHE_KEY_PREFIX = "throttle"  # Added for cache key clarity

    def get_cache_key(self, request, view):
        """Generate a cache key using the IP address."""
        identifier = self.get_ident(request)  # Renamed for clarity
        return f"{self.CACHE_KEY_PREFIX}_{self.scope}_{identifier}"

    def clean_request_history(self, request_history, now):
        """Remove timestamps older than the allowed duration."""
        return [
            timestamp
            for timestamp in request_history
            if timestamp > now - self.duration
        ]

    def allow_request(self, request, view):
        """Check if the incoming request should be allowed."""
        cache_key = self.get_cache_key(request, view)
        if cache_key is None:
            return True

        # Retrieve and clean request history
        request_history = cache.get(cache_key, [])
        now = time.time()
        request_history = self.clean_request_history(request_history, now)

        # Deny request if too many were made recently
        if len(request_history) >= self.num_requests:
            return False

        # Update cache without logging the current request yet
        cache.set(cache_key, request_history, self.duration)
        return True

    def throttle_failure(self, request, view=None):
        """Log a failed request to the cache for throttling purposes."""
        cache_key = self.get_cache_key(request, view)
        if cache_key:
            request_history = cache.get(cache_key, [])
            # Add the current timestamp to the history and update the cache
            request_history.insert(0, time.time())
            cache.set(cache_key, request_history, self.duration)
