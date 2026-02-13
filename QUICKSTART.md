# Pokemon GO News Webapp - Quick Start Guide

Get up and running in 5 minutes!

## Step 1: Get an Anthropic API Key

1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Navigate to API Keys
4. Create a new API key and copy it

## Step 2: Backend Setup

Open a terminal and run:

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env  # Windows
# OR
cp .env.example .env    # macOS/Linux
```

Now edit the `.env` file and add your Anthropic API key:
```
ANTHROPIC_API_KEY=your_api_key_here
```

Start the backend:
```bash
python app.py
```

You should see:
- "Database initialized successfully!"
- "Scheduler started"
- "Running initial scrape..."
- "Running on http://0.0.0.0:5000"

## Step 3: Frontend Setup

Open a NEW terminal (keep backend running) and run:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env file
copy .env.example .env  # Windows
# OR
cp .env.example .env    # macOS/Linux

# Start React app
npm start
```

The app will automatically open at `http://localhost:3000`

## Step 4: Explore!

You're all set! Try these pages:

- **News Feed** (`/`) - Latest Pokemon GO news with AI summaries
- **Events List** (`/events`) - Browse upcoming events
- **Calendar** (`/calendar`) - Visual calendar of all events

## Troubleshooting

### Backend won't start
- Make sure Python 3.8+ is installed: `python --version`
- Verify your API key is correct in `.env`
- Check if port 5000 is already in use

### Frontend won't connect to backend
- Make sure backend is running (check terminal)
- Verify `REACT_APP_API_URL=http://localhost:5000` in frontend/.env
- Try refreshing the page

### No news/events showing
- Wait a moment for the initial scrape to complete
- Check backend terminal for error messages
- Manually trigger a scrape: `curl -X POST http://localhost:5000/api/scrape`

## Next Steps

- Filter events by type (Community Day, Raids, etc.)
- Click on events to see full details
- Browse news from different sources
- Check the calendar for upcoming dates

Enjoy your Pokemon GO News Hub! 🎉
