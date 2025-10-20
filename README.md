# Feature Voting System

A full-stack application for voting on feature requests with backend API, web frontend, and native iOS mobile app.

## Architecture Overview

### Backend (FastAPI + Clean Architecture)
- **Domain Layer**: Business entities, value objects, domain exceptions
- **Application Layer**: Use cases, repository interfaces, DTOs
- **Infrastructure Layer**: Database models, repository implementations, configuration
- **Presentation Layer**: API routes, request/response schemas, controllers

### Frontend (Next.js 14 + shadcn/ui + Atomic Design)
- **Atoms**: Basic UI components (Button, Input, Card, Badge, Label, Textarea)
- **Molecules**: Feature-specific components (FeatureCard, VoteButton, FeatureForm)
- **Organisms**: Complex components (FeatureList, Header, Toaster)
- **Pages**: Application pages (Home, Create Feature, Feature Detail)

### Mobile (Native iOS with SwiftUI)
- **Models**: Data models matching API schema
- **Services**: API service layer, user preferences
- **ViewModels**: MVVM pattern with ObservableObject
- **Views**: SwiftUI views for all screens
- **Components**: Reusable SwiftUI components

## Technology Stack

### Backend
- **Framework**: FastAPI 0.109.0
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0 (async)
- **Migration**: Alembic
- **Language**: Python 3.11

### Frontend
- **Framework**: Next.js 14 (App Router)
- **UI Library**: shadcn/ui with Radix UI primitives
- **Styling**: Tailwind CSS
- **Forms**: React Hook Form + Zod validation
- **Language**: TypeScript

### Mobile
- **Platform**: iOS 16+
- **Framework**: SwiftUI
- **Architecture**: MVVM
- **Language**: Swift 5.0

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Database**: PostgreSQL 15

## Project Structure

```
feature-voting-system/
├── backend/
│   ├── domain/
│   │   ├── entities/          # Business entities (Feature)
│   │   ├── value_objects/     # Value objects (Vote)
│   │   └── exceptions/        # Domain exceptions
│   ├── application/
│   │   ├── use_cases/         # Business logic
│   │   ├── interfaces/        # Repository interfaces
│   │   └── dtos/              # Data transfer objects
│   ├── infrastructure/
│   │   ├── database/          # SQLAlchemy models & repositories
│   │   ├── config/            # Configuration
│   │   └── api/               # Dependency injection
│   ├── presentation/
│   │   └── api/               # FastAPI routes & schemas
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── app/               # Next.js App Router pages
│   │   ├── components/
│   │   │   ├── atoms/         # Basic components
│   │   │   ├── molecules/     # Composite components
│   │   │   └── organisms/     # Complex components
│   │   ├── lib/               # Utilities & API client
│   │   ├── hooks/             # React hooks
│   │   └── types/             # TypeScript types
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   └── Dockerfile
├── mobile/
│   └── FeatureVoting/
│       ├── Models/             # Swift data models
│       ├── Services/           # API & local services
│       ├── ViewModels/         # MVVM ViewModels
│       ├── Views/              # SwiftUI screens
│       ├── Components/         # Reusable components
│       └── FeatureVotingApp.swift
├── docker-compose.yml
└── README.md
```

## Features

### API Endpoints
- `POST /api/v1/features` - Create a new feature request
- `GET /api/v1/features` - List all features (with sorting)
- `GET /api/v1/features/{id}` - Get feature details
- `POST /api/v1/features/{id}/vote` - Vote for a feature
- `GET /api/health` - Health check

### Web Features
- View feature requests in a responsive grid
- Sort by votes or creation date (ascending/descending)
- Vote for features with optimistic UI updates
- Create new feature requests with validation
- View detailed feature information
- Toast notifications for user feedback

### iOS Features
- Native SwiftUI interface
- Pull-to-refresh functionality
- Create feature requests
- Vote on features
- View feature details
- Sort and filter options
- Persistent user identification

## Prerequisites

### For Backend & Frontend (Docker)
- Docker Desktop
- Docker Compose

### For iOS Development
- macOS 12.0+
- Xcode 14.0+
- iOS Simulator or physical device running iOS 16+

## Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
cd feature-voting-system
```

### 2. Setup Environment Variables

```bash
cp .env.example .env
```

Edit `.env` if needed (default values work for local development).

### 3. Start Backend & Frontend with Docker

```bash
docker-compose up --build
```

This will start:
- PostgreSQL database on port 5432
- Backend API on http://localhost:8000
- Frontend web app on http://localhost:3000

Wait for all services to be healthy. You should see:
```
feature-voting-backend | INFO: Application startup complete.
feature-voting-frontend | ✓ Ready in 2.3s
```

### 4. Access the Applications

- **Web App**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **API Health Check**: http://localhost:8000/api/health

### 5. Setup iOS App (Optional)

#### Open in Xcode

```bash
cd mobile
open FeatureVoting.xcodeproj
```

#### Configure API URL

For iOS Simulator (default):
- No changes needed, uses `http://localhost:8000`

For Physical Device:
1. Find your computer's local IP address:
   ```bash
   ifconfig | grep "inet " | grep -v 127.0.0.1
   ```
2. Edit `mobile/FeatureVoting/Services/APIService.swift`:
   ```swift
   baseURL = "http://YOUR_IP_ADDRESS:8000"
   ```

#### Run the App

1. Select a simulator or device in Xcode
2. Press `Cmd + R` or click the Play button
3. The app will build and launch

## API Usage Examples

### Create a Feature

```bash
curl -X POST http://localhost:8000/api/v1/features \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Dark Mode Support",
    "description": "Add dark mode to improve user experience",
    "author_name": "John Doe"
  }'
```

### List Features

```bash
# Most recent
curl http://localhost:8000/api/v1/features?sort_by=created_at&order=desc

# Most voted
curl http://localhost:8000/api/v1/features?sort_by=votes&order=desc
```

### Vote for a Feature

```bash
curl -X POST http://localhost:8000/api/v1/features/{feature_id}/vote \
  -H "Content-Type: application/json" \
  -d '{
    "user_identifier": "user_123"
  }'
```

## Development

### Backend Development

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run locally (without Docker)
export DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/feature_voting"
uvicorn main:app --reload
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
npm start
```

### iOS Development

1. Open `mobile/FeatureVoting.xcodeproj` in Xcode
2. Make changes to Swift files
3. Build and run with `Cmd + R`

## Architecture Patterns

### Backend: Clean Architecture

```
Presentation → Application → Domain ← Infrastructure
     ↓              ↓           ↑            ↑
  Routes      Use Cases    Entities    Repositories
  Schemas        DTOs       Exceptions     Database
```

**Benefits**:
- Clear separation of concerns
- Business logic independent of frameworks
- Testable and maintainable
- Easy to swap implementations

### Frontend: Atomic Design

```
Pages
  ↓
Organisms (FeatureList, Header)
  ↓
Molecules (FeatureCard, VoteButton)
  ↓
Atoms (Button, Input, Card)
```

**Benefits**:
- Consistent component hierarchy
- Reusable components
- Easy to maintain and scale
- Clear component responsibilities

### iOS: MVVM Pattern

```
View ↔ ViewModel → Model
         ↓
      Service
```

**Benefits**:
- Clear separation of UI and logic
- SwiftUI-friendly with @Published
- Easy to test ViewModels
- Reactive data binding

## Design Decisions

1. **UUID for IDs**: Better for distributed systems and prevents enumeration
2. **Simple User Identification**: Uses local storage/UserDefaults for MVP
3. **Optimistic UI**: Immediate feedback for better UX
4. **Health Checks**: Container orchestration and monitoring
5. **Multi-stage Builds**: Optimized Docker images
6. **Async/Await**: Modern async patterns in all layers
7. **Type Safety**: TypeScript (frontend) and Swift (mobile)

## Testing

### Backend Tests (Future Enhancement)

```bash
cd backend
pytest
```

### Frontend Tests (Future Enhancement)

```bash
cd frontend
npm test
```

### iOS Tests (Future Enhancement)

- Use XCTest framework in Xcode
- Press `Cmd + U` to run tests

## Deployment

### Backend Deployment

1. Build production Docker image
2. Set environment variables
3. Deploy to cloud platform (AWS, GCP, Azure)
4. Configure PostgreSQL instance
5. Run database migrations

### Frontend Deployment

- Deploy to Vercel (recommended)
- Or build and deploy Docker container
- Set `NEXT_PUBLIC_API_URL` to production API

### iOS Deployment

1. Configure signing in Xcode
2. Archive the app (`Product → Archive`)
3. Upload to App Store Connect
4. Submit for review

## Troubleshooting

### Docker Issues

```bash
# Stop all containers
docker-compose down

# Remove volumes and restart
docker-compose down -v
docker-compose up --build
```

### Database Connection Issues

- Ensure PostgreSQL container is healthy
- Check DATABASE_URL environment variable
- Verify port 5432 is not in use

### iOS Simulator Can't Connect

- Use `http://localhost:8000` for simulator
- Check backend is running
- Verify Info.plist has NSAppTransportSecurity settings

### iOS Device Can't Connect

- Use your computer's local IP instead of localhost
- Ensure device and computer are on same network
- Update APIService.swift with correct IP

## License

MIT License

## Contributors

AI-Generated Project following Clean Architecture and Atomic Design principles.
# voting-feature
