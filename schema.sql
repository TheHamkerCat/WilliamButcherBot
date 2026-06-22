-- PostgreSQL Schema for WilliamButcherBot
-- Generated for PostgreSQL 12+
-- This file defines all tables needed for the bot's functionality

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============ NOTES TABLE ============
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

-- ============ FILTERS TABLE ============
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

-- ============ WARNS TABLE ============
CREATE TABLE IF NOT EXISTS warns (
    id SERIAL PRIMARY KEY,
    chat_id BIGINT NOT NULL,
    warns_data JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(chat_id)
);
CREATE INDEX IF NOT EXISTS idx_warns_chat_id ON warns(chat_id);

-- ============ KARMA TABLE ============
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

-- ============ CHATS TABLE ============
CREATE TABLE IF NOT EXISTS chats (
    id SERIAL PRIMARY KEY,
    chat_id BIGINT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_chats_chat_id ON chats(chat_id);

-- ============ USERS TABLE ============
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    user_id BIGINT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_users_user_id ON users(user_id);

-- ============ GLOBAL BAN TABLE ============
CREATE TABLE IF NOT EXISTS gban (
    id SERIAL PRIMARY KEY,
    user_id BIGINT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_gban_user_id ON gban(user_id);

-- ============ COUPLE/DATING TABLE ============
CREATE TABLE IF NOT EXISTS couple (
    id SERIAL PRIMARY KEY,
    chat_id BIGINT NOT NULL,
    couple_data JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(chat_id)
);

-- ============ CAPTCHA TABLES ============
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

-- ============ ANTI-SERVICE TABLE ============
CREATE TABLE IF NOT EXISTS antiservice (
    id SERIAL PRIMARY KEY,
    chat_id BIGINT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============ PM PERMIT TABLE ============
CREATE TABLE IF NOT EXISTS pmpermit (
    id SERIAL PRIMARY KEY,
    user_id BIGINT UNIQUE NOT NULL,
    approved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_pmpermit_user_id ON pmpermit(user_id);

-- ============ WELCOME MESSAGES TABLE ============
CREATE TABLE IF NOT EXISTS welcome_text (
    id SERIAL PRIMARY KEY,
    chat_id BIGINT UNIQUE NOT NULL,
    welcome_text TEXT,
    raw_text TEXT,
    file_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============ BLACKLIST FILTERS TABLE ============
CREATE TABLE IF NOT EXISTS blacklist_filters (
    id SERIAL PRIMARY KEY,
    chat_id BIGINT NOT NULL,
    filters TEXT[] DEFAULT ARRAY[]::TEXT[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(chat_id)
);
CREATE INDEX IF NOT EXISTS idx_blacklist_filters_chat_id ON blacklist_filters(chat_id);

-- ============ PIPES/CHAT RELAY TABLE ============
CREATE TABLE IF NOT EXISTS pipes (
    id SERIAL PRIMARY KEY,
    from_chat_id BIGINT NOT NULL,
    to_chat_id BIGINT NOT NULL,
    fetcher VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(from_chat_id, to_chat_id)
);

-- ============ SUDOERS TABLE ============
CREATE TABLE IF NOT EXISTS sudoers (
    id SERIAL PRIMARY KEY,
    sudoers BIGINT[] DEFAULT ARRAY[]::BIGINT[],
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============ BLACKLIST CHATS TABLE ============
CREATE TABLE IF NOT EXISTS blacklist_chat (
    id SERIAL PRIMARY KEY,
    chat_id BIGINT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_blacklist_chat_chat_id ON blacklist_chat(chat_id);

-- ============ RESTART STAGE TABLE ============
CREATE TABLE IF NOT EXISTS restart_stage (
    id SERIAL PRIMARY KEY,
    chat_id BIGINT,
    message_id BIGINT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============ FLOOD TOGGLE TABLE ============
CREATE TABLE IF NOT EXISTS flood_toggle (
    id SERIAL PRIMARY KEY,
    chat_id BIGINT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============ RSS FEEDS TABLE ============
CREATE TABLE IF NOT EXISTS rss (
    id SERIAL PRIMARY KEY,
    chat_id BIGINT UNIQUE NOT NULL,
    url VARCHAR(512) NOT NULL,
    last_title TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_rss_chat_id ON rss(chat_id);

-- ============ RULES TABLE ============
CREATE TABLE IF NOT EXISTS rules (
    id SERIAL PRIMARY KEY,
    chat_id BIGINT UNIQUE NOT NULL,
    rules_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============ CHATBOT TABLE ============
CREATE TABLE IF NOT EXISTS chatbot (
    id SERIAL PRIMARY KEY,
    bot_chats BIGINT[] DEFAULT ARRAY[]::BIGINT[],
    userbot_chats BIGINT[] DEFAULT ARRAY[]::BIGINT[],
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============ FEDERATION TABLES ============
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

-- ============ SCHEMA MIGRATIONS TABLE ============
CREATE TABLE IF NOT EXISTS schema_migrations (
    id SERIAL PRIMARY KEY,
    version VARCHAR(255) UNIQUE NOT NULL,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
