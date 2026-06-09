class ETLUtilsError(Exception):
    """
    Base exception for typed-etl.
    """


class ConfigValidationError(ETLUtilsError):
    """
    Raised when configuration validation fails.
    """


class UnsupportedFileFormatError(ETLUtilsError):
    """
    Raised when unsupported file format is provided.
    """


class MaxRetriesExceededError(ETLUtilsError):
    """
    Raised when retry attempts are exhausted.
    """

    def __init__(
        self,
        function_name: str,
        attempts: int,
        original_exception: Exception,
    ) -> None:
        self.function_name = function_name
        self.attempts = attempts
        self.original_exception = original_exception

        super().__init__(
            f"Function '{function_name}' failed after "
            f"{attempts} attempts. "
            f"Last error: {original_exception}"
        )


class FileReadError(ETLUtilsError):
    """
    Raised when file reading fails.
    """
