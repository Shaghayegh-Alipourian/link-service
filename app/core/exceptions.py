class LinkServiceError(Exception):
    """Base exception for the application."""


class LinkNotFoundError(LinkServiceError):
    """Raised when a link does not exist."""


class LinkCreationError(LinkServiceError):
    """Raised when link creation fails."""


class RateLimitExceededError(LinkServiceError):
    """Raised when the client exceeds the rate limit."""


class CacheError(LinkServiceError):
    """Raised when a cache operation fails."""