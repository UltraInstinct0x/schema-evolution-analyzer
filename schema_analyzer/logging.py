"""Logging configuration for Schema Evolution Analyzer"""

import structlog
from elasticsearch import AsyncElasticsearch
import sentry_sdk
from typing import Dict, Any
import logging.config
import json

def setup_logging(config: Dict[str, Any]) -> None:
    """Configure structured logging with ELK stack integration"""
    
    # Configure Sentry for error tracking
    sentry_sdk.init(
        dsn=config['sentry_dsn'],
        traces_sample_rate=0.1,
        environment=config['environment']
    )
    
    # Configure structured logging
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Configure logging to Elasticsearch
    es_logger = ElasticsearchLogger(
        hosts=[config['elasticsearch_host']],
        index_prefix=config['elasticsearch_index_prefix'],
    )
    
    # Configure general logging
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'json': {
                '()': structlog.stdlib.ProcessorFormatter,
                'processor': structlog.processors.JSONRenderer(),
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'json',
            },
            'elasticsearch': {
                '()': lambda: es_logger,
                'level': 'INFO',
            },
        },
        'root': {
            'handlers': ['console', 'elasticsearch'],
            'level': config['log_level'],
        },
    })

class ElasticsearchLogger:
    """Custom logger for Elasticsearch integration"""
    
    def __init__(self, hosts: list, index_prefix: str):
        self.es = AsyncElasticsearch(hosts=hosts)
        self.index_prefix = index_prefix
    
    async def emit(self, record: logging.LogRecord) -> None:
        """Send log record to Elasticsearch"""
        try:
            log_entry = {
                'timestamp': record.created,
                'level': record.levelname,
                'message': record.getMessage(),
                'logger': record.name,
                'path': record.pathname,
                'line_number': record.lineno,
            }
            
            if hasattr(record, 'stack_info'):
                log_entry['stack_info'] = record.stack_info
            
            await self.es.index(
                index=f"{self.index_prefix}-{record.created:%Y.%m.%d}",
                document=log_entry
            )
        except Exception as e:
            # Fallback to console logging if Elasticsearch is unavailable
            print(f"Failed to log to Elasticsearch: {e}")