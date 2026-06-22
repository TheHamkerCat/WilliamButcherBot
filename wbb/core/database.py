"""
MIT License

Copyright (c) 2024 TheHamkerCat

PostgreSQL Database Connection and Schema Management Module

Replaces MongoDB (motor) with async PostgreSQL (asyncpg) for production-grade
data persistence with connection pooling and automatic migrations.
"""

import asyncio
import json
from typing import Any, Dict, List, Optional

import asyncpg
from wbb import log


class DatabasePool:
    """Manages PostgreSQL connection pool and query execution."""

    def __init__(self, database_url: str, min_size: int = 10, max_size: int = 20):
        self.database_url = database_url
        self.min_size = min_size
        self.max_size = max_size
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self) -> None:
        """Initialize connection pool."""
        try:
            self.pool = await asyncpg.create_pool(
                self.database_url,
                min_size=self.min_size,
                max_size=self.max_size,
                command_timeout=60,
            )
            log.info("PostgreSQL connection pool initialized")
        except Exception as e:
            log.error(f"Failed to connect to PostgreSQL: {e}")
            raise

    async def disconnect(self) -> None:
        """Close connection pool."""
        if self.pool:
            await self.pool.close()
            log.info("PostgreSQL connection pool closed")

    async def execute(self, query: str, *args) -> Any:
        """Execute a query and return result."""
        if not self.pool:
            raise RuntimeError("Database pool not initialized")
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)

    async def fetch(self, query: str, *args) -> List[asyncpg.Record]:
        """Fetch multiple rows."""
        if not self.pool:
            raise RuntimeError("Database pool not initialized")
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)

    async def fetchrow(self, query: str, *args) -> Optional[asyncpg.Record]:
        """Fetch single row."""
        if not self.pool:
            raise RuntimeError("Database pool not initialized")
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, *args)

    async def fetchval(self, query: str, *args) -> Any:
        """Fetch single value."""
        if not self.pool:
            raise RuntimeError("Database pool not initialized")
        async with self.pool.acquire() as conn:
            return await conn.fetchval(query, *args)


class DatabaseSchema:
    """Creates and manages PostgreSQL schema."""

    SCHEMA_SQL = """
    -- Enable UUID extension
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

    -- Notes table
    CREATE TABLE IF NOT EXISTS notes (
        id SERIAL PRIMARY KEY,
        chat_id BIGINT NOT NULL,
        name VARCHAR(255) NOT NULL,
        note_data JSONB NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(chat_id, name)
    );
    CREATE INDEX IF NOT EXISTS idx_notes_chat_id ON notes(chat_id);

    -- Filters table
    CREATE TABLE IF NOT EXISTS filters (
        id SERIAL PRIMARY KEY,
        chat_id BIGINT NOT NULL,
        name VARCHAR(255) NOT NULL,
        filter_data JSONB NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(chat_id, name)
    );
    CREATE INDEX IF NOT EXISTS idx_filters_chat_id ON filters(chat_id);

    -- Warns table
    CREATE TABLE IF NOT EXISTS warns (
        id SERIAL PRIMARY KEY,
        chat_id BIGINT NOT NULL,
        warns_data JSONB NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(chat_id)
    );
    CREATE INDEX IF NOT EXISTS idx_warns_chat_id ON warns(chat_id);

    -- Karma table
    CREATE TABLE IF NOT EXISTS karma (
        id SERIAL PRIMARY KEY,
        chat_id BIGINT NOT NULL,
        karma_data JSONB NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(chat_id)
    );
    CREATE INDEX IF NOT EXISTS idx_karma_chat_id ON karma(chat_id);
    CREATE TABLE IF NOT EXISTS karma_toggle (
        id SERIAL PRIMARY KEY,
        chat_id BIGINT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Chats table
    CREATE TABLE IF NOT EXISTS chats (
        id SERIAL PRIMARY KEY,
        chat_id BIGINT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE INDEX IF NOT EXISTS idx_chats_chat_id ON chats(chat_id);

    -- Users table
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        user_id BIGINT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE INDEX IF NOT EXISTS idx_users_user_id ON users(user_id);

    -- Global bans table
    CREATE TABLE IF NOT EXISTS gban (
        id SERIAL PRIMARY KEY,
        user_id BIGINT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE INDEX IF NOT EXISTS idx_gban_user_id ON gban(user_id);

    -- Couple/Dating table
    CREATE TABLE IF NOT EXISTS couple (
        id SERIAL PRIMARY KEY,
        chat_id BIGINT NOT NULL,
        couple_data JSONB NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(chat_id)
    );

    -- Captcha table
    CREATE TABLE IF NOT EXISTS captcha (
        id SERIAL PRIMARY KEY,
        chat_id BIGINT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS solved_captcha (
        id SERIAL PRIMARY KEY,
        chat_id BIGINT NOT NULL,
        user_id BIGINT NOT NULL,
        solved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(chat_id, user_id)
    );
    CREATE TABLE IF NOT EXISTS captcha_cache (
        id SERIAL PRIMARY KEY,
        cache_key VARCHAR(255) UNIQUE NOT NULL,
        pickled_data TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Anti-service table
    CREATE TABLE IF NOT EXISTS antiservice (
        id SERIAL PRIMARY KEY,
        chat_id BIGINT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- PM permit table
    CREATE TABLE IF NOT EXISTS pmpermit (
        id SERIAL PRIMARY KEY,
        user_id BIGINT UNIQUE NOT NULL,
        approved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE INDEX IF NOT EXISTS idx_pmpermit_user_id ON pmpermit(user_id);

    -- Welcome messages table
    CREATE TABLE IF NOT EXISTS welcome_text (
        id SERIAL PRIMARY KEY,
        chat_id BIGINT UNIQUE NOT NULL,
        welcome_text TEXT,
        raw_text TEXT,
        file_id VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Blacklist filters table
    CREATE TABLE IF NOT EXISTS blacklist_filters (
        id SERIAL PRIMARY KEY,
        chat_id BIGINT NOT NULL,
        filters TEXT[] DEFAULT ARRAY[]::TEXT[],
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(chat_id)
    );
    CREATE INDEX IF NOT EXISTS idx_blacklist_filters_chat_id ON blacklist_filters(chat_id);

    -- Pipes/Chat relay table
    CREATE TABLE IF NOT EXISTS pipes (
        id SERIAL PRIMARY KEY,
        from_chat_id BIGINT NOT NULL,
        to_chat_id BIGINT NOT NULL,
        fetcher VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(from_chat_id, to_chat_id)
    );

    -- Sudoers table
    CREATE TABLE IF NOT EXISTS sudoers (
        id SERIAL PRIMARY KEY,
        sudoers BIGINT[] DEFAULT ARRAY[]::BIGINT[],
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Blacklist chats table
    CREATE TABLE IF NOT EXISTS blacklist_chat (
        id SERIAL PRIMARY KEY,
        chat_id BIGINT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE INDEX IF NOT EXISTS idx_blacklist_chat_chat_id ON blacklist_chat(chat_id);

    -- Restart stage table
    CREATE TABLE IF NOT EXISTS restart_stage (
        id SERIAL PRIMARY KEY,
        chat_id BIGINT,
        message_id BIGINT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Flood toggle table
    CREATE TABLE IF NOT EXISTS flood_toggle (
        id SERIAL PRIMARY KEY,
        chat_id BIGINT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- RSS feeds table
    CREATE TABLE IF NOT EXISTS rss (
        id SERIAL PRIMARY KEY,
        chat_id BIGINT UNIQUE NOT NULL,
        url VARCHAR(512) NOT NULL,
        last_title TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE INDEX IF NOT EXISTS idx_rss_chat_id ON rss(chat_id);

    -- Rules table
    CREATE TABLE IF NOT EXISTS rules (
        id SERIAL PRIMARY KEY,
        chat_id BIGINT UNIQUE NOT NULL,
        rules_text TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Chatbot table
    CREATE TABLE IF NOT EXISTS chatbot (
        id SERIAL PRIMARY KEY,
        bot_chats BIGINT[] DEFAULT ARRAY[]::BIGINT[],
        userbot_chats BIGINT[] DEFAULT ARRAY[]::BIGINT[],
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Federation tables
    CREATE TABLE IF NOT EXISTS feds (
        id SERIAL PRIMARY KEY,
        fed_id VARCHAR(255) UNIQUE NOT NULL,
        fed_name VARCHAR(255) NOT NULL,
        owner_id BIGINT NOT NULL,
        owner_mention VARCHAR(255),
        fadmins BIGINT[] DEFAULT ARRAY[]::BIGINT[],
        chat_ids JSONB DEFAULT '[]'::jsonb,
        banned_users JSONB DEFAULT '[]'::jsonb,
        log_group_id BIGINT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE INDEX IF NOT EXISTS idx_feds_fed_id ON feds(fed_id);
    CREATE INDEX IF NOT EXISTS idx_feds_owner_id ON feds(owner_id);

    -- Migration metadata table
    CREATE TABLE IF NOT EXISTS schema_migrations (
        id SERIAL PRIMARY KEY,
        version VARCHAR(255) UNIQUE NOT NULL,
        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    @staticmethod
    async def init_schema(pool: DatabasePool) -> None:
        """Initialize database schema."""
        try:
            # Split into individual statements and execute
            statements = [
                s.strip() for s in DatabaseSchema.SCHEMA_SQL.split(";") if s.strip()
            ]
            for statement in statements:
                await pool.execute(statement)
            log.info("PostgreSQL schema initialized successfully")
        except Exception as e:
            log.error(f"Failed to initialize schema: {e}")
            raise


class MongoCompatibilityLayer:
    """Provides MongoDB-like interface for PostgreSQL queries.
    
    Simplifies migration by maintaining similar API to MongoDB operations.
    """

    def __init__(self, pool: DatabasePool, table_name: str):
        self.pool = pool
        self.table_name = table_name

    async def find_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find single document."""
        where_clause = self._build_where_clause(query)
        sql = f"SELECT * FROM {self.table_name} WHERE {where_clause} LIMIT 1"
        params = list(query.values())
        row = await self.pool.fetchrow(sql, *params)
        return dict(row) if row else None

    async def find(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find multiple documents."""
        where_clause = self._build_where_clause(query)
        sql = f"SELECT * FROM {self.table_name} WHERE {where_clause}"
        params = list(query.values())
        rows = await self.pool.fetch(sql, *params)
        return [dict(row) for row in rows]

    async def insert_one(self, document: Dict[str, Any]) -> str:
        """Insert single document."""
        columns = ", ".join(document.keys())
        placeholders = ", ".join([f"${i+1}" for i in range(len(document))])
        sql = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders}) RETURNING id"
        result = await self.pool.fetchval(sql, *document.values())
        return str(result)

    async def update_one(
        self, filter_dict: Dict[str, Any], update_dict: Dict[str, Any], upsert: bool = False
    ) -> None:
        """Update single document or insert if not exists (upsert)."""
        existing = await self.find_one(filter_dict)
        
        if existing:
            where_clause = self._build_where_clause(filter_dict)
            set_clause = ", ".join([f"{k}=${i+1}" for i, k in enumerate(update_dict.keys())])
            sql = f"UPDATE {self.table_name} SET {set_clause} WHERE {where_clause}"
            params = list(update_dict.values()) + list(filter_dict.values())
            await self.pool.execute(sql, *params)
        elif upsert:
            doc = {**filter_dict, **update_dict}
            await self.insert_one(doc)

    async def delete_one(self, filter_dict: Dict[str, Any]) -> None:
        """Delete single document."""
        where_clause = self._build_where_clause(filter_dict)
        sql = f"DELETE FROM {self.table_name} WHERE {where_clause}"
        await self.pool.execute(sql, *filter_dict.values())

    @staticmethod
    def _build_where_clause(query: Dict[str, Any]) -> str:
        """Build WHERE clause from query dict."""
        conditions = []
        for i, key in enumerate(query.keys(), 1):
            conditions.append(f"{key} = ${i}")
        return " AND ".join(conditions)
