"""Minimal retry wrapper for transient errors (standard library only)."""
import time
from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


def retry(
    function: Callable[[], T],
    attempts: int = 3,
    base_delay: float = 0.25,
    retry_on: tuple[type[Exception], ...] = (TimeoutError,),
) -> T:
    if attempts < 1 or base_delay < 0:
        raise ValueError("attempts must be positive and delay nonnegative")
    for attempt in range(attempts):
        try:
            return function()
        except retry_on:
            if attempt == attempts - 1:
                raise
            time.sleep(base_delay * (2 ** attempt))
    raise RuntimeError("unreachable")
