<!--
SYNC IMPACT REPORT
==================
Version Change: 0.0.0 → 1.0.0 (Initial constitution creation)
Modified Principles: N/A (Initial creation)
Added Sections:
  - Core Principles (5 principles)
  - Technology Stack
  - Development Workflow
  - Governance
Removed Sections: N/A
Templates Requiring Updates:
  - ✅ .specify/templates/plan-template.md (Constitution Check section aligned)
  - ✅ .specify/templates/spec-template.md (Requirements structure compatible)
  - ✅ .specify/templates/tasks-template.md (Task categorization aligned)
Follow-up TODOs: None
-->

# 家庭点菜网站 (Family Menu Ordering Website) Constitution

## Core Principles

### I. User Experience Excellence (NON-NEGOTIABLE)

Every feature MUST deliver a warm, delightful experience through cute pixel art aesthetics and silky smooth interactions.

**Why**: The family-oriented nature of this application demands an inviting, approachable interface that brings joy to everyday meal planning. Cold start time directly impacts daily usage frequency—families won't wait for a slow app during busy meal times.

**How to apply**:
- All UI elements MUST use the warm pixel art design system
- Animations MUST maintain 60fps performance (no frame drops below 55fps)
- Application cold start MUST complete in under 2 seconds on 4G mobile connections
- All interactive elements MUST provide immediate visual feedback (within 16ms)
- Color palette MUST use warm tones (amber, coral, peach, soft yellows) with premium feel
- Transitions MUST be smooth and natural, avoiding jarring movements

### II. Performance Standards (NON-NEGOTIABLE)

Performance is a feature, not an afterthought. All features MUST meet strict performance budgets before deployment.

**Why**: A family app used multiple times daily cannot have performance degradation. Slow loading or choppy animations will lead to abandonment and return to manual meal planning methods.

**How to apply**:
- Bundle size budgets: Initial load <500KB gzipped
- Time to Interactive <2 seconds on mobile 4G
- Animation frame rate MUST NOT drop below 55fps during any interaction
- Database queries MUST return within 200ms (p95)
- API response time MUST be <150ms (p95)
- Images MUST be optimized and lazy-loaded
- Performance testing MUST pass in CI/CD before merge

### III. Component-Based Architecture

All frontend code MUST be built as modular, reusable Vue 3 components with clear separation of concerns.

**Why**: Component reusability reduces development time, ensures design consistency, and makes the codebase maintainable for long-term evolution. Vue 3's Composition API enables better logic reuse and testing.

**How to apply**:
- Each component MUST have a single, clear responsibility
- Shared UI components MUST be placed in a design system library
- Components MUST use TypeScript for type safety
- Component props and events MUST be well-documented
- Complex state MUST use Vue 3's reactive primitives (ref, reactive, computed)
- Components MUST be independently testable in isolation

### IV. Automated Quality Assurance (NON-NEGOTIABLE)

All code changes MUST pass automated testing and quality gates before deployment.

**Why**: Manual testing is insufficient for ensuring reliability across devices and use cases. Automated testing catches regressions early and enables confident, rapid iteration. CI/CD automation eliminates human error in deployment.

**How to apply**:
- All new features MUST include unit tests (minimum 80% code coverage)
- Critical user journeys MUST have end-to-end tests
- All code MUST pass linting (ESLint for Vue, Pylint/Black for Python)
- Type checking MUST pass (TypeScript for frontend, mypy for backend)
- Security scans MUST pass (dependency vulnerabilities, code analysis)
- Performance tests MUST validate 60fps and <2s cold start
- No code MAY be merged to main without passing CI/CD gates

### V. API-First Design

Backend and frontend MUST be developed as independent layers communicating through well-defined RESTful APIs.

**Why**: Clear API contracts enable parallel development, easier testing, and future flexibility (mobile apps, third-party integrations). Supabase provides the database layer, while Python backend handles business logic.

**How to apply**:
- All API endpoints MUST be documented with OpenAPI/Swagger
- API versioning MUST follow semantic versioning (v1, v2, etc.)
- Request/response schemas MUST be validated
- APIs MUST return appropriate HTTP status codes
- Error responses MUST include clear, actionable error messages
- Frontend MUST NOT access Supabase directly—only through Python API layer
- API changes MUST be backward compatible or versioned

## Technology Stack

**Frontend**:
- Framework: Vue 3 (Composition API)
- Language: TypeScript
- Build Tool: Vite
- Styling: CSS/SCSS with pixel art design system
- State Management: Pinia
- Testing: Vitest (unit), Playwright (e2e)

**Backend**:
- Language: Python 3.11+
- Framework: FastAPI
- Database: Supabase (PostgreSQL)
- ORM: SQLAlchemy or Supabase Python client
- Testing: pytest
- API Documentation: OpenAPI/Swagger

**Infrastructure**:
- Code Hosting: GitHub
- CI/CD: GitHub Actions
- Deployment: Vercel (serverless functions for Python backend)
- Database Hosting: Supabase Cloud
- CDN: Vercel Edge Network

**Design Assets**:
- Pixel art sprites and icons
- Warm color palette (amber, coral, peach, cream, soft yellows)
- Smooth animation library (custom or CSS-based)

## Development Workflow

### Test-Driven Development

For critical features and bug fixes:
1. Write failing test defining expected behavior
2. Implement minimum code to pass test
3. Refactor while keeping tests green
4. All tests MUST pass before code review

### Code Review Requirements

- All changes MUST be reviewed by at least one team member
- Reviews MUST verify compliance with constitution principles
- Performance implications MUST be explicitly evaluated
- Security considerations MUST be documented

### Deployment Process

1. Code merged to main branch triggers CI/CD pipeline
2. Automated tests MUST pass (unit, integration, e2e)
3. Performance benchmarks MUST validate <2s cold start and 60fps
4. Security scans MUST pass
5. Automatic deployment to Vercel preview environment
6. Manual verification in preview (optional)
7. Automatic promotion to production

### Quality Gates

**Pre-merge**:
- Linting passes (0 errors)
- Type checking passes
- Unit tests pass with >80% coverage
- Integration tests pass
- No security vulnerabilities in dependencies

**Pre-deployment**:
- All pre-merge gates
- End-to-end tests pass
- Performance benchmarks meet standards
- Bundle size within budget

## Governance

This constitution supersedes all other development practices and conventions. When in doubt, refer to these principles.

### Amendment Process

1. Propose amendment with clear rationale
2. Document impact on existing code and workflows
3. Update constitution with version increment (MAJOR.MINOR.PATCH)
4. Propagate changes to dependent templates and documentation
5. Communicate changes to all team members

### Versioning Policy

- **MAJOR**: Backward incompatible principle removals or fundamental redefinitions
- **MINOR**: New principles added or materially expanded guidance
- **PATCH**: Clarifications, wording improvements, non-semantic refinements

### Compliance Verification

- All pull requests MUST include constitution compliance checklist
- Code reviews MUST explicitly verify principle adherence
- Performance testing MUST validate all performance-related principles
- Quarterly audits MAY review codebase compliance with constitution

**Version**: 1.0.0 | **Ratified**: 2026-03-30 | **Last Amended**: 2026-03-30
