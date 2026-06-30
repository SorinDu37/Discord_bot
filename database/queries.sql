-- name: upsert_user
INSERT INTO users (user_id, username, exp, last_connection)
VALUES (?, ?, ?, ?)
ON CONFLICT(user_id) DO UPDATE SET
    username = excluded.username,
    exp = users.exp + excluded.exp,
    last_connection = excluded.last_connection;

-- name: get_leaderboard
SELECT username, exp 
FROM users 
ORDER BY exp DESC 
LIMIT 10;

-- name: set_rank
INSERT INTO ranks (role_id, required_exp)
VALUES (?, ?)
ON CONFLICT(role_id) DO UPDATE SET required_exp = excluded.required_exp;

-- name: modify_user_exp
UPDATE users 
SET exp = CASE 
    WHEN (exp + ?) < 0 THEN 0 
    ELSE (exp + ?) 
END
WHERE user_id = ?;

-- name: check_eligible_ranks
SELECT role_id FROM ranks WHERE required_exp <= ?;