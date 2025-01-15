-- Drop existing tables
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS recipes;
DROP TABLE IF EXISTS ingredients;
DROP TABLE IF EXISTS shopping_list;
DROP TABLE IF EXISTS favorites;

-- Create users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create recipes table
CREATE TABLE recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    prep_time INTEGER,
    servings INTEGER,
    instructions TEXT,
    tips TEXT,
    image_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Create ingredients table
CREATE TABLE ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    amount REAL,
    unit TEXT,
    description TEXT,
    category TEXT,
    FOREIGN KEY (recipe_id) REFERENCES recipes (id)
);

-- Create shopping_list table
CREATE TABLE shopping_list (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    recipe_id INTEGER NOT NULL,
    ingredient_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    checked BOOLEAN NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (recipe_id) REFERENCES recipes (id),
    FOREIGN KEY (ingredient_id) REFERENCES ingredients (id)
);

-- Create favorites table
CREATE TABLE favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    recipe_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (recipe_id) REFERENCES recipes (id),
    UNIQUE(user_id, recipe_id)
);

-- Insert admin user
INSERT INTO users (username, password, role) VALUES 
('admin', 'pbkdf2:sha256:260000$rMQd4vx8$7a4a413b3d1e37651f1a6e6271ef87f0f1f2c0296c31f825f91847676dce8a2a', 'admin');