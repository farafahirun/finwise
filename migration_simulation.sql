CREATE TABLE IF NOT EXISTS simulation_history (
    sim_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    scenario_name VARCHAR(100) NOT NULL,
    inc_change_pct DECIMAL(5,2) DEFAULT 0,
    exp_change_pct DECIMAL(5,2) DEFAULT 0,
    debt_reduction_amt DECIMAL(15,2) DEFAULT 0,
    goal_boost_amt DECIMAL(15,2) DEFAULT 0,
    sim_health_score DECIMAL(5,2) DEFAULT 0,
    sim_saving_rate DECIMAL(5,2) DEFAULT 0,
    sim_debt_ratio DECIMAL(5,2) DEFAULT 0,
    sim_goal_completion_months INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES app_users(user_id)
);
