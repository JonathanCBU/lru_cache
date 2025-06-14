"""Module exceptions."""

from enum import IntEnum
from logging import getLogger

GENERIC_CODE_BOUNDS = [1000, 1999]
NODE_CODE_BOUNDS = [2000, 2999]
CACHE_CODE_BOUNDS = [3000, 3999]


class CacheErrorCode(IntEnum):
    """Integer error codes for cache library exceptions.

    Error code ranges:
    - 1000-1999: General cache errors
    - 2000-2999: Node-related errors
    - 3000-3999: Cache operation errors
    - 4000-4999: Configuration errors
    - 5000-5999: Reserved for future use
    """

    # General Cache Errors (1000-1999)
    UNKNOWN_ERROR = 1000
    GENERIC_ERROR = 1001

    # Node Errors (2000-2999)
    NODE_ERROR = 2000
    INVALID_NODE_TYPE = 2001
    INVALID_NODE_LINK = 2002
    NODE_SELF_LINK = 2003

    # Cache Operation Errors (3000-3999)
    CACHE_KEY_NOT_FOUND = 3001
    CACHE_EVICTION_FAILED = 3002
    CACHE_LOOKUP_FAILED = 3003

    @classmethod
    def get_category(cls, code: int) -> str:
        """Get the category name for an error code.

        Args:
            code: The error code integer

        Returns:
            Category name as string
        """
        if GENERIC_CODE_BOUNDS[0] <= code <= GENERIC_CODE_BOUNDS[1]:
            return "General Cache Error"
        if NODE_CODE_BOUNDS[0] <= code <= NODE_CODE_BOUNDS[1]:
            return "Node Error"
        if CACHE_CODE_BOUNDS[0] <= code <= CACHE_CODE_BOUNDS[1]:
            return "Cache Operation Error"
        return "Unknown Category"


ERROR_CODE_MESSAGES = {
    CacheErrorCode.UNKNOWN_ERROR: "An unknown error occurred",
    CacheErrorCode.GENERIC_ERROR: "General cache error",
    # Node errors
    CacheErrorCode.NODE_ERROR: "General node error",
    CacheErrorCode.INVALID_NODE_TYPE: "Invalid data type for node",
    CacheErrorCode.INVALID_NODE_LINK: "Invalid node link operation",
    CacheErrorCode.NODE_SELF_LINK: "Node trying to link to self",
    # Cache operation errors
    CacheErrorCode.CACHE_KEY_NOT_FOUND: "Cache key not found",
    CacheErrorCode.CACHE_EVICTION_FAILED: "Failed to evict cache entry",
    CacheErrorCode.CACHE_LOOKUP_FAILED: "Failed to find node in cache.",
}


class GenericError(Exception):
    """Base class for all exceptions with logging."""

    def __init__(self, message: str, code: int) -> None:
        """Create exception and log."""
        self.logger = getLogger(__name__)
        self.code = code
        self.message = message
        self.logger.exception(str(self))
        super().__init__(message)

    def __str__(self) -> str:
        """String representation of custom errors."""
        return f"{self.code}: {self.message}"


class NodeError(GenericError):
    """Base class for node exceptions."""


class InvalidNodeLinkError(NodeError):
    """Raised when node.next is invalid."""

    def __init__(
        self,
        message: str = ERROR_CODE_MESSAGES[CacheErrorCode.INVALID_NODE_LINK],
        code: int = CacheErrorCode.INVALID_NODE_LINK,
    ) -> None:
        """Log node link error."""
        super().__init__(message, code)


class InvalidNodeDataError(NodeError):
    """Raised when node.data is invalid."""

    def __init__(
        self,
        message: str = ERROR_CODE_MESSAGES[CacheErrorCode.INVALID_NODE_TYPE],
        code: int = CacheErrorCode.INVALID_NODE_TYPE,
    ) -> None:
        """Log data type error."""
        super().__init__(message, code)


class NodeSelfLinkError(NodeError):
    """Raised when a node tries to make itself it's own next."""

    def __init__(
        self,
        message: str = ERROR_CODE_MESSAGES[CacheErrorCode.NODE_SELF_LINK],
        code: int = CacheErrorCode.NODE_SELF_LINK,
    ) -> None:
        """Log self reference error."""
        super().__init__(message, code)


class CacheError(GenericError):
    """Base class for cache errors."""


class CacheNodeNotFoundError(CacheError):
    """Raised when node not found in cache."""

    def __init__(
        self,
        message: str = ERROR_CODE_MESSAGES[CacheErrorCode.CACHE_LOOKUP_FAILED],
        code: int = CacheErrorCode.CACHE_LOOKUP_FAILED,
    ) -> None:
        """Log cache not found."""
        super().__init__(message, code)


class CacheLookupError(CacheError):
    """Raised when cache lookup key invalid."""

    def __init__(
        self,
        message: str = ERROR_CODE_MESSAGES[CacheErrorCode.CACHE_LOOKUP_FAILED],
        code: int = CacheErrorCode.CACHE_LOOKUP_FAILED,
    ) -> None:
        """Log lookup failure."""
        super().__init__(message, code)
