CREATE TABLE IF NOT EXISTS user_learning_progress (
    progress_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    topic_id VARCHAR(100) NOT NULL,
    progress_type VARCHAR(50) NOT NULL, -- MATERIAL, QUIZ
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES app_users(user_id),
    UNIQUE KEY unique_user_topic (user_id, topic_id, progress_type)
);
