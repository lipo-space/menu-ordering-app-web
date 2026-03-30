# Research & Technical Decisions: Family Menu Ordering System

**Feature**: Family Menu Ordering System
**Branch**: 001-family-menu-system
**Date**: 2026-03-30

## Overview

This document consolidates research findings and technical decisions for implementing a mobile-first family menu ordering web application with warm pixel art design, 60fps animations, and <2s cold start performance.

---

## Frontend Architecture

### Vue 3 Composition API Pattern

**Decision**: Use Vue 3 Composition API with `<script setup>` syntax exclusively

**Rationale**:
- Better TypeScript integration and type inference
- Improved code organization with composable functions
- Smaller bundle size (tree-shaking friendly)
- Easier testing of composition functions
- Aligns with Vue 3 best practices and future direction

**Alternatives Considered**:
- Options API: Rejected - larger bundle, weaker TypeScript support, harder to test
- Class-based (vue-class-component): Rejected - additional abstraction, not idiomatic Vue 3

**Implementation**:
```typescript
// Use <script setup> for all components
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

const dishes = ref<Dish[]>([])
const loading = ref(true)

onMounted(async () => {
  dishes.value = await dishService.getAll()
  loading.value = false
})
</script>
```

---

### State Management: Pinia

**Decision**: Use Pinia for global state management with modular stores

**Rationale**:
- Official Vue 3 state management (Vuex successor)
- Excellent TypeScript support with full type inference
- Simpler API than Vuex (no mutations)
- Better DevTools integration
- Smaller bundle size
- Modular store architecture scales well

**Store Structure**:
```typescript
// stores/dishStore.ts
export const useDishStore = defineStore('dishes', () => {
  const dishes = ref<Dish[]>([])
  const loading = ref(false)

  const dishCount = computed(() => dishes.value.length)

  async function fetchDishes() {
    loading.value = true
    dishes.value = await dishService.getAll()
    loading.value = false
  }

  return { dishes, loading, dishCount, fetchDishes }
})
```

**Alternatives Considered**:
- Vuex 4: Rejected - more verbose, weaker TypeScript support
- Reactive objects only: Rejected - no DevTools, harder debugging, no persistence
- Redux: Rejected - not idiomatic Vue, unnecessary complexity

---

### Pixel Art Design System

**Decision**: Custom pixel art component library using CSS + SVG

**Rationale**:
- Full control over warm, cute aesthetic
- SVG provides scalable, crisp pixel art at any resolution
- CSS animations enable 60fps performance
- No external emoji dependencies
- Consistent design language across all components

**Implementation Approach**:
1. **Pixel Art Components**: Create base components (PixelButton, PixelCard, PixelModal) with 2px border style
2. **Color Palette**: Define warm color tokens (amber-500, coral-400, peach-300, cream-100)
3. **Animations**: Use CSS transforms and `will-change` for GPU acceleration
4. **SVG Sprites**: Inline SVG for pixel art icons and decorations
5. **Responsive**: Scale pixel grid proportionally (8px base unit)

**Color Tokens**:
```css
:root {
  /* Warm Palette */
  --color-amber-500: #F59E0B;
  --color-coral-400: #F87171;
  --color-peach-300: #FBBF24;
  --color-cream-100: #FEF3C7;

  /* Pixel Art Style */
  --pixel-border: 2px solid #1F2937;
  --pixel-shadow: 4px 4px 0 rgba(0, 0, 0, 0.1);
  --pixel-radius: 0; /* Sharp corners for pixel aesthetic */
}
```

**Animation Performance**:
```css
.pixel-button {
  transition: transform 0.15s cubic-bezier(0.4, 0, 0.2, 1);
  will-change: transform;
}

.pixel-button:active {
  transform: scale(0.95);
}
```

**Alternatives Considered**:
- Emoji-based design: Rejected - requirement specifies no emoji
- Pre-built UI library (Vuetify, Quasar): Rejected - doesn't match pixel art aesthetic
- Canvas-based rendering: Rejected - unnecessary complexity, accessibility concerns

---

### Animation Strategy (60fps)

**Decision**: CSS-first animations with `requestAnimationFrame` for complex interactions

**Rationale**:
- CSS animations are hardware-accelerated (GPU)
- `transform` and `opacity` don't trigger layout/reflow
- 60fps achievable with proper optimization
- Simpler than JS-based animation libraries

**Performance Guidelines**:
1. **Only animate**: `transform`, `opacity` (GPU-accelerated)
2. **Avoid animating**: `width`, `height`, `margin`, `padding` (causes layout)
3. **Use `will-change`**: Hints browser to optimize (sparingly)
4. **Debounce scroll/resize**: Prevent excessive event firing
5. **Lazy load images**: Use `loading="lazy"` and Intersection Observer

**Bundle Optimization**:
- Vite code splitting by route
- Dynamic imports for heavy components
- Tree shaking for unused code
- Compress assets (gzip/brotli)

**Alternatives Considered**:
- GSAP: Rejected - adds ~45KB, CSS sufficient for needs
- Framer Motion: Rejected - React-specific, larger bundle
- Lottie animations: Considered for future - adds ~15KB for complex animations

---

## Backend Architecture

### FastAPI + Supabase Integration

**Decision**: FastAPI with Supabase Python client for database operations

**Rationale**:
- FastAPI: High performance, async support, automatic OpenAPI docs
- Supabase client: Direct integration with Supabase Auth, RLS, Realtime
- Pydantic: Built-in validation and serialization
- Type safety: End-to-end TypeScript (frontend) + Python type hints (backend)

**Architecture Pattern**:
```
Frontend (Vue 3)
    ↓ HTTP/JSON
FastAPI Backend
    ↓ Supabase Client
Supabase (PostgreSQL)
```

**Implementation**:
```python
# backend/src/db/supabase_client.py
from supabase import create_client, Client
from config import settings

supabase: Client = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_ANON_KEY
)

# backend/src/services/dish_service.py
from src.db.supabase_client import supabase

class DishService:
    async def get_all(self) -> list[Dish]:
        response = supabase.table('dishes').select('*').execute()
        return [Dish(**dish) for dish in response.data]
```

**Alternatives Considered**:
- SQLAlchemy ORM: Rejected - Supabase client more idiomatic, RLS support
- Direct PostgreSQL (psycopg2): Rejected - loses Supabase features (Auth, RLS, Realtime)
- Prisma: Rejected - Node.js-based, not Python

---

### Database Schema Design

**Decision**: PostgreSQL via Supabase with normalized schema and proper indexing

**Schema Structure**:

```sql
-- dishes table
CREATE TABLE dishes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  description TEXT,
  times_paired INTEGER DEFAULT 0,
  times_enjoyed INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_dishes_name ON dishes(name);

-- menus table
CREATE TABLE menus (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  date DATE NOT NULL UNIQUE,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_menus_date ON menus(date DESC);

-- menu_dishes junction table (many-to-many)
CREATE TABLE menu_dishes (
  menu_id UUID REFERENCES menus(id) ON DELETE CASCADE,
  dish_id UUID REFERENCES dishes(id) ON DELETE RESTRICT,
  PRIMARY KEY (menu_id, dish_id)
);

-- combinations table
CREATE TABLE combinations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- combination_dishes junction table
CREATE TABLE combination_dishes (
  combination_id UUID REFERENCES combinations(id) ON DELETE CASCADE,
  dish_id UUID REFERENCES dishes(id) ON DELETE RESTRICT,
  PRIMARY KEY (combination_id, dish_id)
);
```

**Indexing Strategy**:
- B-tree indexes on frequently queried columns (date, name)
- Composite indexes for common query patterns
- Foreign key indexes for join performance

**Alternatives Considered**:
- NoSQL (MongoDB): Rejected - relational data suits SQL, better consistency
- Single-table design: Rejected - poor scalability, data redundancy

---

### API Design (RESTful)

**Decision**: RESTful API with OpenAPI 3.0 documentation

**Endpoint Structure**:
```
GET    /api/v1/dishes              # List all dishes
POST   /api/v1/dishes              # Create dish
GET    /api/v1/dishes/:id          # Get dish details
PUT    /api/v1/dishes/:id          # Update dish
DELETE /api/v1/dishes/:id          # Delete dish

GET    /api/v1/menus               # List menus (with date filter)
POST   /api/v1/menus               # Create menu
GET    /api/v1/menus/:date         # Get menu by date
PUT    /api/v1/menus/:date         # Update menu
DELETE /api/v1/menus/:date         # Delete menu

GET    /api/v1/combinations        # List combinations
POST   /api/v1/combinations        # Create combination
GET    /api/v1/combinations/:id    # Get combination
PUT    /api/v1/combinations/:id    # Update combination
DELETE /api/v1/combinations/:id    # Delete combination

GET    /api/v1/history             # Get menu history (date range filter)
```

**Response Format**:
```json
{
  "data": [...],
  "meta": {
    "total": 100,
    "page": 1,
    "per_page": 20
  }
}
```

**Error Handling**:
```json
{
  "error": {
    "code": "DISH_NOT_FOUND",
    "message": "Dish with ID xyz not found",
    "details": {}
  }
}
```

**Alternatives Considered**:
- GraphQL: Rejected - overkill for simple CRUD, adds complexity
- gRPC: Rejected - not suitable for web browsers, requires HTTP/2

---

## Performance Optimization

### Cold Start <2 Seconds

**Decision**: Multi-layered optimization strategy

**Strategies**:
1. **Code Splitting**: Route-based lazy loading
   ```typescript
   const routes = [
     { path: '/', component: () => import('@/pages/HomePage.vue') }
   ]
   ```

2. **Bundle Size Budgets**:
   - Initial bundle: <200KB gzipped
   - Per-route chunk: <50KB gzipped
   - Total: <500KB gzipped

3. **Asset Optimization**:
   - SVG sprites for pixel art (inlined)
   - WebP for any photos (with fallback)
   - Font subsetting (only used characters)

4. **Critical CSS**: Inline above-fold styles
   ```typescript
   // vite.config.ts
   build: {
     cssCodeSplit: true,
     rollupOptions: {
       output: {
         manualChunks: {
           'vendor': ['vue', 'pinia', 'vue-router']
         }
       }
     }
   }
   ```

5. **Preconnect**: Hints for external resources
   ```html
   <link rel="preconnect" href="https://api.example.com">
   <link rel="dns-prefetch" href="https://supabase.io">
   ```

**Alternatives Considered**:
- SSR (Nuxt): Rejected - adds complexity, not needed for v1
- Service Worker caching: Deferred to v2 - adds complexity

---

### 60fps Animation Techniques

**Decision**: GPU-accelerated CSS animations with performance monitoring

**Techniques**:
1. **Use GPU-accelerated properties only**:
   - `transform: translate, scale, rotate`
   - `opacity`

2. **Avoid layout thrashing**:
   - Batch DOM reads/writes
   - Use `requestAnimationFrame` for JS animations

3. **Optimize rendering**:
   ```css
   .animate-element {
     will-change: transform;
     transform: translateZ(0); /* Force GPU layer */
   }
   ```

4. **Performance monitoring**:
   ```typescript
   // Track frame drops
   const fps = useFpsMonitor()
   if (fps.current < 55) {
     console.warn('Frame drop detected')
   }
   ```

**Alternatives Considered**:
- WebGL: Rejected - overkill for 2D UI animations
- Canvas: Rejected - DOM accessibility concerns

---

## Testing Strategy

### Frontend Testing

**Decision**: Vitest (unit) + Playwright (e2e)

**Unit Tests** (Vitest):
- Component mounting and rendering
- Store actions and computed properties
- Service layer API calls (mocked)
- Target: >80% code coverage

**E2E Tests** (Playwright):
- Critical user journeys (P1 stories)
- Menu creation flow
- Dish management flow
- Mobile viewport testing (375px, 414px, 768px)

**Alternatives Considered**:
- Jest: Rejected - Vitest faster, better Vite integration
- Cypress: Rejected - Playwright faster, better multi-browser

---

### Backend Testing

**Decision**: pytest with async support

**Test Types**:
- **Unit tests**: Service layer logic (mocked database)
- **Integration tests**: API endpoints with test database
- **Contract tests**: Verify API schema compliance

**Test Database**: Separate Supabase project for testing

**Alternatives Considered**:
- unittest: Rejected - pytest more Pythonic, better fixtures
- nose2: Rejected - less popular, smaller ecosystem

---

## Deployment & CI/CD

### Vercel Deployment

**Decision**: Monorepo deployment with Vercel

**Configuration**:
```json
// vercel.json (root)
{
  "version": 2,
  "builds": [
    { "src": "backend/**/*.py", "use": "@vercel/python" },
    { "src": "frontend/package.json", "use": "@vercel/static-build" }
  ],
  "routes": [
    { "src": "/api/(.*)", "dest": "backend/src/api/$1" },
    { "src": "/(.*)", "dest": "frontend/$1" }
  ]
}
```

**Environment Variables**:
- `SUPABASE_URL`: Supabase project URL
- `SUPABASE_ANON_KEY`: Supabase anonymous key
- `SUPABASE_SERVICE_KEY`: Supabase service role key (backend only)

**Alternatives Considered**:
- Separate repos: Rejected - harder to coordinate deployments
- Docker containers: Rejected - Vercel simpler for serverless

---

### GitHub Actions CI/CD

**Decision**: Automated testing and deployment pipeline

**Workflow**:
```yaml
name: CI/CD
on: [push, pull_request]

jobs:
  test-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: cd frontend && npm ci
      - run: npm run lint
      - run: npm run type-check
      - run: npm run test:unit
      - run: npm run build

  test-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: cd backend && pip install -r requirements.txt
      - run: pytest

  deploy:
    needs: [test-frontend, test-backend]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: amondnet/vercel-action@v20
```

**Alternatives Considered**:
- Travis CI: Rejected - GitHub Actions better integrated
- CircleCI: Rejected - GitHub Actions free tier better

---

## Security Considerations

### Row-Level Security (RLS)

**Decision**: Enable Supabase RLS for data isolation

**Implementation**:
```sql
-- Enable RLS on all tables
ALTER TABLE dishes ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see their own family's data
CREATE POLICY "Users can view own dishes"
  ON dishes FOR SELECT
  USING (family_id = auth.uid());
```

**Alternatives Considered**:
- Application-level security: Rejected - RLS more robust, defense in depth

---

## Summary

All technical decisions align with constitution principles:
- ✅ **UX Excellence**: Pixel art design system, 60fps animations, mobile-first
- ✅ **Performance**: <2s cold start, optimized bundles, GPU-accelerated animations
- ✅ **Component Architecture**: Vue 3 Composition API, TypeScript, modular design
- ✅ **Quality Assurance**: Vitest + Playwright + pytest, >80% coverage, CI/CD gates
- ✅ **API-First**: RESTful FastAPI, OpenAPI docs, Pydantic validation

No technical blockers remain. Ready to proceed with Phase 1 design artifacts.
