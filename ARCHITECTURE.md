# Architecture Documentation

## System Overview

The Feature Voting System is a full-stack application built with three main components:
1. **Backend API** (FastAPI + PostgreSQL)
2. **Web Frontend** (Next.js 14 + shadcn/ui)
3. **Native iOS App** (SwiftUI)

## Backend Architecture: Clean Architecture

### Layer Structure

```
┌─────────────────────────────────────────────────────────┐
│                    Presentation Layer                    │
│  ┌────────────────────────────────────────────────────┐ │
│  │  FastAPI Routes, Pydantic Schemas, Controllers     │ │
│  └────────────────────────────────────────────────────┘ │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                   Application Layer                      │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Use Cases (CreateFeature, UpvoteFeature, etc.)   │ │
│  │  Repository Interfaces, DTOs                       │ │
│  └────────────────────────────────────────────────────┘ │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                     Domain Layer                         │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Entities (Feature), Value Objects (Vote)          │ │
│  │  Domain Exceptions, Business Rules                 │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                       ▲
┌──────────────────────┴──────────────────────────────────┐
│                 Infrastructure Layer                     │
│  ┌────────────────────────────────────────────────────┐ │
│  │  SQLAlchemy Models, Repository Implementations     │ │
│  │  Database Connection, Configuration                │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### Dependency Flow

```
Presentation → Application → Domain
                              ↑
Infrastructure ──────────────┘
```

**Key Principle**: Dependencies point inward. Domain has no dependencies.

### File Organization

```
backend/
├── domain/
│   ├── entities/
│   │   └── feature.py           # Feature entity with business logic
│   ├── value_objects/
│   │   └── vote.py              # Vote value object
│   └── exceptions/
│       └── domain_exceptions.py # Domain-specific exceptions
├── application/
│   ├── use_cases/
│   │   ├── create_feature.py    # CreateFeatureUseCase
│   │   ├── get_feature.py       # GetFeatureUseCase
│   │   ├── list_features.py     # ListFeaturesUseCase
│   │   └── upvote_feature.py    # UpvoteFeatureUseCase
│   ├── interfaces/
│   │   └── repositories/
│   │       ├── feature_repository.py  # Interface
│   │       └── vote_repository.py     # Interface
│   └── dtos/
│       └── feature_dto.py       # Data transfer objects
├── infrastructure/
│   ├── database/
│   │   ├── models/
│   │   │   ├── feature_model.py # SQLAlchemy model
│   │   │   └── vote_model.py    # SQLAlchemy model
│   │   ├── repositories/
│   │   │   ├── feature_repository_impl.py
│   │   │   └── vote_repository_impl.py
│   │   └── connection.py        # Database connection
│   ├── config/
│   │   └── settings.py          # Configuration management
│   └── api/
│       └── dependencies.py      # Dependency injection
└── presentation/
    └── api/
        ├── routes/
        │   ├── features.py      # Feature endpoints
        │   └── health.py        # Health check
        └── schemas/
            └── feature_schemas.py # Request/Response schemas
```

## Frontend Architecture: Atomic Design

### Component Hierarchy

```
┌─────────────────────────────────────────────────────────┐
│                        Pages                             │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Home, CreateFeature, FeatureDetail                │ │
│  └────────────────────────────────────────────────────┘ │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                     Organisms                            │
│  ┌────────────────────────────────────────────────────┐ │
│  │  FeatureList, Header, Toaster                      │ │
│  └────────────────────────────────────────────────────┘ │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                     Molecules                            │
│  ┌────────────────────────────────────────────────────┐ │
│  │  FeatureCard, VoteButton, FeatureForm              │ │
│  └────────────────────────────────────────────────────┘ │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                       Atoms                              │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Button, Input, Card, Badge, Label, Textarea       │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### File Organization

```
frontend/src/
├── app/                         # Next.js App Router
│   ├── layout.tsx              # Root layout
│   ├── page.tsx                # Home page
│   ├── create/
│   │   └── page.tsx            # Create feature page
│   ├── features/
│   │   └── [id]/
│   │       └── page.tsx        # Feature detail page
│   └── globals.css             # Global styles
├── components/
│   ├── atoms/                  # Basic building blocks
│   │   ├── button.tsx
│   │   ├── input.tsx
│   │   ├── card.tsx
│   │   ├── badge.tsx
│   │   ├── label.tsx
│   │   ├── textarea.tsx
│   │   └── toast.tsx
│   ├── molecules/              # Composite components
│   │   ├── feature-card.tsx
│   │   ├── vote-button.tsx
│   │   └── feature-form.tsx
│   └── organisms/              # Complex components
│       ├── feature-list.tsx
│       ├── header.tsx
│       └── toaster.tsx
├── lib/
│   ├── utils.ts               # Utility functions
│   └── api.ts                 # API client
├── hooks/
│   └── use-toast.ts           # Toast hook
└── types/
    └── index.ts               # TypeScript types
```

### Component Responsibilities

**Atoms**: Basic UI elements with no business logic
- Pure presentational components
- Highly reusable
- Accept props for customization

**Molecules**: Combinations of atoms serving a specific purpose
- May contain minimal local state
- Handle specific user interactions
- Reusable in different contexts

**Organisms**: Complex components with business logic
- May fetch data
- Contain multiple molecules/atoms
- Manage complex state

**Pages**: Top-level route components
- Compose organisms
- Handle routing
- Minimal logic (delegate to organisms)

## iOS Architecture: MVVM Pattern

### Architecture Flow

```
┌─────────────────────────────────────────────────────────┐
│                        View                              │
│  ┌────────────────────────────────────────────────────┐ │
│  │  SwiftUI Views (FeaturesListView, etc.)           │ │
│  └────────────┬───────────────────────────────────────┘ │
└───────────────┼─────────────────────────────────────────┘
                │ @Published/@ObservedObject
┌───────────────▼─────────────────────────────────────────┐
│                     ViewModel                            │
│  ┌────────────────────────────────────────────────────┐ │
│  │  FeaturesViewModel, FeatureDetailViewModel         │ │
│  └────────────┬───────────────────────────────────────┘ │
└───────────────┼─────────────────────────────────────────┘
                │ async/await
┌───────────────▼─────────────────────────────────────────┐
│                      Service                             │
│  ┌────────────────────────────────────────────────────┐ │
│  │  APIService, UserDefaultsService                   │ │
│  └────────────┬───────────────────────────────────────┘ │
└───────────────┼─────────────────────────────────────────┘
                │
┌───────────────▼─────────────────────────────────────────┐
│                       Model                              │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Feature, CreateFeatureRequest, VoteRequest        │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### File Organization

```
mobile/FeatureVoting/
├── Models/
│   └── Feature.swift           # Data models
├── Services/
│   ├── APIService.swift        # Network layer
│   └── UserDefaultsService.swift
├── ViewModels/
│   ├── FeaturesViewModel.swift
│   ├── FeatureDetailViewModel.swift
│   └── CreateFeatureViewModel.swift
├── Views/
│   ├── FeaturesListView.swift
│   ├── FeatureDetailView.swift
│   └── CreateFeatureView.swift
├── Components/
│   └── FeatureCardView.swift
└── FeatureVotingApp.swift     # App entry point
```

### Responsibilities

**Model**: Data structures matching API responses
- Codable for JSON parsing
- Identifiable for SwiftUI lists
- Computed properties for formatting

**Service**: External communication
- API calls with async/await
- Local data persistence
- Error handling

**ViewModel**: Business logic and state management
- @Published properties for reactive UI
- Calls services
- Transforms data for view
- Handles user actions

**View**: UI presentation
- SwiftUI declarative syntax
- Observes ViewModel
- User interaction handlers
- No business logic

## Data Flow

### Creating a Feature

```
┌──────────┐
│   User   │
└────┬─────┘
     │ Fills form
     ▼
┌────────────────┐        ┌──────────────────┐
│ FeatureForm    │        │ CreateFeature    │
│ (Frontend)     │───────▶│ UseCase          │
└────────────────┘  POST  │ (Backend)        │
                           └────────┬─────────┘
                                    │ validates
                                    ▼
                           ┌──────────────────┐
                           │ Feature Entity   │
                           │ (Domain)         │
                           └────────┬─────────┘
                                    │ saves
                                    ▼
                           ┌──────────────────┐
                           │ Repository       │
                           │ (Infrastructure) │
                           └────────┬─────────┘
                                    │
                                    ▼
                           ┌──────────────────┐
                           │ PostgreSQL       │
                           └──────────────────┘
```

### Voting for a Feature

```
┌──────────┐
│   User   │
└────┬─────┘
     │ Clicks vote
     ▼
┌────────────────┐  optimistic  ┌──────────────────┐
│ VoteButton     │   update      │ UpvoteFeature    │
│ (Frontend)     │──────────────▶│ UseCase          │
└────────────────┘               │ (Backend)        │
     │                           └────────┬─────────┘
     │                                    │
     │                                    ▼
     │                           ┌──────────────────┐
     │                           │ Check duplicate  │
     │                           │ vote             │
     │                           └────────┬─────────┘
     │                                    │
     │                                    ▼
     │                           ┌──────────────────┐
     │                           │ Increment votes  │
     │                           └────────┬─────────┘
     │                                    │
     │ ◄──────────────────────────────────┘
     │ Update with server data
     ▼
┌────────────────┐
│ UI reflects    │
│ new count      │
└────────────────┘
```

## Key Design Patterns

### Backend

1. **Repository Pattern**: Abstracts data access
2. **Dependency Injection**: Loose coupling between layers
3. **DTO Pattern**: Separates domain from presentation
4. **Use Case Pattern**: Encapsulates business operations

### Frontend

1. **Atomic Design**: Component hierarchy
2. **Composition**: Compose small components into larger ones
3. **Custom Hooks**: Reusable stateful logic
4. **Optimistic Updates**: Immediate UI feedback

### iOS

1. **MVVM**: Separation of concerns
2. **Singleton Pattern**: Shared services (APIService)
3. **Observer Pattern**: SwiftUI reactive updates
4. **Async/Await**: Modern concurrency

## API Design

### RESTful Principles

- Resources: `/api/v1/features`
- HTTP Methods: GET, POST
- Status Codes: 200, 201, 400, 404, 409, 500
- JSON payloads

### Endpoints

```
GET    /api/v1/features              List features
POST   /api/v1/features              Create feature
GET    /api/v1/features/{id}         Get feature
POST   /api/v1/features/{id}/vote    Vote for feature
GET    /api/health                   Health check
```

### Request/Response Format

**Feature Response**:
```json
{
  "id": "uuid",
  "title": "string",
  "description": "string",
  "author_name": "string",
  "votes_count": 0,
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## Database Schema

```sql
CREATE TABLE features (
    id UUID PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    author_name VARCHAR(100) NOT NULL,
    votes_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE votes (
    id UUID PRIMARY KEY,
    feature_id UUID REFERENCES features(id),
    user_identifier VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(feature_id, user_identifier)
);
```

## Deployment Architecture

```
┌──────────────────────────────────────────────────────┐
│                   Docker Compose                      │
│                                                       │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐    │
│  │  Frontend  │  │  Backend   │  │ PostgreSQL │    │
│  │  (Next.js) │  │  (FastAPI) │  │    (DB)    │    │
│  │  :3000     │  │  :8000     │  │  :5432     │    │
│  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘    │
│        │                │                │           │
│        └────────────────┴────────────────┘           │
└──────────────────────────────────────────────────────┘
                         ▲
                         │ HTTP
                         │
                ┌────────┴─────────┐
                │   iOS App        │
                │   (SwiftUI)      │
                └──────────────────┘
```

## Security Considerations

1. **CORS**: Configured for allowed origins
2. **Input Validation**: Pydantic schemas + Zod validation
3. **SQL Injection**: SQLAlchemy ORM protection
4. **Rate Limiting**: To be implemented
5. **Authentication**: Simplified for MVP (user_identifier)

## Performance Optimizations

1. **Database Indexing**: On feature_id and user_identifier
2. **Async I/O**: FastAPI + SQLAlchemy async
3. **Connection Pooling**: PostgreSQL connection pool
4. **Optimistic UI**: Immediate feedback without waiting
5. **Lazy Loading**: SwiftUI LazyVStack

## Testing Strategy

### Backend
- Unit tests: Domain entities, use cases
- Integration tests: Repository implementations
- E2E tests: API endpoints

### Frontend
- Unit tests: Utility functions, hooks
- Component tests: Individual components
- Integration tests: Page flows

### iOS
- Unit tests: ViewModels, Services
- UI tests: SwiftUI views
- Integration tests: API communication

## Future Enhancements

1. **Authentication**: JWT-based auth system
2. **Comments**: Add comments to features
3. **Categories**: Organize features by category
4. **Search**: Full-text search
5. **Admin Panel**: Manage features
6. **Analytics**: Track voting patterns
7. **Notifications**: Push notifications for iOS
8. **Real-time Updates**: WebSocket support
9. **Image Uploads**: Attach images to features
10. **Export**: Export features to CSV/PDF
