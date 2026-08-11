CREATE DATABASE IF NOT EXISTS inventory;
USE inventory;

CREATE TABLE IF NOT EXISTS inventory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    stock INT NOT NULL,
    cp DECIMAL(12,2) NOT NULL,
    sp DECIMAL(12,2) NOT NULL,
    totalcp DECIMAL(14,2) NOT NULL,
    totalsp DECIMAL(14,2) NOT NULL,
    assumed_profit DECIMAL(14,2) NOT NULL,
    vendor VARCHAR(255),
    vendor_phoneno VARCHAR(50)
);

-- Login accounts are stored locally in users.json by the GUI.
-- This table is reserved for a future MySQL-backed authentication system.
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
