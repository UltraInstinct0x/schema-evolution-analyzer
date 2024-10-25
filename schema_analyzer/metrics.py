"""Prometheus metrics configuration for Schema Evolution Analyzer"""

from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time
from functools import wraps
from typing import Callable, Any

# Analysis metrics
ANALYSIS_DURATION = Histogram(
    'schema_analysis_duration_seconds',
    'Time spent performing schema analysis',
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
)

ANALYSIS_ERRORS = Counter(
    'schema_analysis_errors_total',
    'Total number of analysis errors',
    ['error_type']
)

ACTIVE_ANALYSES = Gauge(
    'schema_analysis_active',
    'Number of currently running analyses'
)

CACHE_SIZE = Gauge(
    'schema_analysis_cache_size',
    'Current size of the analysis cache'
)

# Query metrics
QUERY_PROCESSING_TIME = Histogram(
    'schema_query_processing_seconds',
    'Time spent processing individual queries',
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0]
)

# Storage metrics
STORAGE_OPERATIONS = Counter(
    'schema_storage_operations_total',
    'Total number of storage operations',
    ['operation_type']
)

STORAGE_ERRORS = Counter(
    'schema_storage_errors_total',
    'Total number of storage errors',
    ['error_type']
)

def instrument_method(metric: Histogram) -> Callable:
    """Decorator to instrument methods with Prometheus metrics"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.time()
            ACTIVE_ANALYSES.inc()
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                ANALYSIS_ERRORS.labels(error_type=type(e).__name__).inc()
                raise
            finally:
                ACTIVE_ANALYSES.dec()
                metric.observe(time.time() - start_time)
        return wrapper
    return decorator