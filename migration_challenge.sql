CREATE TABLE IF NOT EXISTS challenge_master (
    challenge_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    difficulty VARCHAR(50) NOT NULL, -- Easy, Medium, Hard
    reward_xp INT NOT NULL,
    challenge_type VARCHAR(50) NOT NULL, -- WEEKLY, MONTHLY
    metric_type VARCHAR(50) NOT NULL, -- SAVING_RATE, EMERGENCY_FUND, GOAL_ADDITION, DEBT_REDUCTION, BUDGET_COMPLIANCE
    metric_target DECIMAL(15, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS user_challenges (
    user_challenge_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    challenge_id INT NOT NULL,
    progress DECIMAL(15, 2) DEFAULT 0,
    status VARCHAR(50) DEFAULT 'ACTIVE', -- ACTIVE, COMPLETED, FAILED
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES app_users(user_id),
    FOREIGN KEY (challenge_id) REFERENCES challenge_master(challenge_id)
);

-- Insert Default Master Challenges
INSERT INTO challenge_master (title, description, difficulty, reward_xp, challenge_type, metric_type, metric_target)
VALUES 
('Konsisten Menabung', 'Capai saving rate 20% bulan ini', 'Medium', 100, 'MONTHLY', 'SAVING_RATE', 0.20),
('Tambah Dana Darurat', 'Tambahkan Rp500.000 ke dana darurat', 'Hard', 200, 'MONTHLY', 'EMERGENCY_FUND', 500000),
('Mulai Berinvestasi', 'Sisihkan Rp100.000 untuk tujuan keuangan', 'Easy', 50, 'WEEKLY', 'GOAL_ADDITION', 100000),
('Tahan Belanja', 'Gunakan budget tidak lebih dari 90%', 'Medium', 150, 'MONTHLY', 'BUDGET_COMPLIANCE', 0.90),
('Kurangi Beban', 'Turunkan debt ratio sebanyak 1%', 'Hard', 300, 'MONTHLY', 'DEBT_REDUCTION', 0.01)
ON DUPLICATE KEY UPDATE title=title;
