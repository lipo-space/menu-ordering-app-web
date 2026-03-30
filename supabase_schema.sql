-- ============================================
-- Family Menu Web App - Supabase Database Schema
-- ============================================
-- Run this SQL in Supabase Dashboard > SQL Editor
-- ============================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Auto-update updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- ============================================
-- DISHES TABLE
-- ============================================
CREATE TABLE dishes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL CHECK (length(name) >= 1 AND length(name) <= 100),
    description TEXT CHECK (description IS NULL OR length(description) <= 500),
    times_paired INTEGER NOT NULL DEFAULT 0 CHECK (times_paired >= 0),
    times_enjoyed INTEGER NOT NULL DEFAULT 0 CHECK (times_enjoyed >= 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_dishes_name ON dishes(name);
CREATE INDEX idx_dishes_created_at ON dishes(created_at DESC);

CREATE TRIGGER update_dishes_updated_at BEFORE UPDATE ON dishes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- MENUS TABLE
-- ============================================
CREATE TABLE menus (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    date DATE NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_menus_date ON menus(date DESC);

-- ============================================
-- MENU_DISHES JOIN TABLE
-- ============================================
CREATE TABLE menu_dishes (
    menu_id UUID NOT NULL REFERENCES menus(id) ON DELETE CASCADE,
    dish_id UUID NOT NULL REFERENCES dishes(id) ON DELETE RESTRICT,
    PRIMARY KEY (menu_id, dish_id)
);

CREATE INDEX idx_menu_dishes_dish_id ON menu_dishes(dish_id);

-- ============================================
-- COMBINATIONS TABLE
-- ============================================
CREATE TABLE combinations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL CHECK (length(name) >= 1 AND length(name) <= 100),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_combinations_name ON combinations(name);
CREATE INDEX idx_combinations_created_at ON combinations(created_at DESC);

-- ============================================
-- COMBINATION_DISHES JOIN TABLE
-- ============================================
CREATE TABLE combination_dishes (
    combination_id UUID NOT NULL REFERENCES combinations(id) ON DELETE CASCADE,
    dish_id UUID NOT NULL REFERENCES dishes(id) ON DELETE RESTRICT,
    PRIMARY KEY (combination_id, dish_id)
);

CREATE INDEX idx_combination_dishes_dish_id ON combination_dishes(dish_id);

-- ============================================
-- DONE! Tables created successfully
-- ============================================
