"""Storage implementation for Schema Evolution Analyzer"""

from abc import ABC, abstractmethod
import asyncpg
from typing import Dict, Any, Optional
import json
from datetime import datetime
import structlog

logger = structlog.get_logger()

class StorageBackend(ABC):
    """Abstract base class for storage backends"""
    
    @abstractmethod
    async def store_result(self, session_id: str, result: Dict[str, Any]) -> None:
        """Store analysis result"""
        pass
    
    @abstractmethod
    async def retrieve_result(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve analysis result"""
        pass
    
    @abstractmethod
    async def store_metrics(self, metrics: Dict[str, Any]) -> None:
        """Store analysis metrics"""
        pass

class PostgresStorage(StorageBackend):
    """PostgreSQL storage backend"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.pool = None
    
    async def initialize(self):
        """Initialize database connection pool"""
        self.pool = await asyncpg.create_pool(
            host=self.config['host'],
            port=self.config['port'],
            user=self.config['user'],
            password=self.config['password'],
            database=self.config['database']
        )
        
        # Create tables if they don't exist
        async with self.pool.acquire() as conn:
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS analysis_results (
                    session_id TEXT PRIMARY KEY,
                    result JSONB,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                )
            ''')
            
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS analysis_metrics (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    metrics JSONB
                )
            ''')
    
    async def store_result(self, session_id: str, result: Dict[str, Any]) -> None:
        """Store analysis result in PostgreSQL"""
        async with self.pool.acquire() as conn:
            await conn.execute(
                '''
                INSERT INTO analysis_results (session_id, result)
                VALUES ($1, $2)
                ON CONFLICT (session_id) DO UPDATE
                SET result = $2
                ''',
                session_id,
                json.dumps(result)
            )
    
    async def retrieve_result(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve analysis result from PostgreSQL"""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                'SELECT result FROM analysis_results WHERE session_id = $1',
                session_id
            )
            return json.loads(row['result']) if row else None
    
    async def store_metrics(self, metrics: Dict[str, Any]) -> None:
        """Store analysis metrics in PostgreSQL"""
        async with self.pool.acquire() as conn:
            await conn.execute(
                'INSERT INTO analysis_metrics (metrics) VALUES ($1)',
                json.dumps(metrics)
            )

class StorageFactory:
    """Factory for creating storage backends"""
    
    @staticmethod
    async def create_storage(config: Dict[str, Any]) -> StorageBackend:
        """Create and initialize storage backend"""
        storage_type = config.get('type', 'postgresql')
        
        if storage_type == 'postgresql':
            storage = PostgresStorage(config)
            await storage.initialize()
            return storage
        else:
            raise ValueError(f"Unsupported storage type: {storage_type}")