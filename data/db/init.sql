CREATE TABLE IF NOT EXISTS question_history (
    tracking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    problem_id INTEGER UNIQUE,
    correct_count INTEGER,
    fail_count INTEGER
);