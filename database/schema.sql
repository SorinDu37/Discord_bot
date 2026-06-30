
-- Creates the core table if it does not exist yet
CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT PRIMARY KEY,
    username TEXT NOT NULL,
    exp INTEGER DEFAULT 0
);

-- Creates ranks to give
CREATE TABLE IF NOT EXISTS ranks (
    role_id BIGINT PRIMARY KEY,
    role_name TEXT NOT NULL,
    required_exp INTEGER NOT NULL UNIQUE
);

-- Create an index on EXP to make queries fast
CREATE INDEX IF NOT EXISTS idx_users_exp ON users(exp DESC);
