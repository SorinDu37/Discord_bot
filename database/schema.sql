
-- Creates the core table if it does not exist yet
CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT PRIMARY KEY,
    username TEXT NOT NULL,
    exp INTEGER DEFAULT 0,
);

-- Create an index on EXP to make queries fast
CREATE INDEX IF NOT EXISTS idx_users_exp ON users(exp DESC);

-- UPSERT: Insert a new user or update an existing user's EXP and timestamp
-- (In your code, replace the '?' placeholders with dynamic values)
INSERT INTO users (user_id, username, exp, last_connection)
VALUES (?, ?, ?, ?)
ON CONFLICT(user_id) DO UPDATE SET
    username = excluded.username,
    exp = users.exp + excluded.exp,

-- Fetch the Top 10 leaderboard
SELECT username, exp
FROM users 
ORDER BY exp DESC 
LIMIT 10;

-- Reset a single user's experience points
UPDATE users 
SET exp = 0 
WHERE user_id = ?;