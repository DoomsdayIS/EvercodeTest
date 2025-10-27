import time
from functools import wraps
from typing import Callable, Type


def retry(
    max_attempts: int = 3,
    wait_seconds: float = 2.0,
    retry_on: tuple[Type[Exception], ...] = (Exception,),
    return_none_on_failure: bool = False,
) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except retry_on as e:
                    last_exception = e
                    if attempt < max_attempts:
                        time.sleep(wait_seconds)
                except Exception as e:
                    raise e
            if return_none_on_failure:
                return None
            raise last_exception

        return wrapper

    return decorator
