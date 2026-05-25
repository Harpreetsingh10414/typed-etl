class ETLUtilsError(Exception):
    """
    Base exception for typed-etl.
    """


class ConfigValidationError(ETLUtilsError):
    """
    Raised when config validation fails.
    """


class UnsupportedFileFormatError(ETLUtilsError):
    """
    Raised when unsupported file format is used.
    """


class MaxRetriesExceededError(ETLUtilsError):
    """
    Raised when retry attempts are exhausted.
    """
