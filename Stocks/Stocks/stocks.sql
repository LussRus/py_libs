CREATE TABLE IF NOT EXISTS tech_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    btm_lev TEXT,
    top_lev TEXT,
    deviation_percent TEXT
);

CREATE TABLE IF NOT EXISTS stock_list (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT NOT NULL,
    full_name TEXT NOT NULL,
    industry TEXT,
    sector TEXT
);
