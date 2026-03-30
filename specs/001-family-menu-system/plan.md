# Implementation Plan: Family Menu Ordering System

**Branch**: `001-family-menu-system` | **Date**: 2026-03-30 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-family-menu-system/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Build a mobile-first family menu ordering web application with warm, cute pixel art design. The system enables families to create daily menus by selecting dishes from a personal library or pre-made combinations, track meal history, and view statistics on family preferences. Core functionality includes dish management (CRUD), combination management, daily menu creation, and historical menu viewing with date filtering. All interactions must maintain 60fps performance with <2s cold start time.

## Technical Context

**Language/Version**: Vue 3 (Composition API) + TypeScript 5.x (frontend), Python 3.11+ (backend)
**Primary Dependencies**: Vue 3, Pinia (state), Vite (build), FastAPI, Supabase Python Client
**Storage**: Supabase (PostgreSQL database with real-time subscriptions)
**Testing**: Vitest (unit), Playwright (e2e) for frontend; pytest (backend)
**Target Platform**: Progressive Web App (mobile-first, responsive from 320px to 1920px)
**Project Type**: web-application (monorepo with backend/ and frontend/ directories)
**Performance Goals**: 60fps animations (min 55fps), <2s cold start on 4G, <500KB initial bundle gzipped
**Constraints**: <200ms API response (p95), offline not required v1, single family account v1
**Scale/Scope**: 500+ dishes supported, personal/family use (not multi-tenant), 5 main pages

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: User Experience Excellence (NON-NEGOTIABLE)
- ✅ **PASS**: All UI will use warm pixel art design system
- ✅ **PASS**: Animation budget enforced (60fps, <2s cold start)
- ✅ **PASS**: Mobile-first responsive design (320px-1920px)
- ✅ **PASS**: Immediate visual feedback (<16ms interaction response)
- **Implementation**: Use CSS transforms/animations, lazy loading, optimized assets

### Principle II: Performance Standards (NON-NEGOTIABLE)
- ✅ **PASS**: Bundle size <500KB gzipped (Vite code splitting, tree shaking)
- ✅ **PASS**: Time to Interactive <2s (critical path optimization, lazy routes)
- ✅ **PASS**: Animation 60fps minimum (CSS hardware acceleration, requestAnimationFrame)
- ✅ **PASS**: API <150ms p95 (FastAPI async, Supabase connection pooling)
- ✅ **PASS**: Database queries <200ms p95 (indexed queries, optimized joins)
- **Implementation**: Performance budgets in CI/CD, Lighthouse CI, bundle analyzers

### Principle III: Component-Based Architecture
- ✅ **PASS**: Vue 3 Composition API with single-responsibility components
- ✅ **PASS**: TypeScript for type safety across all components
- ✅ **PASS**: Shared UI components in design system library (`frontend/src/components/ui/`)
- ✅ **PASS**: Well-documented props/events, independently testable
- **Implementation**: Component library structure, Storybook for documentation (optional)

### Principle IV: Automated Quality Assurance (NON-NEGOTIABLE)
- ✅ **PASS**: Unit tests with >80% coverage (Vitest + pytest)
- ✅ **PASS**: E2E tests for critical user journeys (Playwright)
- ✅ **PASS**: ESLint + Pylint/Black linting in pre-commit and CI
- ✅ **PASS**: TypeScript + mypy type checking
- ✅ **PASS**: Security scans (npm audit, safety check)
- ✅ **PASS**: Performance tests (60fps, <2s cold start)
- **Implementation**: GitHub Actions CI pipeline with all quality gates

### Principle V: API-First Design
- ✅ **PASS**: OpenAPI/Swagger documentation for all endpoints
- ✅ **PASS**: Semantic versioning (v1) with backward compatibility
- ✅ **PASS**: Request/response schema validation (Pydantic)
- ✅ **PASS**: Frontend accesses only through Python API (no direct Supabase from frontend)
- **Implementation**: FastAPI auto-generated OpenAPI docs, Pydantic models

**Gate Status**: ✅ ALL PRINCIPLES PASS - No violations, proceed to research

## Project Structure

### Documentation (this feature)

```text
specs/001-family-menu-system/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
│   ├── api-endpoints.yaml    # REST API contract
│   └── database-schema.yaml  # Supabase schema
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/           # Pydantic models + SQLAlchemy/Supabase schemas
│   │   ├── dish.py
│   │   ├── menu.py
│   │   ├── combination.py
│   │   └── history.py
│   ├── services/         # Business logic layer
│   │   ├── dish_service.py
│   │   ├── menu_service.py
│   │   ├── combination_service.py
│   │   └── history_service.py
│   ├── api/              # FastAPI routes and endpoints
│   │   ├── __init__.py
│   │   ├── dishes.py
│   │   ├── menus.py
│   │   ├── combinations.py
│   │   └── history.py
│   ├── db/               # Database connection and utilities
│   │   ├── __init__.py
│   │   ├── supabase_client.py
│   │   └── migrations/
│   └── config.py         # Environment configuration
├── tests/
│   ├── unit/
│   ├── integration/
│   └── conftest.py
├── requirements.txt
├── pyproject.toml
└── vercel.json           # Vercel serverless configuration

frontend/
├── src/
│   ├── components/       # Vue 3 components
│   │   ├── ui/           # Design system (pixel art components)
│   │   │   ├── PixelButton.vue
│   │   │   ├── PixelCard.vue
│   │   │   ├── PixelModal.vue
│   │   │   └── PixelInput.vue
│   │   ├── dishes/       # Dish management components
│   │   ├── menus/        # Menu creation components
│   │   ├── combinations/ # Combination components
│   │   └── history/      # History view components
│   ├── pages/            # Page-level components (routes)
│   │   ├── HomePage.vue
│   │   ├── DishesPage.vue
│   │   ├── DishDetailPage.vue
│   │   ├── CombinationsPage.vue
│   │   └── HistoryPage.vue
│   ├── services/         # API client services
│   │   ├── api.ts
│   │   ├── dishService.ts
│   │   ├── menuService.ts
│   │   ├── combinationService.ts
│   │   └── historyService.ts
│   ├── stores/           # Pinia stores
│   │   ├── dishStore.ts
│   │   ├── menuStore.ts
│   │   ├── combinationStore.ts
│   │   └── historyStore.ts
│   ├── assets/           # Pixel art assets, SVGs, animations
│   │   ├── sprites/
│   │   ├── animations/
│   │   └── styles/
│   ├── router/           # Vue Router configuration
│   │   └── index.ts
│   ├── App.vue
│   └── main.ts
├── tests/
│   ├── unit/
│   └── e2e/
├── public/
├── package.json
├── vite.config.ts
├── tsconfig.json
└── vercel.json           # Vercel static deployment config

.specify/
├── memory/
│   └── constitution.md
└── templates/
```

**Structure Decision**: Web application structure with separate backend (FastAPI) and frontend (Vue 3) directories. This separation enables:
- Independent deployment (backend as Vercel serverless functions, frontend as static assets)
- Clear API contract between layers
- Separate testing and CI/CD pipelines
- Technology-specific tooling optimization

The backend exposes RESTful APIs that the frontend consumes. All database access goes through the Python backend layer (Principle V compliance).

## Complexity Tracking

> **No violations** - All constitution principles pass without requiring justification.

