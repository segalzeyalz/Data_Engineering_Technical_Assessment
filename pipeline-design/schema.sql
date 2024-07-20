-- schema.sql
-- SQL schema for the tasks table

CREATE TABLE IF NOT EXISTS tasks (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL,
    result TEXT,
    start_time TIMESTAMP,
    end_time TIMESTAMP
);
