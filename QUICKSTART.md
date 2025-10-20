# Quick Start Guide

Get the Feature Voting System running in 5 minutes!

## Prerequisites

- Docker Desktop installed
- (Optional) Xcode for iOS development

## 1. Start the Application

```bash
cd feature-voting-system
docker-compose up --build
```

Wait for services to start (approximately 30-60 seconds).

## 2. Verify Services

Open your browser and check:

- ✅ Frontend: http://localhost:3000
- ✅ API Docs: http://localhost:8000/docs
- ✅ Health Check: http://localhost:8000/api/health

You should see the Feature Voting web interface!

## 3. Test the Application

### Create a Feature (Web)

1. Go to http://localhost:3000
2. Click "New Feature" button
3. Fill in the form:
   - Title: "Dark Mode Support"
   - Description: "Add dark mode toggle to the app"
   - Your Name: "John Doe"
4. Click "Create Feature"
5. You'll be redirected to the home page with your feature!

### Vote for a Feature

1. On the home page, click the vote button (arrow up icon)
2. The vote count increments immediately
3. Try voting again - you'll get an error (duplicate votes prevented)

### View Feature Details

1. Click on a feature card
2. See the full description and vote count
3. Vote from the detail page

## 4. (Optional) Run iOS App

### Open in Xcode

```bash
cd mobile
open FeatureVoting.xcodeproj
```

### Run the App

1. Select "iPhone 15" simulator
2. Press `Cmd + R`
3. Wait for build to complete
4. The app launches with feature list!

### Test iOS Features

- Pull down to refresh
- Tap "+" to create feature
- Tap feature card to view details
- Tap vote button to vote
- Use filter menu (top left) to sort

## Common Commands

### Stop All Services

```bash
docker-compose down
```

### Restart Services

```bash
docker-compose restart
```

### View Logs

```bash
# All services
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# Frontend only
docker-compose logs -f frontend
```

### Reset Database

```bash
docker-compose down -v
docker-compose up --build
```

## API Testing with cURL

### Create Feature

```bash
curl -X POST http://localhost:8000/api/v1/features \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Search Functionality",
    "description": "Add search bar to find features quickly",
    "author_name": "Jane Smith"
  }'
```

### List Features

```bash
curl http://localhost:8000/api/v1/features
```

### Vote

```bash
# Replace {feature_id} with actual ID from list
curl -X POST http://localhost:8000/api/v1/features/{feature_id}/vote \
  -H "Content-Type: application/json" \
  -d '{"user_identifier": "user_123"}'
```

## Troubleshooting

### Port Already in Use

If ports 3000, 8000, or 5432 are in use:

```bash
# Find process using port
lsof -i :8000

# Kill the process
kill -9 <PID>
```

### Database Connection Error

```bash
# Wait for database to be ready
docker-compose logs database

# Should see: "database system is ready to accept connections"
```

### Frontend Not Loading

1. Check backend is running: http://localhost:8000/api/health
2. Check frontend logs: `docker-compose logs frontend`
3. Try rebuilding: `docker-compose up --build frontend`

### iOS App Can't Connect

**For Simulator**:
- Backend must be running on `localhost:8000`
- Check: `curl http://localhost:8000/api/health`

**For Physical Device**:
1. Get your computer's IP:
   ```bash
   ifconfig | grep "inet " | grep -v 127.0.0.1
   ```
2. Edit `mobile/FeatureVoting/Services/APIService.swift`:
   ```swift
   baseURL = "http://YOUR_IP:8000"
   ```
3. Rebuild the app

## Next Steps

- Read [README.md](README.md) for detailed documentation
- Check [ARCHITECTURE.md](ARCHITECTURE.md) for architecture details
- Explore the API at http://localhost:8000/docs
- Customize the frontend styling
- Add your own features!

## File Locations

- Backend code: `backend/`
- Frontend code: `frontend/src/`
- iOS code: `mobile/FeatureVoting/`
- Docker config: `docker-compose.yml`

## Development Tips

### Hot Reload

All services support hot reload:
- **Backend**: Edit Python files → Auto-reloads
- **Frontend**: Edit React files → Auto-updates browser
- **iOS**: Edit Swift files → Rebuild with Cmd+R

### API Documentation

Visit http://localhost:8000/docs for:
- Interactive API testing
- Request/response schemas
- Try out endpoints

### Database Access

```bash
# Connect to PostgreSQL
docker exec -it feature-voting-db psql -U postgres -d feature_voting

# List tables
\dt

# Query features
SELECT * FROM features;

# Exit
\q
```

## Support

If you encounter issues:
1. Check the logs: `docker-compose logs`
2. Verify all services are running: `docker ps`
3. Review the error message
4. Consult [README.md](README.md) troubleshooting section

Happy coding! 🚀
