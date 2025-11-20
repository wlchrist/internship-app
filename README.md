# Internship Aggregator

A full-stack application that aggregates Computer Science internship postings from the Fantastic Jobs API and presents them in a clean, modern web interface. The application fetches real internship data every 24 hours and displays them in real-time.

## Architecture

- **Frontend**: Next.js 15.5.4 with React 19.1.0, TypeScript, and Tailwind CSS
- **Backend**: FastAPI with Python 3.13
- **Data Source**: Fantastic Jobs API via RapidAPI
- **Auto-refresh**: Data refreshes every 24 hours automatically
- **Filtering**: Focuses on Computer Science internships (Software Engineering, Data Science, AI/ML, etc.)

## Features

- **Real-time CS Internship Listings**: View current Computer Science internship opportunities
- **Auto-refresh**: Data refreshes every 24 hours automatically
- **Modern UI**: Clean, responsive design with Tailwind CSS
- **Mobile-friendly**: Responsive design that works on all devices
- **Detailed Information**: Company, location, salary, requirements, and more
- **Remote Work Support**: Clear indication of remote opportunities
- **CS-Focused**: Specifically targets Software Engineering, Data Science, AI/ML, and related fields
- **Smart Filtering**: Excludes non-CS positions (accounting, finance, marketing, etc.)
- **SMS Notifications**: Professional SMS delivery via Twilio
- **Instant Alerts**: Real-time SMS for urgent opportunities
- **Personalized Preferences**: Choose notification types and frequency
- **User Credentials**: Users can provide their own Twilio credentials
- **Free Tier**: $15 Twilio credit (enough for ~2,000 SMS)

## Quick Start

### Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Node.js** (v18 or later)
- **npm** (comes with Node.js) or **yarn**
- **Python** (v3.10 or later)
- **pip** (Python package manager)

### Option 1: Using Startup Scripts (Recommended)

The startup scripts will automatically handle virtual environment creation and dependency installation.

1. **Start the Backend**:
   ```bash
   ./start-backend.sh
   ```
   - Automatically creates Python virtual environment if needed
   - Installs all required dependencies
   - Starts FastAPI server on `http://localhost:8000`
   - API documentation available at `http://localhost:8000/docs`

2. **Start the Frontend** (in a new terminal):
   ```bash
   ./start-frontend.sh
   ```
   - Automatically installs Node.js dependencies if needed
   - Starts Next.js development server on `http://localhost:3000`

### Option 2: Manual Setup

1. **Backend Setup**:
   ```bash
   # Navigate to API directory
   cd api
   
   # Create and activate virtual environment
   python3 -m venv fastapi
   source fastapi/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Start the server
   python main.py
   ```

2. **Frontend Setup** (in a new terminal):
   ```bash
   # Navigate to frontend directory
   cd web/internship-app-frontend
   
   # Install dependencies
   npm install
   
   # Start development server
   npm run dev
   ```

## API Configuration

The application uses the Fantastic Jobs API via RapidAPI. The API key is already configured, but you can customize it:

### Environment Variables

Create a `.env` file in the `api` directory (optional):

```bash
# API Configuration
RAPIDAPI_KEY=your_rapidapi_key_here
API_HOST=0.0.0.0
API_PORT=8000

# SMS Notification Configuration (Optional - Users can provide their own)
# System-wide Twilio credentials (fallback if users don't provide their own)
# Get free account at: https://www.twilio.com/try-twilio
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
```

### Current API Query

The application uses a comprehensive query to fetch CS internships:

- **Location**: United States
- **Keywords**: Python, Java, C++, JavaScript, Go, Rust
- **Roles**: Software Engineering, Full-Stack Developer, AI Research, Machine Learning Engineer, Data Science, etc.
- **Exclusions**: Senior, staff, lead, principal positions
- **Focus**: Internship and co-op positions only

## API Endpoints

### Core Endpoints
- `GET /` - API health check
- `GET /internships` - Get all internship postings
- `GET /internships/refresh` - Manually refresh internship data
- `GET /health` - Health check endpoint
- `GET /docs` - Interactive API documentation (Swagger UI)

### Notification Endpoints
- `POST /notifications/subscribe` - Subscribe to email/SMS notifications
- `POST /notifications/unsubscribe` - Unsubscribe from notifications
- `GET /notifications/subscribers` - Get subscriber count and info (admin)
- `POST /notifications/send-test` - Send test notification (admin)

## Development

### Essential Files for Contributors

#### Backend Files (FastAPI)

**Core Application Files:**
- **`api/main.py`** - Main FastAPI application with all API endpoints
- **`api/models.py`** - Pydantic data models for internship postings
- **`api/services.py`** - Business logic for fetching and managing internship data
- **`api/requirements.txt`** - Python dependencies

**Key Endpoints in `main.py`:**
- `GET /internships` - Returns all internship postings
- `GET /internships/refresh` - Manually refreshes data
- `GET /health` - Health check

#### Frontend Files (Next.js)

**Main Application Files:**
- **`web/internship-app-frontend/src/app/page.tsx`** - Main homepage component
- **`web/internship-app-frontend/src/app/layout.tsx`** - Root layout and metadata
- **`web/internship-app-frontend/src/app/components/InternshipCard.tsx`** - Individual internship card component
- **`web/internship-app-frontend/src/app/components/LoadingSpinner.tsx`** - Loading spinner component
- **`web/internship-app-frontend/src/app/components/FilterPanel.tsx`** - Filter panel component
- **`web/internship-app-frontend/src/app/components/NotificationSubscription.tsx`** - SMS notification subscription component

**Configuration Files:**
- **`web/internship-app-frontend/package.json`** - Node.js dependencies and scripts
- **`web/internship-app-frontend/next.config.ts`** - Next.js configuration
- **`web/internship-app-frontend/tsconfig.json`** - TypeScript configuration

#### File Structure Summary

```
internship-app/
├── api/
│   ├── main.py              # Main API endpoints
│   ├── models.py           # Data models
│   ├── services.py         # Business logic
│   ├── requirements.txt     # Dependencies
│   └── fastapi/            # Python virtual environment (auto-created)
├── web/internship-app-frontend/
│   ├── src/app/
│   │   ├── page.tsx        # Main page
│   │   ├── layout.tsx      # Root layout
│   │   └── components/
│   │       ├── InternshipCard.tsx    # Internship display
│   │       ├── FilterPanel.tsx       # Filter interface
│   │       ├── NotificationSubscription.tsx  # SMS subscription
│   │       └── LoadingSpinner.tsx   # Loading component
│   ├── package.json        # Node.js dependencies
│   └── next.config.ts      # Next.js config
├── start-backend.sh        # Backend startup script
├── start-frontend.sh       # Frontend startup script
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

#### Quick Reference for Common Tasks

| Task | File to Edit |
|------|-------------|
| Add new API endpoint | `api/main.py` |
| Change data structure | `api/models.py` |
| Modify data fetching | `api/services.py` |
| Update main page | `web/.../src/app/page.tsx` |
| Add new UI component | `web/.../src/app/components/` |
| Change styling | Any `.tsx` file (Tailwind CSS) |
| Add dependencies | `api/requirements.txt` or `web/.../package.json` |

#### Development Tips

1. **Start with `api/main.py`** for backend changes
2. **Start with `web/.../src/app/page.tsx`** for frontend changes
3. **Use the API docs** at `http://localhost:8000/docs` to test endpoints
4. **Check browser console** for frontend errors
5. **Both servers auto-reload** when you save changes

### Backend Development

The backend is built with FastAPI and includes:

- **Models** (`models.py`): Pydantic models for internship data
- **Services** (`services.py`): Business logic for fetching and managing data
- **Main App** (`main.py`): FastAPI application with endpoints

### Frontend Development

The frontend is built with Next.js and includes:

- **Components**: Reusable React components
- **Pages**: Next.js App Router pages
- **Styling**: Tailwind CSS for responsive design

### Adding Real API Integration

To integrate with real job board APIs:

1. Update the `_fetch_from_real_api` method in `services.py`
2. Add API credentials to environment variables
3. Implement data transformation for different API formats
4. Add error handling and rate limiting

Example:
```python
async def _fetch_from_real_api(self, api_url: str, headers: Dict[str, str] = None):
    async with httpx.AsyncClient() as client:
        response = await client.get(api_url, headers=headers or {})
        return response.json()
```

## Data Model

Each internship posting includes:

```typescript
interface Internship {
  id: string;
  title: string;
  company: string;
  location: string;
  description: string;
  requirements?: string;
  salary?: string;
  duration?: string;
  posted_date: string;
  source_url: string;
  source: string;
  remote?: boolean;
}
```

## Configuration

### Environment Variables

Create a `.env` file in the `api` directory:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# External API Keys (when integrating real APIs)
INDEED_API_KEY=your_key_here
LINKEDIN_API_KEY=your_key_here
```

### CORS Configuration

The backend is configured to allow requests from `http://localhost:3000`. Update the CORS settings in `main.py` for production:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Deployment

**Using Docker (Recommended for local & multi-machine runs)**

This repository includes a `docker-compose.yml` and Dockerfiles for both the backend and frontend. The compose file uses a host bind mount (`./data:/data`) so the SQLite database file is stored inside the project directory. This makes the setup portable across machines (no named volume required) and easy to back up.

Quick steps:

```zsh
# (1) Copy example env and edit secrets
cp .env.example .env
# (2) Ensure data directory exists so containers can write the DB file
mkdir -p ./data
# (3) Build and start services
docker compose up --build
```

Services:
- Backend: `http://localhost:8000` (OpenAPI at `/docs`)
- Frontend: `http://localhost:3000`

Persistence details:
- The SQLite file will be created at `./data/internship_app.db` on the host. Keep that directory under versioned backups if you need to preserve application data across machines or re-deploys.
- If you prefer a Docker named volume instead of a host directory, replace the `./data:/data` volume in `docker-compose.yml` with a named volume (previously `db_data:/data`).

Security & env vars:
- The compose file reads environment variables from a `.env` file in the project root. Do not commit secrets to git.

Now the usual Backend / Frontend subsections follow.

### Backend Deployment

1. **Using Docker**:
   ```dockerfile
   FROM python:3.13-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["python", "main.py"]
   ```

2. **Using Cloud Platforms**:
   - **Railway**: Connect your GitHub repo
   - **Heroku**: Add Procfile with `web: python main.py`
   - **AWS**: Use Elastic Beanstalk or Lambda

### Frontend Deployment

1. **Build the application**:
   ```bash
   cd web/internship-app-frontend
   npm run build
   ```

2. **Deploy to Vercel** (recommended):
   ```bash
   npx vercel
   ```

3. **Deploy to other platforms**:
   - **Netlify**: Connect GitHub repo
   - **AWS S3**: Upload build files
   - **DigitalOcean**: Use App Platform

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Troubleshooting

### Common Issues

1. **Port already in use**:
   - Backend: Change port in `main.py` or kill process using port 8000
   - Frontend: Change port in `package.json` or kill process using port 3000

2. **CORS errors**:
   - Ensure backend is running on port 8000
   - Check CORS configuration in `main.py`

3. **Virtual environment issues**:
   - The startup script automatically creates the virtual environment
   - If you encounter issues, delete `api/fastapi` folder and run `./start-backend.sh` again
   - Manual fix: `cd api && python3 -m venv fastapi && source fastapi/bin/activate && pip install -r requirements.txt`

4. **Module not found**:
   - Ensure virtual environment is activated
   - Run `pip install -r requirements.txt`

5. **Frontend not loading**:
   - Check if backend is running
   - Verify API endpoints are accessible
   - Check browser console for errors

6. **Startup script permissions**:
   - If scripts are not executable: `chmod +x start-backend.sh start-frontend.sh`

7. **"Files Too Large" error in Git**:
   - This happens when `node_modules` or Python virtual environments are accidentally committed
   - The `.gitignore` file should prevent this automatically
   - If you see this error, remove large files: `git rm -r --cached node_modules/ api/fastapi/`
   - Then commit: `git add .gitignore && git commit -m "Add gitignore"`

8. **API Rate Limiting**:
   - The Fantastic Jobs API has rate limits
   - If you hit limits, the app falls back to mock data
   - Consider upgrading your RapidAPI plan for higher limits

9. **WSL (Windows Subsystem for Linux) Issues**:
   - **Node.js not found**: Install Node.js in WSL: `curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - && sudo apt-get install -y nodejs`
   - **Permission denied**: Make script executable: `chmod +x start-frontend.sh`
   - **Port conflicts**: Windows might be using port 3000, try: `npm run dev -- -p 3001`
   - **Access from Windows**: Use `http://localhost:3000` in Windows browser
   - **WSL networking**: If localhost doesn't work, try the WSL IP: `http://$(hostname -I | awk '{print $1}'):3000`

### Getting Help

- Check the API documentation at `http://localhost:8000/docs`
- Review the browser console for frontend errors
- Check the terminal output for backend errors

## Access Your Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs