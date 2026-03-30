# Tasks: Family Menu Ordering System

**Input**: Design documents from `/specs/001-family-menu-system/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are OPTIONAL - included as recommended tasks for quality assurance but can be skipped if rapid prototyping is preferred.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- Paths shown below follow the monorepo structure defined in plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan
- [X] T002 Initialize frontend Vue 3 project with Vite and TypeScript in frontend/
- [X] T003 [P] Initialize backend Python project with FastAPI in backend/
- [X] T004 [P] Setup Supabase project and configure environment variables
- [X] T005 [P] Configure ESLint and Prettier for frontend
- [X] T006 [P] Configure Pylint and Black for backend
- [X] T007 [P] Setup Vue Router with basic route structure in frontend/src/router/index.ts
- [X] T008 [P] Configure Vite with code splitting and optimization settings in frontend/vite.config.ts

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T009 Setup Supabase database schema using migration SQL from contracts/database-schema.yaml
- [ ] T010 [P] Create Supabase client connection module in backend/src/db/supabase_client.py
- [ ] T011 [P] Create Pydantic base models for Dish, Menu, Combination in backend/src/models/
- [ ] T012 [P] Setup FastAPI application with CORS middleware in backend/src/api/__init__.py
- [ ] T013 [P] Create API client base with axios/fetch in frontend/src/services/api.ts
- [ ] T014 [P] Create Pinia store base structure in frontend/src/stores/
- [ ] T015 [P] Create pixel art design system color tokens in frontend/src/assets/styles/tokens.css
- [ ] T016 [P] Create PixelButton component in frontend/src/components/ui/PixelButton.vue
- [ ] T017 [P] Create PixelCard component in frontend/src/components/ui/PixelCard.vue
- [ ] T018 [P] Create PixelInput component in frontend/src/components/ui/PixelInput.vue
- [ ] T019 [P] Create PixelModal component in frontend/src/components/ui/PixelModal.vue
- [ ] T020 Create AppHeader component with navigation in frontend/src/components/AppHeader.vue
- [ ] T021 Create AppNavigation component with mobile menu in frontend/src/components/AppNavigation.vue
- [ ] T022 Create PageContainer layout component in frontend/src/components/PageContainer.vue

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create Today's Menu (Priority: P1) 🎯 MVP

**Goal**: Enable users to create daily menus by selecting dishes from the library or combinations

**Independent Test**: Create a new menu from scratch, select dishes, save with today's date, verify it appears on home page

### Recommended Tests for User Story 1 (OPTIONAL)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T023 [P] [US1] Integration test for menu creation flow in backend/tests/integration/test_menus.py
- [ ] T024 [P] [US1] E2E test for today's menu creation in frontend/tests/e2e/menu-creation.spec.ts

### Backend Implementation for User Story 1

- [ ] T025 [P] [US1] Create Menu Pydantic model with validation in backend/src/models/menu.py
- [ ] T026 [P] [US1] Create MenuDish junction model in backend/src/models/menu_dish.py
- [ ] T027 [US1] Implement MenuService with create, read, update methods in backend/src/services/menu_service.py
- [ ] T028 [US1] Implement menu statistics auto-increment logic in backend/src/services/menu_service.py
- [ ] T029 [US1] Create menu API endpoints (GET /menus, POST /menus, GET /menus/:date, PUT /menus/:date) in backend/src/api/menus.py
- [ ] T030 [US1] Add error handling and validation for menu operations in backend/src/api/menus.py

### Frontend Implementation for User Story 1

- [ ] T031 [P] [US1] Create menuService API client in frontend/src/services/menuService.ts
- [ ] T032 [P] [US1] Create menuStore with Pinia in frontend/src/stores/menuStore.ts
- [ ] T033 [P] [US1] Create HomePage component showing today's menu in frontend/src/pages/HomePage.vue
- [ ] T034 [P] [US1] Create MenuCreationModal component in frontend/src/components/menus/MenuCreationModal.vue
- [ ] T035 [P] [US1] Create DishSelector component for browsing and selecting dishes in frontend/src/components/menus/DishSelector.vue
- [ ] T036 [P] [US1] Create SelectedDishesList component in frontend/src/components/menus/SelectedDishesList.vue
- [ ] T037 [US1] Integrate menu creation flow in HomePage with smooth animations
- [ ] T038 [US1] Add empty state for no menu today in frontend/src/pages/HomePage.vue
- [ ] T039 [US1] Implement menu save with today's date and success feedback

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. Users can create daily menus.

---

## Phase 4: User Story 2 - Manage Dishes (Priority: P2)

**Goal**: Enable users to add, edit, view, and delete dishes in the menu library

**Independent Test**: Create a new dish, view it in library, edit details, delete it, verify CRUD operations work

### Recommended Tests for User Story 2 (OPTIONAL)

- [ ] T040 [P] [US2] Unit test for DishService CRUD operations in backend/tests/unit/test_dish_service.py
- [ ] T041 [P] [US2] Integration test for dish API endpoints in backend/tests/integration/test_dishes.py
- [ ] T042 [P] [US2] E2E test for dish management flow in frontend/tests/e2e/dish-management.spec.ts

### Backend Implementation for User Story 2

- [ ] T043 [P] [US2] Create Dish Pydantic model with validation in backend/src/models/dish.py
- [ ] T044 [US2] Implement DishService with full CRUD operations in backend/src/services/dish_service.py
- [ ] T045 [US2] Implement dish deletion restrictions (check menu_dishes, combination_dishes) in backend/src/services/dish_service.py
- [ ] T046 [US2] Create dish API endpoints (GET /dishes, POST /dishes, GET /dishes/:id, PUT /dishes/:id, DELETE /dishes/:id) in backend/src/api/dishes.py
- [ ] T047 [US2] Add search/filter functionality for dishes in backend/src/api/dishes.py
- [ ] T048 [US2] Add pagination support for dish listing in backend/src/api/dishes.py

### Frontend Implementation for User Story 2

- [ ] T049 [P] [US2] Create dishService API client in frontend/src/services/dishService.ts
- [ ] T050 [P] [US2] Create dishStore with Pinia in frontend/src/stores/dishStore.ts
- [ ] T051 [P] [US2] Create DishesPage component showing dish library in frontend/src/pages/DishesPage.vue
- [ ] T052 [P] [US2] Create DishCard component for displaying individual dishes in frontend/src/components/dishes/DishCard.vue
- [ ] T053 [P] [US2] Create DishFormModal for add/edit operations in frontend/src/components/dishes/DishFormModal.vue
- [ ] T054 [P] [US2] Create DishSearchBar component with instant filtering in frontend/src/components/dishes/DishSearchBar.vue
- [ ] T055 [US2] Implement dish CRUD operations with optimistic UI updates
- [ ] T056 [US2] Add delete confirmation dialog with restriction error handling
- [ ] T057 [US2] Implement dish search/filter with debounce in frontend/src/stores/dishStore.ts

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. Users can manage dishes and create menus.

---

## Phase 5: User Story 3 - View Dish Statistics (Priority: P2)

**Goal**: Display dish usage statistics (times paired, times enjoyed) on dish detail page

**Independent Test**: View dish detail page, verify statistics display correctly, create menu with dish, verify count increments

### Recommended Tests for User Story 3 (OPTIONAL)

- [ ] T058 [P] [US3] Unit test for statistics increment logic in backend/tests/unit/test_statistics.py
- [ ] T059 [P] [US3] E2E test for dish detail page statistics in frontend/tests/e2e/dish-statistics.spec.ts

### Backend Implementation for User Story 3

- [ ] T060 [US3] Implement times_paired auto-increment when dish added to combination in backend/src/services/dish_service.py
- [ ] T061 [US3] Implement times_enjoyed auto-increment when dish added to menu in backend/src/services/dish_service.py
- [ ] T062 [US3] Add statistics fields to dish detail endpoint response in backend/src/api/dishes.py

### Frontend Implementation for User Story 3

- [ ] T063 [P] [US3] Create DishDetailPage component in frontend/src/pages/DishDetailPage.vue
- [ ] T064 [P] [US3] Create DishStatistics component showing times paired/enjoyed in frontend/src/components/dishes/DishStatistics.vue
- [ ] T065 [US3] Add navigation from DishesPage to DishDetailPage on dish click
- [ ] T066 [US3] Implement statistics display with pixel art styling and animations

**Checkpoint**: At this point, Users can view dish statistics and understand family preferences.

---

## Phase 6: User Story 4 - Manage Favorite Combinations (Priority: P3)

**Goal**: Enable users to create, edit, and delete dish combinations for quick menu creation

**Independent Test**: Create a combination, view in list, use it to populate menu, edit combination, delete it

### Recommended Tests for User Story 4 (OPTIONAL)

- [ ] T067 [P] [US4] Integration test for combination CRUD in backend/tests/integration/test_combinations.py
- [ ] T068 [P] [US4] E2E test for combination management flow in frontend/tests/e2e/combination-management.spec.ts

### Backend Implementation for User Story 4

- [ ] T069 [P] [US4] Create Combination Pydantic model in backend/src/models/combination.py
- [ ] T070 [P] [US4] Create CombinationDish junction model in backend/src/models/combination_dish.py
- [ ] T071 [US4] Implement CombinationService with CRUD operations in backend/src/services/combination_service.py
- [ ] T072 [US4] Create combination API endpoints in backend/src/api/combinations.py
- [ ] T073 [US4] Add validation to ensure minimum 1 dish per combination in backend/src/services/combination_service.py

### Frontend Implementation for User Story 4

- [ ] T074 [P] [US4] Create combinationService API client in frontend/src/services/combinationService.ts
- [ ] T075 [P] [US4] Create combinationStore with Pinia in frontend/src/stores/combinationStore.ts
- [ ] T076 [P] [US4] Create CombinationsPage component in frontend/src/pages/CombinationsPage.vue
- [ ] T077 [P] [US4] Create CombinationCard component in frontend/src/components/combinations/CombinationCard.vue
- [ ] T078 [P] [US4] Create CombinationFormModal for add/edit in frontend/src/components/combinations/CombinationFormModal.vue
- [ ] T079 [P] [US4] Create DishMultiSelector for selecting multiple dishes in frontend/src/components/combinations/DishMultiSelector.vue
- [ ] T080 [US4] Implement combination CRUD operations with optimistic updates
- [ ] T081 [US4] Add combination selector to MenuCreationModal for quick menu population
- [ ] T082 [US4] Implement "Use Combination" action to add all dishes to today's menu

**Checkpoint**: At this point, Users can create combinations and use them for faster menu creation.

---

## Phase 7: User Story 5 - View Historical Menus (Priority: P3)

**Goal**: Enable users to filter and view past menus by date range

**Independent Test**: Create menus on different dates, filter by date range, verify correct menus displayed

### Recommended Tests for User Story 5 (OPTIONAL)

- [ ] T083 [P] [US5] Integration test for history endpoint with date filtering in backend/tests/integration/test_history.py
- [ ] T084 [P] [US5] E2E test for history viewing flow in frontend/tests/e2e/history-viewing.spec.ts

### Backend Implementation for User Story 5

- [ ] T085 [US5] Implement history query with date range filtering in backend/src/services/history_service.py
- [ ] T086 [US5] Create history API endpoint (GET /history with start_date, end_date params) in backend/src/api/history.py
- [ ] T087 [US5] Add pagination support for history queries in backend/src/api/history.py

### Frontend Implementation for User Story 5

- [ ] T088 [P] [US5] Create historyService API client in frontend/src/services/historyService.ts
- [ ] T089 [P] [US5] Create historyStore with Pinia in frontend/src/stores/historyStore.ts
- [ ] T090 [P] [US5] Create HistoryPage component in frontend/src/pages/HistoryPage.vue
- [ ] T091 [P] [US5] Create DateRangePicker component in frontend/src/components/history/DateRangePicker.vue
- [ ] T092 [P] [US5] Create HistoryList component showing historical menus in frontend/src/components/history/HistoryList.vue
- [ ] T093 [P] [US5] Create HistoricalMenuCard component in frontend/src/components/history/HistoricalMenuCard.vue
- [ ] T094 [US5] Implement date filtering with smooth loading states
- [ ] T095 [US5] Add empty state for no menus in selected date range
- [ ] T096 [US5] Add navigation from historical menu card to dish detail on dish click

**Checkpoint**: All user stories should now be independently functional. Users can view meal history.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final quality checks

- [ ] T097 [P] Add loading skeletons for all pages to improve perceived performance
- [ ] T098 [P] Implement error boundary components for graceful error handling in frontend/src/components/ErrorBoundary.vue
- [ ] T099 [P] Add toast notification system for user feedback in frontend/src/components/ToastNotification.vue
- [ ] T100 [P] Optimize images and SVGs for fast loading
- [ ] T101 [P] Implement lazy loading for route components in frontend/src/router/index.ts
- [ ] T102 Verify all animations maintain 60fps (use Chrome DevTools Performance tab)
- [ ] T103 Test cold start time <2 seconds on 4G network throttling
- [ ] T104 [P] Run Lighthouse audit and achieve Performance score >90
- [ ] T105 [P] Test responsive design on mobile (320px), tablet (768px), desktop (1920px)
- [ ] T106 [P] Add touch target size verification (minimum 44x44px)
- [ ] T107 [P] Implement bundle size analysis and optimize if >500KB gzipped
- [ ] T108 [P] Add keyboard navigation support for accessibility
- [ ] T109 [P] Test with screen reader for accessibility compliance
- [ ] T110 [P] Write README.md with setup instructions and usage guide
- [ ] T111 [P] Create API documentation using FastAPI auto-generated Swagger UI
- [ ] T112 Performance test with 500+ dishes to verify no degradation
- [ ] T113 [P] Add 404 error page in frontend/src/pages/NotFoundPage.vue
- [ ] T114 [P] Implement network error handling with retry logic in frontend/src/services/api.ts
- [ ] T115 Final integration test of all user stories together

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independent of US1 (but US1 becomes more useful with US2)
- **User Story 3 (P2)**: Depends on User Story 2 (needs dish management to display statistics)
- **User Story 4 (P3)**: Can start after Foundational (Phase 2) - Independent but references dishes from US2
- **User Story 5 (P3)**: Depends on User Story 1 (needs menus to exist for history)

### Within Each User Story

- Tests (if included) SHOULD be written and FAIL before implementation
- Models before services
- Services before API endpoints
- Backend API endpoints before frontend services
- Frontend services before stores
- Stores before UI components
- Core implementation before integration

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes:
  - User Story 1 and User Story 2 can start in parallel (no dependencies)
  - User Story 4 can start in parallel with US1/US2
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Integration test for menu creation flow in backend/tests/integration/test_menus.py"
Task: "E2E test for today's menu creation in frontend/tests/e2e/menu-creation.spec.ts"

# Launch all models for User Story 1 together:
Task: "Create Menu Pydantic model with validation in backend/src/models/menu.py"
Task: "Create MenuDish junction model in backend/src/models/menu_dish.py"

# Launch all frontend services for User Story 1 together:
Task: "Create menuService API client in frontend/src/services/menuService.ts"
Task: "Create menuStore with Pinia in frontend/src/stores/menuStore.ts"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready - Users can create daily menus!

**MVP Value**: Families can immediately start planning daily meals and building habits.

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP! 🎯)
3. Add User Story 2 → Test independently → Deploy/Demo (Enhanced with dish management)
4. Add User Story 3 → Test independently → Deploy/Demo (Statistics insights)
5. Add User Story 4 → Test independently → Deploy/Demo (Quick combinations)
6. Add User Story 5 → Test independently → Deploy/Demo (Complete system with history)
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Menu creation)
   - Developer B: User Story 2 (Dish management)
3. After US1 and US2 complete:
   - Developer A: User Story 3 (Statistics)
   - Developer B: User Story 4 (Combinations)
4. After US3 and US4 complete:
   - Any available developer: User Story 5 (History)
5. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (if tests are included)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Summary

**Total Tasks**: 115
**Setup Phase**: 8 tasks
**Foundational Phase**: 14 tasks (BLOCKING)
**User Story 1 (P1 - MVP)**: 17 tasks (including 2 optional tests)
**User Story 2 (P2)**: 18 tasks (including 3 optional tests)
**User Story 3 (P2)**: 9 tasks (including 2 optional tests)
**User Story 4 (P3)**: 16 tasks (including 2 optional tests)
**User Story 5 (P3)**: 12 tasks (including 2 optional tests)
**Polish Phase**: 19 tasks

**Parallel Opportunities**: 47 tasks marked [P] can run in parallel within their phase

**Suggested MVP Scope**: Complete through User Story 1 (Phase 1-3) = 39 tasks

**Estimated Timeline**:
- MVP (US1): 1-1.5 weeks
- Full System (all stories): 2-3 weeks (single developer)
