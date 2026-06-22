"""
MIT License

Copyright (c) 2024 TheHamkerCat

Database Migration and Initialization Utilities

Handles schema initialization and data migrations for PostgreSQL.
"""

import asyncio
from typing import Optional

from wbb import log
from wbb.core.database import DatabasePool, DatabaseSchema


class DatabaseMigrator:
    """Handles database schema initialization and migrations."""

    def __init__(self, db_pool: DatabasePool):
        self.pool = db_pool
        self.applied_migrations = set()

    async def initialize(self) -> None:
        """Initialize database schema and run pending migrations."""
        try:
            log.info("Initializing database schema...")
            await DatabaseSchema.init_schema(self.pool)
            log.info("Database schema initialized successfully")
        except Exception as e:
            log.error(f"Database initialization failed: {e}")
            raise

    async def get_applied_migrations(self) -> set:
        """Get set of already applied migrations."""
        try:
            rows = await self.pool.fetch(
                "SELECT version FROM schema_migrations ORDER BY applied_at"
            )
            return {row["version"] for row in rows}
        except Exception:
            # Table might not exist yet
            return set()

    async def record_migration(self, version: str) -> None:
        """Record that a migration has been applied."""
        await self.pool.execute(
            'INSERT INTO schema_migrations (version) VALUES ($1) ON CONFLICT DO NOTHING',
            version
        )


async def initialize_database(database_url: str) -> DatabasePool:
    """Initialize database connection pool and schema.
    
    Args:
        database_url: PostgreSQL connection string
        
    Returns:
        Initialized DatabasePool instance
        
    Raises:
        Exception: If connection or schema initialization fails
    """
    pool = DatabasePool(database_url)
    
    try:
        await pool.connect()
        log.info("Connected to PostgreSQL database")
        
        migrator = DatabaseMigrator(pool)
        await migrator.initialize()
        
        log.info("Database initialization complete")
        return pool
    except Exception as e:
        log.error(f"Database initialization failed: {e}")
        await pool.disconnect()
        raise
