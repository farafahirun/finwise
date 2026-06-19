CREATE TABLE IF NOT EXISTS user_xp (
    xp_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    total_xp INT DEFAULT 0,
    level INT DEFAULT 1,
    title VARCHAR(100) DEFAULT 'Starter',
    FOREIGN KEY (user_id) REFERENCES app_users(user_id)
);

CREATE TABLE IF NOT EXISTS xp_history (
    history_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    activity VARCHAR(255) NOT NULL,
    xp_amount INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES app_users(user_id)
);
