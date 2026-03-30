# Data Model: Family Menu Ordering System

**Feature**: Family Menu Ordering System
**Branch**: 001-family-menu-system
**Date**: 2026-03-30

## Overview

This document defines the data entities, relationships, and validation rules for the family menu ordering system. The model supports dish management, menu creation, combinations, and historical tracking with proper referential integrity.

---

## Entity Relationship Diagram

```
┌─────────────┐
│   dishes    │
├─────────────┤
│ id (PK)     │◄───────┐
│ name        │        │
│ description │        │
│ times_paired│        │
│ times_enjoyed│       │
│ created_at  │        │
│ updated_at  │        │
└─────────────┘        │
                       │
┌─────────────┐        │        ┌──────────────────┐
│   menus     │        │        │  combinations    │
├─────────────┤        │        ├──────────────────┤
│ id (PK)     │        │        │ id (PK)          │
│ date (UK)   │        │        │ name             │
│ created_at  │        │        │ created_at       │
└─────────────┘        │        └──────────────────┘
       │               │                │
       │               │                │
       ▼               │                ▼
┌──────────────────┐   │        ┌────────────────────┐
│  menu_dishes     │   │        │ combination_dishes │
├──────────────────┤   │        ├────────────────────┤
│ menu_id (PK,FK)  │   │        │ combination_id (PK,FK) │
│ dish_id (PK,FK)  │───┘        │ dish_id (PK,FK)    │───┘
└──────────────────┘            └────────────────────┘

UK = Unique Key
PK = Primary Key
FK = Foreign Key
```

---

## Core Entities

### 1. Dish (菜品)

Represents a single food item in the menu library.

**Table**: `dishes`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Unique identifier |
| `name` | TEXT | NOT NULL, CHECK (length(name) >= 1 AND length(name) <= 100) | Dish name (1-100 chars) |
| `description` | TEXT | NULLABLE, CHECK (length(description) <= 500) | Optional description (max 500 chars) |
| `times_paired` | INTEGER | NOT NULL, DEFAULT 0, CHECK (times_paired >= 0) | Number of combinations containing this dish |
| `times_enjoyed` | INTEGER | NOT NULL, DEFAULT 0, CHECK (times_enjoyed >= 0) | Total times this dish appeared in menus |
| `created_at` | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | Creation timestamp |
| `updated_at` | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Indexes**:
- `idx_dishes_name` on `name` (for search/filter performance)
- `idx_dishes_created_at` on `created_at DESC` (for recent dishes queries)

**Validation Rules**:
- `name` is required and must be 1-100 characters
- `description` is optional but max 500 characters if provided
- `times_paired` and `times_enjoyed` auto-increment, cannot be negative
- `updated_at` auto-updates on any modification

**Business Logic**:
- When dish is added to a combination: increment `times_paired`
- When dish is added to a menu: increment `times_enjoyed`
- Dish deletion: Restrict if dish exists in historical menus (preserve history)
- Dish deletion: Cascade remove from combinations and future menus

---

### 2. Menu (菜单)

A collection of dishes selected for a specific date.

**Table**: `menus`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Unique identifier |
| `date` | DATE | NOT NULL, UNIQUE | Menu date (one menu per date) |
| `created_at` | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | Creation timestamp |

**Indexes**:
- `idx_menus_date` on `date DESC` (for history queries)
- UNIQUE constraint on `date` ensures one menu per date

**Validation Rules**:
- `date` is required and must be unique
- Only one menu allowed per date
- Date can be past, present, or future (no restriction)

**Business Logic**:
- Creating menu for existing date: Update existing menu (replace dishes)
- Deleting menu: Cascade delete all menu_dishes entries
- Historical preservation: Menu data retained even if dishes deleted

---

### 3. Menu-Dish Junction (menu_dishes)

Many-to-many relationship between menus and dishes.

**Table**: `menu_dishes`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `menu_id` | UUID | PRIMARY KEY, FOREIGN KEY REFERENCES menus(id) ON DELETE CASCADE | Menu reference |
| `dish_id` | UUID | PRIMARY KEY, FOREIGN KEY REFERENCES dishes(id) ON DELETE RESTRICT | Dish reference |

**Composite Primary Key**: `(menu_id, dish_id)`

**Indexes**:
- Composite index on `(menu_id, dish_id)` (primary key)
- Index on `dish_id` for reverse lookups

**Validation Rules**:
- Same dish can appear multiple times in same menu (for portion tracking if needed)
- Deletion: Cascade when menu deleted, Restrict when dish deleted

**Business Logic**:
- Adding dish to menu: Automatically increment `dish.times_enjoyed`
- Removing dish from menu: Decrement `dish.times_enjoyed` (if menu not historical)
- Bulk operations supported for menu creation

---

### 4. Combination (搭配)

A saved collection of dishes for quick menu creation.

**Table**: `combinations`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Unique identifier |
| `name` | TEXT | NOT NULL, CHECK (length(name) >= 1 AND length(name) <= 100) | Combination name (1-100 chars) |
| `created_at` | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | Creation timestamp |

**Indexes**:
- `idx_combinations_name` on `name` (for search performance)
- `idx_combinations_created_at` on `created_at DESC` (for recent combinations)

**Validation Rules**:
- `name` is required and must be 1-100 characters
- Name should be unique per family (enforced at application level initially)

**Business Logic**:
- Combination can be empty (no dishes)
- Deleting combination: Cascade delete all combination_dishes entries
- Combination deletion doesn't affect historical menus

---

### 5. Combination-Dish Junction (combination_dishes)

Many-to-many relationship between combinations and dishes.

**Table**: `combination_dishes`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `combination_id` | UUID | PRIMARY KEY, FOREIGN KEY REFERENCES combinations(id) ON DELETE CASCADE | Combination reference |
| `dish_id` | UUID | PRIMARY KEY, FOREIGN KEY REFERENCES dishes(id) ON DELETE RESTRICT | Dish reference |

**Composite Primary Key**: `(combination_id, dish_id)`

**Indexes**:
- Composite index on `(combination_id, dish_id)` (primary key)
- Index on `dish_id` for reverse lookups (times_paired queries)

**Validation Rules**:
- Same dish can only appear once per combination
- Minimum 1 dish required to create combination (enforced at application level)

**Business Logic**:
- Adding dish to combination: Automatically increment `dish.times_paired`
- Removing dish from combination: Decrement `dish.times_paired`
- Bulk operations supported for combination creation

---

## Data Relationships

### Relationships Summary

1. **Menu ↔ Dishes** (Many-to-Many)
   - A menu contains multiple dishes
   - A dish can appear in multiple menus (different dates)
   - Junction table: `menu_dishes`
   - Cascade: Menu delete removes junction entries
   - Restrict: Dish delete blocked if in historical menus

2. **Combination ↔ Dishes** (Many-to-Many)
   - A combination contains multiple dishes
   - A dish can appear in multiple combinations
   - Junction table: `combination_dishes`
   - Cascade: Combination delete removes junction entries
   - Restrict: Dish delete blocked if in combinations

3. **Dish Statistics** (Derived)
   - `times_paired`: Count of entries in `combination_dishes` for this dish
   - `times_enjoyed`: Count of entries in `menu_dishes` for this dish
   - Automatically maintained via triggers or application logic

---

## State Transitions

### Dish Lifecycle

```
[Created] → [Active] → [Deleted]
              ↓
         [In Use]
         (in combinations/menus)
```

**States**:
- **Created**: Dish exists in library, not used anywhere
- **Active**: Dish exists and is used in combinations or menus
- **Deleted**: Dish removed from library (soft delete or hard delete with restrictions)

**Transitions**:
- Created → Active: Add dish to combination or menu
- Active → Deleted: Remove dish (restrict if in historical menus)

---

### Menu Lifecycle

```
[Empty] → [Draft] → [Saved] → [Historical]
                        ↓
                    [Updated]
```

**States**:
- **Empty**: No menu for the date
- **Draft**: Menu being created (frontend-only state)
- **Saved**: Menu persisted to database
- **Historical**: Menu date is in the past (read-only)
- **Updated**: Saved menu modified

**Transitions**:
- Empty → Draft: User starts creating menu
- Draft → Saved: User saves menu
- Saved → Updated: User modifies saved menu (today or future)
- Saved → Historical: Date passes (automatic, no state change in DB)

---

### Combination Lifecycle

```
[Created] → [Active] → [Deleted]
```

**States**:
- **Created**: Combination exists, may or may not have dishes
- **Active**: Combination has dishes and can be used
- **Deleted**: Combination removed

**Transitions**:
- Created → Active: Add dishes to combination
- Active → Deleted: User deletes combination

---

## Data Constraints & Invariants

### Business Rules

1. **One Menu Per Date**: UNIQUE constraint on `menus.date`
2. **Dish Statistics Accuracy**: `times_paired` and `times_enjoyed` must match junction table counts
3. **Referential Integrity**:
   - Cannot delete dish if referenced in `menu_dishes` (RESTRICT)
   - Cannot delete dish if referenced in `combination_dishes` (RESTRICT)
   - Deleting menu cascades to `menu_dishes`
   - Deleting combination cascades to `combination_dishes`
4. **Data Preservation**: Historical menus retain dish names even if dish deleted (soft delete or archive strategy)

### Data Quality Rules

1. **Required Fields**:
   - Dish: `name`
   - Menu: `date`
   - Combination: `name`

2. **Length Limits**:
   - Dish name: 1-100 characters
   - Dish description: max 500 characters
   - Combination name: 1-100 characters

3. **Numeric Constraints**:
   - `times_paired` >= 0
   - `times_enjoyed` >= 0

4. **Uniqueness**:
   - Menu date must be unique (one menu per day)
   - Combination names should be unique per family (application-level check)

---

## Performance Considerations

### Query Patterns

**Frequent Queries**:
1. Get all dishes (with optional search/filter)
   - Optimized by: `idx_dishes_name`
2. Get menu by date
   - Optimized by: `idx_menus_date`
3. Get dishes in a menu
   - Optimized by: Composite PK on `menu_dishes`
4. Get dishes in a combination
   - Optimized by: Composite PK on `combination_dishes`
5. Get menu history (date range)
   - Optimized by: `idx_menus_date DESC`

**Index Strategy**:
- B-tree indexes on all foreign keys
- B-tree indexes on frequently filtered columns (name, date)
- Composite indexes for junction tables
- Descending indexes for chronological queries

---

## Migration Strategy

### Initial Migration

```sql
-- Create tables in dependency order
CREATE TABLE dishes (...);
CREATE TABLE menus (...);
CREATE TABLE menu_dishes (...);
CREATE TABLE combinations (...);
CREATE TABLE combination_dishes (...);

-- Create indexes
CREATE INDEX idx_dishes_name ON dishes(name);
CREATE INDEX idx_menus_date ON menus(date DESC);
-- ... other indexes

-- Create triggers for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_dishes_updated_at BEFORE UPDATE ON dishes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

### Future Migrations

- Use Supabase migrations system
- Version control all schema changes
- Test migrations on staging environment first
- Ensure backward compatibility for API clients

---

## Summary

The data model supports all feature requirements:
- ✅ Dish management with statistics tracking
- ✅ Daily menu creation with date uniqueness
- ✅ Combinations for quick menu creation
- ✅ Historical menu preservation
- ✅ Referential integrity and data consistency
- ✅ Performance optimization through proper indexing

All entities have clear validation rules, state transitions, and relationships defined. Ready for implementation.
