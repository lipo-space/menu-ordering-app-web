# Quick Start: Family Menu Ordering System

**Feature**: Family Menu Ordering System
**Branch**: 001-family-menu-system
**Estimated Time**: 2-3 weeks (single developer)

This guide provides a rapid onboarding reference for implementing the family menu ordering system. Follow these steps to get the development environment running and understand the key implementation patterns.

---

## Prerequisites

### Required Software
- **Node.js**: v18+ (LTS recommended)
- **Python**: v3.11+
- **PostgreSQL**: v15+ (via Supabase)
- **Git**: Latest version
- **VS Code**: Recommended with extensions:
  - Vue Language Features (Volar)
  - Python
  - Pylance
  - ESLint
  - Prettier

### External Services
- **Supabase Account**: Free tier sufficient for development
- **Vercel Account**: Free tier for deployment
- **GitHub Account**: For repository and CI/CD

---

## Initial Setup (30 minutes)

### 1. Clone and Setup Repository

```bash
# Navigate to project directory
cd /Users/lipo/zdx/menu/menu-web

# Install frontend dependencies
cd frontend
npm install

# Install backend dependencies
cd ../backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables

**Backend** (`backend/.env`):
```bash
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-role-key

# API Configuration
API_VERSION=v1
ENVIRONMENT=development

# CORS
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

**Frontend** (`frontend/.env`):
```bash
# API Configuration
VITE_API_BASE_URL=http://localhost:8000/api/v1

# Supabase (for future auth)
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
```

### 3. Setup Supabase Database

```bash
# Option 1: Use Supabase Dashboard
# 1. Go to supabase.com and create new project
# 2. Navigate to SQL Editor
# 3. Run migration from contracts/database-schema.yaml

# Option 2: Use Supabase CLI
npm install -g supabase
supabase login
supabase init
supabase db push
```

Copy the migration SQL from `specs/001-family-menu-system/contracts/database-schema.yaml` and execute it in Supabase.

### 4. Start Development Servers

**Terminal 1 - Backend**:
```bash
cd backend
source venv/bin/activate
uvicorn src.api:app --reload --port 8000
```

**Terminal 2 - Frontend**:
```bash
cd frontend
npm run dev
```

**Access**:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs (FastAPI auto-generated)

---

## Project Structure Overview

```
menu-web/
├── backend/                 # Python FastAPI backend
│   ├── src/
│   │   ├── api/            # API routes
│   │   │   ├── dishes.py   # Dish endpoints
│   │   │   ├── menus.py    # Menu endpoints
│   │   │   ├── combinations.py
│   │   │   └── history.py
│   │   ├── models/         # Pydantic models
│   │   ├── services/       # Business logic
│   │   └── db/             # Supabase client
│   └── tests/
│
├── frontend/               # Vue 3 frontend
│   ├── src/
│   │   ├── components/     # Vue components
│   │   │   ├── ui/         # Pixel art design system
│   │   │   ├── dishes/
│   │   │   ├── menus/
│   │   │   └── combinations/
│   │   ├── pages/          # Route pages
│   │   ├── services/       # API clients
│   │   ├── stores/         # Pinia stores
│   │   └── assets/         # Pixel art, styles
│   └── tests/
│
└── specs/                  # Feature documentation
    └── 001-family-menu-system/
        ├── spec.md         # Requirements
        ├── plan.md         # This plan
        ├── research.md     # Technical decisions
        ├── data-model.md   # Database schema
        └── contracts/      # API & DB contracts
```

---

## Implementation Sequence

Follow this order for smooth development:

### Phase 1: Foundation (Day 1-2)
1. ✅ **Database Setup**
   - Run migration SQL in Supabase
   - Verify tables created correctly
   - Test basic CRUD with Supabase dashboard

2. ✅ **Backend Core**
   - Setup FastAPI application structure
   - Implement Pydantic models (match data-model.md)
   - Create Supabase client connection
   - Basic error handling

3. ✅ **Frontend Core**
   - Setup Vue 3 + Vite project
   - Configure Vue Router
   - Setup Pinia stores
   - Create API service layer

### Phase 2: Design System (Day 3-4)
4. ✅ **Pixel Art Components**
   - Create base components: PixelButton, PixelCard, PixelModal, PixelInput
   - Define warm color palette CSS variables
   - Implement 60fps animations with CSS transforms
   - Test mobile responsiveness (375px+)

5. ✅ **Layout Components**
   - AppHeader, AppNavigation
   - PageContainer with proper padding
   - Mobile-optimized navigation

### Phase 3: Core Features (Day 5-10)
6. ✅ **Dish Management** (User Story 2)
   - Backend: GET/POST/PUT/DELETE `/api/v1/dishes`
   - Frontend: DishesPage, DishDetailPage
   - Store: dishStore with CRUD actions
   - Tests: Unit + Integration

7. ✅ **Menu Creation** (User Story 1 - MVP)
   - Backend: Menu endpoints with dish selection
   - Frontend: HomePage with today's menu
   - Menu creation flow with dish picker
   - Save to history with date
   - Tests: E2E with Playwright

8. ✅ **Dish Statistics** (User Story 3)
   - Backend: Track times_paired, times_enjoyed
   - Frontend: DishDetailPage with statistics display
   - Auto-increment on menu/combination save
   - Tests: Verify counts update correctly

### Phase 4: Enhanced Features (Day 11-14)
9. ✅ **Combinations** (User Story 4)
   - Backend: Combination CRUD endpoints
   - Frontend: CombinationsPage, creation flow
   - Use combinations in menu creation
   - Tests: Integration tests

10. ✅ **History View** (User Story 5)
    - Backend: History endpoint with date filter
    - Frontend: HistoryPage with date picker
    - Filter by date range
    - Tests: Date filtering logic

### Phase 5: Polish & Testing (Day 15-17)
11. ✅ **Performance Optimization**
    - Code splitting with dynamic imports
    - Lazy load images
    - Optimize bundle size (<500KB gzipped)
    - Verify 60fps animations
    - Test cold start <2s

12. ✅ **Testing & Quality**
    - Achieve >80% test coverage
    - E2E tests for critical paths
    - Accessibility audit (keyboard nav, screen reader)
    - Mobile testing (iOS Safari, Android Chrome)

13. ✅ **Documentation**
    - Update README with setup instructions
    - Document API endpoints (auto-generated by FastAPI)
    - Component documentation (optional: Storybook)

---

## Key Implementation Patterns

### 1. API Service Layer (Frontend)

```typescript
// frontend/src/services/dishService.ts
import { apiClient } from './api'
import type { Dish, CreateDish, UpdateDish } from '@/types'

export const dishService = {
  async getAll(search?: string): Promise<Dish[]> {
    const params = search ? { search } : {}
    const { data } = await apiClient.get('/dishes', { params })
    return data.data
  },

  async getById(id: string): Promise<Dish> {
    const { data } = await apiClient.get(`/dishes/${id}`)
    return data
  },

  async create(dish: CreateDish): Promise<Dish> {
    const { data } = await apiClient.post('/dishes', dish)
    return data
  },

  async update(id: string, dish: UpdateDish): Promise<Dish> {
    const { data } = await apiClient.put(`/dishes/${id}`, dish)
    return data
  },

  async delete(id: string): Promise<void> {
    await apiClient.delete(`/dishes/${id}`)
  }
}
```

### 2. Pinia Store Pattern

```typescript
// frontend/src/stores/dishStore.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { dishService } from '@/services/dishService'
import type { Dish } from '@/types'

export const useDishStore = defineStore('dishes', () => {
  const dishes = ref<Dish[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const dishCount = computed(() => dishes.value.length)

  async function fetchDishes(search?: string) {
    loading.value = true
    error.value = null
    try {
      dishes.value = await dishService.getAll(search)
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to load dishes'
    } finally {
      loading.value = false
    }
  }

  return { dishes, loading, error, dishCount, fetchDishes }
})
```

### 3. Pixel Art Component

```vue
<!-- frontend/src/components/ui/PixelButton.vue -->
<script setup lang="ts">
defineProps<{
  variant?: 'primary' | 'secondary'
  disabled?: boolean
}>()

defineEmits<{
  click: []
}>()
</script>

<template>
  <button
    class="pixel-button"
    :class="[`pixel-button--${variant}`, { 'pixel-button--disabled': disabled }]"
    :disabled="disabled"
    @click="$emit('click')"
  >
    <slot />
  </button>
</template>

<style scoped>
.pixel-button {
  padding: 12px 24px;
  border: 2px solid #1F2937;
  background: var(--color-amber-500);
  color: #1F2937;
  font-family: 'Press Start 2P', monospace;
  font-size: 14px;
  cursor: pointer;
  transition: transform 0.15s cubic-bezier(0.4, 0, 0.2, 1);
  will-change: transform;
}

.pixel-button:active:not(.pixel-button--disabled) {
  transform: scale(0.95);
}

.pixel-button--disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
```

### 4. FastAPI Endpoint

```python
# backend/src/api/dishes.py
from fastapi import APIRouter, HTTPException
from pydantic import UUID4
from src.models.dish import Dish, CreateDish, UpdateDish
from src.services.dish_service import DishService

router = APIRouter(prefix="/dishes", tags=["dishes"])
dish_service = DishService()

@router.get("/", response_model=dict)
async def list_dishes(search: str | None = None, limit: int = 50, offset: int = 0):
    dishes = await dish_service.get_all(search, limit, offset)
    return {
        "data": dishes,
        "meta": {"total": len(dishes), "limit": limit, "offset": offset}
    }

@router.post("/", response_model=Dish, status_code=201)
async def create_dish(dish: CreateDish):
    return await dish_service.create(dish)

@router.get("/{dish_id}", response_model=Dish)
async def get_dish(dish_id: UUID4):
    dish = await dish_service.get_by_id(dish_id)
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    return dish

@router.put("/{dish_id}", response_model=Dish)
async def update_dish(dish_id: UUID4, dish: UpdateDish):
    updated = await dish_service.update(dish_id, dish)
    if not updated:
        raise HTTPException(status_code=404, detail="Dish not found")
    return updated

@router.delete("/{dish_id}", status_code=204)
async def delete_dish(dish_id: UUID4):
    success = await dish_service.delete(dish_id)
    if not success:
        raise HTTPException(status_code=404, detail="Dish not found")
```

---

## Testing Strategy

### Unit Tests (Vitest)

```typescript
// frontend/tests/unit/dishStore.test.ts
import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useDishStore } from '@/stores/dishStore'

describe('DishStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('fetches dishes successfully', async () => {
    const store = useDishStore()
    await store.fetchDishes()
    expect(store.dishes.length).toBeGreaterThan(0)
    expect(store.loading).toBe(false)
  })
})
```

### E2E Tests (Playwright)

```typescript
// frontend/tests/e2e/menu-creation.spec.ts
import { test, expect } from '@playwright/test'

test('user can create a menu for today', async ({ page }) => {
  await page.goto('/')

  // Start menu creation
  await page.click('[data-testid="create-menu-btn"]')

  // Select dishes
  await page.click('[data-testid="dish-item"]:first-child')
  await page.click('[data-testid="dish-item"]:nth-child(2)')

  // Save menu
  await page.click('[data-testid="save-menu-btn"]')

  // Verify success
  await expect(page.locator('[data-testid="today-menu"]')).toBeVisible()
})
```

### Backend Tests (pytest)

```python
# backend/tests/api/test_dishes.py
import pytest
from httpx import AsyncClient
from src.api import app

@pytest.mark.asyncio
async def test_list_dishes():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/v1/dishes")
    assert response.status_code == 200
    assert "data" in response.json()

@pytest.mark.asyncio
async def test_create_dish():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/dishes",
            json={"name": "Test Dish", "description": "Test Description"}
        )
    assert response.status_code == 201
    assert response.json()["name"] == "Test Dish"
```

---

## Performance Checklist

Before deployment, verify:

- [ ] Bundle size <500KB gzipped
- [ ] Cold start <2 seconds on 4G
- [ ] All animations 60fps (no frame drops below 55fps)
- [ ] Lighthouse Performance score >90
- [ ] No layout shifts (CLS <0.1)
- [ ] First Contentful Paint <1.5s
- [ ] Time to Interactive <2s
- [ ] All images optimized (WebP with fallbacks)
- [ ] Lazy loading implemented for routes
- [ ] API responses <150ms (p95)

---

## Deployment

### Vercel Deployment

1. **Connect GitHub Repository**
   ```bash
   # Install Vercel CLI
   npm i -g vercel

   # Login and link project
   vercel login
   vercel link
   ```

2. **Configure Environment Variables**
   - Add all `.env` variables in Vercel dashboard
   - Set production-specific values

3. **Deploy**
   ```bash
   # Preview deployment
   vercel

   # Production deployment
   vercel --prod
   ```

### CI/CD Pipeline

GitHub Actions automatically:
1. Runs linting and type checking
2. Executes all tests (unit + e2e)
3. Checks bundle size budgets
4. Deploys to Vercel on main branch merge

---

## Troubleshooting

### Common Issues

**Issue**: Supabase connection fails
- **Solution**: Verify `SUPABASE_URL` and `SUPABASE_ANON_KEY` in `.env`
- **Solution**: Check Supabase project is running (not paused)

**Issue**: CORS errors in frontend
- **Solution**: Add `http://localhost:5173` to `ALLOWED_ORIGINS` in backend `.env`
- **Solution**: Restart backend server after `.env` changes

**Issue**: Animations not 60fps
- **Solution**: Use `will-change` CSS property sparingly
- **Solution**: Only animate `transform` and `opacity`
- **Solution**: Check for layout thrashing with Chrome DevTools Performance tab

**Issue**: Bundle size too large
- **Solution**: Analyze with `npm run build -- --mode analyze`
- **Solution**: Add more code splitting with dynamic imports
- **Solution**: Tree-shake unused dependencies

---

## Resources

### Documentation
- [Vue 3 Composition API](https://vuejs.org/guide/extras/composition-api-faq.html)
- [Pinia State Management](https://pinia.vuejs.org/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Supabase Docs](https://supabase.com/docs)
- [Vite Guide](https://vitejs.dev/guide/)

### Tools
- [Vue DevTools](https://devtools.vuejs.org/)
- [Supabase Dashboard](https://app.supabase.com/)
- [Vercel Dashboard](https://vercel.com/dashboard)

---

## Next Steps

1. Complete initial setup (30 min)
2. Review spec.md and data-model.md thoroughly
3. Start with Phase 1: Foundation
4. Follow implementation sequence
5. Run tests frequently
6. Refer to this quickstart for patterns

**Ready to start coding!** 🚀
