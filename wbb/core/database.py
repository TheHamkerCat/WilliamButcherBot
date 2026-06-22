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

    Handles MongoDB-style patterns:
    - $set operator in update dicts
    - $lt, $gt, $exists operators in filter dicts
    - Dummy sentinel filters (e.g. {"pipe": "pipe"}) that match any row
    - BIGINT[] coercion for list-of-int values
    - async for iteration over find() results
    """

    # Columns that are real database columns (not dummy sentinel keys)
    # Sentinel keys are ones whose value equals the key name itself
    # and the column doesn't exist in the table — handled as "get first row"

    def __init__(self, pool: DatabasePool, table_name: str):
        self.pool = pool
        self.table_name = table_name

    # ── Value coercion ──────────────────────────────────────────────────────

    @staticmethod
    def _coerce_value(value: Any) -> Any:
        """Convert Python lists to typed bigint lists for asyncpg."""
        if isinstance(value, (list, tuple)):
            return [int(v) if isinstance(v, int) else v for v in value]
        return value

    @staticmethod
    def _is_sentinel_filter(query: Dict[str, Any]) -> bool:
        """Return True if every key maps to itself (e.g. {"pipe": "pipe"}).

        These are MongoDB hacks to reference a singleton document; in
        PostgreSQL we just select / update / delete the first (or only) row.
        """
        return bool(query) and all(
            isinstance(v, str) and k == v for k, v in query.items()
        )

    # ── WHERE-clause builder ────────────────────────────────────────────────

    def _build_where(
        self, query: Dict[str, Any], start_idx: int = 1
    ) -> tuple:
        """Build a WHERE clause and matching param list from a query dict.

        Handles:
        - Plain equality:   {"col": val}
        - $lt / $gt:        {"col": {"$lt": val}}
        - $exists:          {"col": {"$exists": 1}}  →  col IS NOT NULL

        Returns (sql_fragment, params_list).
        """
        conditions: List[str] = []
        params: List[Any] = []
        idx = start_idx

        for key, val in query.items():
            if isinstance(val, dict):
                op, op_val = next(iter(val.items()))
                if op == "$lt":
                    conditions.append(f"{key} < ${idx}")
                    params.append(self._coerce_value(op_val))
                    idx += 1
                elif op == "$gt":
                    conditions.append(f"{key} > ${idx}")
                    params.append(self._coerce_value(op_val))
                    idx += 1
                elif op == "$exists":
                    conditions.append(f"{key} IS NOT NULL")
                else:
                    conditions.append(f"{key} = ${idx}")
                    params.append(self._coerce_value(val))
                    idx += 1
            else:
                conditions.append(f"{key} = ${idx}")
                params.append(self._coerce_value(val))
                idx += 1

        where = " AND ".join(conditions) if conditions else "TRUE"
        return where, params

    # ── SET-clause builder ──────────────────────────────────────────────────

    def _build_set(
        self, update_dict: Dict[str, Any], start_idx: int = 1
    ) -> tuple:
        """Extract the actual field→value map from an update dict.

        If the dict has a single "$set" key we unwrap it; otherwise we treat
        the whole dict as field→value pairs.  Returns (set_sql, params, next_idx).
        """
        if "$set" in update_dict:
            fields = update_dict["$set"]
        else:
            fields = update_dict

        parts: List[str] = []
        params: List[Any] = []
        idx = start_idx

        for col, val in fields.items():
            coerced = self._coerce_value(val)
            if isinstance(coerced, list) and all(isinstance(x, int) for x in coerced):
                parts.append(f"{col} = ${idx}::bigint[]")
            else:
                parts.append(f"{col} = ${idx}")
            params.append(coerced)
            idx += 1

        return ", ".join(parts), params, idx

    # ── Public API ──────────────────────────────────────────────────────────

    async def find_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find single document. Handles sentinel and operator filters."""
        if self._is_sentinel_filter(query):
            sql = f"SELECT * FROM {self.table_name} LIMIT 1"
            row = await self.pool.fetchrow(sql)
        else:
            where, params = self._build_where(query)
            sql = f"SELECT * FROM {self.table_name} WHERE {where} LIMIT 1"
            row = await self.pool.fetchrow(sql, *params)
        return dict(row) if row else None

    def find(self, query: Dict[str, Any]):
        """Return an async-iterable of matching rows."""
        return _AsyncFind(self.pool, self.table_name, query, self._build_where, self._is_sentinel_filter)

    async def insert_one(self, document: Dict[str, Any]) -> str:
        """Insert a single document."""
        columns = ", ".join(document.keys())
        values = [self._coerce_value(v) for v in document.values()]
        placeholders = []
        for i, v in enumerate(values):
            if isinstance(v, list) and all(isinstance(x, int) for x in v):
                placeholders.append(f"${i+1}::bigint[]")
            else:
                placeholders.append(f"${i+1}")
        sql = (
            f"INSERT INTO {self.table_name} ({columns})"
            f" VALUES ({', '.join(placeholders)}) RETURNING id"
        )
        result = await self.pool.fetchval(sql, *values)
        return str(result)

    async def update_one(
        self,
        filter_dict: Dict[str, Any],
        update_dict: Dict[str, Any],
        upsert: bool = False,
    ) -> None:
        """Update a document (or upsert). Handles $set and sentinel filters."""
        existing = await self.find_one(filter_dict)

        if existing:
            set_sql, set_params, next_idx = self._build_set(update_dict, start_idx=1)

            if self._is_sentinel_filter(filter_dict):
                # Update first/only row using primary key
                pk = existing.get("id")
                if pk is not None:
                    sql = f"UPDATE {self.table_name} SET {set_sql} WHERE id = ${next_idx}"
                    await self.pool.execute(sql, *set_params, pk)
                else:
                    sql = f"UPDATE {self.table_name} SET {set_sql}"
                    await self.pool.execute(sql, *set_params)
            else:
                where, where_params = self._build_where(filter_dict, start_idx=next_idx)
                sql = f"UPDATE {self.table_name} SET {set_sql} WHERE {where}"
                await self.pool.execute(sql, *set_params, *where_params)

        elif upsert:
            # Build the document to insert
            if "$set" in update_dict:
                fields = update_dict["$set"]
            else:
                fields = update_dict

            if not self._is_sentinel_filter(filter_dict):
                doc = {**filter_dict, **fields}
            else:
                doc = dict(fields)

            await self.insert_one(doc)

    async def delete_one(self, filter_dict: Dict[str, Any]) -> None:
        """Delete a single document."""
        if self._is_sentinel_filter(filter_dict):
            # Delete the first row (sentinel tables have one row)
            sql = f"DELETE FROM {self.table_name} WHERE id = (SELECT id FROM {self.table_name} LIMIT 1)"
            await self.pool.execute(sql)
        else:
            where, params = self._build_where(filter_dict)
            sql = f"DELETE FROM {self.table_name} WHERE id = (SELECT id FROM {self.table_name} WHERE {where} LIMIT 1)"
            await self.pool.execute(sql, *params)


class _AsyncFind:
    """Async-iterable wrapper returned by MongoCompatibilityLayer.find()."""

    def __init__(self, pool, table_name, query, build_where_fn, is_sentinel_fn):
        self._pool = pool
        self._table_name = table_name
        self._query = query
        self._build_where = build_where_fn
        self._is_sentinel = is_sentinel_fn
        self._rows: Optional[List[Any]] = None
        self._idx = 0

    async def _load(self):
        if self._rows is None:
            if self._is_sentinel(self._query):
                sql = f"SELECT * FROM {self._table_name}"
                self._rows = await self._pool.fetch(sql)
            else:
                where, params = self._build_where(self._query)
                sql = f"SELECT * FROM {self._table_name} WHERE {where}"
                self._rows = await self._pool.fetch(sql, *params)

    def __aiter__(self):
        return self

    async def __anext__(self):
        await self._load()
        if self._idx >= len(self._rows):
            raise StopAsyncIteration
        row = dict(self._rows[self._idx])
        self._idx += 1
        return row

    def __await__(self):
        """Allow `await db.find(...)` to return a plain list."""
        async def _collect():
            await self._load()
            return [dict(r) for r in self._rows]
        return _collect().__await__()
