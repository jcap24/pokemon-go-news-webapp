# Pokemon GO News Webapp

A full-stack web application that aggregates Pokemon GO news from multiple sources (LeekDuck, Official Pokemon GO Blog, The Silph Road) and uses AI to generate player-friendly event summaries.

## Features

- 📰 **News Feed** - Latest Pokemon GO news from multiple sources
- 🎉 **Events List** - Browse upcoming events with AI-generated summaries
- 📅 **Interactive Calendar** - Visual calendar showing all events
- 🔍 **Smart Filtering** - Filter by event type and news source
- 🤖 **AI Summaries** - Automatic event and news summarization using Claude
- 🔄 **Auto-Updates** - Background scraping every 30 minutes

## Tech Stack

### Backend
- **Python 3.8+** with Flask
- **SQLAlchemy** for database ORM
- **BeautifulSoup4** for web scraping
- **Anthropic Claude API** for AI summarization
- **APScheduler** for background jobs
- **SQLite** database

### Frontend
- **React 18** with hooks
- **React Router** for navigation
- **Axios** for API calls
- **Tailwind CSS** for styling
- **React Calendar** for calendar view
- **date-fns** for date formatting

## Project Structure

```
pokemon-go-news-webapp/
├── backend/
│   ├── app.py                    # Flask application entry point
│   ├── requirements.txt          # Python dependencies
│   ├── .env.example             # Environment variables template
│   ├── models/                  # Database models
│   │   ├── __init__.py
│   │   └── database.py
│   ├── scrapers/                # Web scrapers
│   │   ├── __init__.py
│   │   ├── leekduck.py
│   │   ├── official_blog.py
│   │   └── silph_road.py
│   ├── services/                # Business logic
│   │   ├── __init__.py
│   │   ├── summarizer.py       # AI summarization
│   │   └── scheduler.py        # Background jobs
│   └── routes/                  # API endpoints
│       ├── __init__.py
│       ├── news.py
│       └── events.py
└── frontend/
    ├── package.json             # Node dependencies
    ├── .env.example            # Frontend environment variables
    ├── tailwind.config.js      # Tailwind configuration
    ├── public/
    │   └── index.html
    └── src/
        ├── App.jsx             # Main React component
        ├── index.js            # React entry point
        ├── components/         # React components
        │   ├── EventCard.jsx
        │   ├── EventCalendar.jsx
        │   ├── EventsList.jsx
        │   ├── FilterBar.jsx
        │   ├── NewsFeed.jsx
        │   └── NewsItem.jsx
        └── services/
            └── api.js          # API client
```

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- Anthropic API key (get one at https://console.anthropic.com/)

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```

5. Edit `.env` and add your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```

6. Run the backend server:
   ```bash
   python app.py
   ```

   The backend will:
   - Initialize the SQLite database
   - Run an initial scrape of all news sources
   - Start the Flask server on `http://localhost:5000`
   - Schedule automatic scraping every 30 minutes

### Frontend Setup

1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node dependencies:
   ```bash
   npm install
   ```

3. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```

4. (Optional) If your backend runs on a different port, update `.env`:
   ```
   REACT_APP_API_URL=http://localhost:5000
   ```

5. Start the React development server:
   ```bash
   npm start
   ```

   The frontend will open at `http://localhost:3000`

## Usage

### API Endpoints

#### News Endpoints
- `GET /api/news` - Get all news (supports pagination and source filtering)
- `GET /api/news/:id` - Get single news item
- `GET /api/news/sources` - Get list of all sources

#### Events Endpoints
- `GET /api/events` - Get all events (supports filtering by type, source, date range)
- `GET /api/events/:id` - Get single event
- `GET /api/events/calendar` - Get events for calendar view
- `GET /api/events/types` - Get list of all event types

#### Admin Endpoints
- `POST /api/scrape` - Manually trigger scraping
- `GET /api/health` - Health check

### Frontend Pages

- **/** - News feed with latest Pokemon GO news
- **/events** - List view of all upcoming events
- **/calendar** - Interactive calendar showing events

## Configuration

### Backend Environment Variables

- `ANTHROPIC_API_KEY` - Your Anthropic API key (required)
- `DATABASE_URL` - Database connection string (default: sqlite:///pokemon_go_news.db)
- `SCRAPE_INTERVAL` - Minutes between automatic scrapes (default: 30)
- `FLASK_ENV` - Flask environment (development/production)
- `PORT` - Server port (default: 5000)

### Frontend Environment Variables

- `REACT_APP_API_URL` - Backend API URL (default: http://localhost:5000)

## Development

### Running Tests

Backend:
```bash
cd backend
python -m pytest
```

Frontend:
```bash
cd frontend
npm test
```

### Building for Production

Frontend:
```bash
cd frontend
npm run build
```

## Deployment

### Backend Deployment
- Deploy to services like Render, Railway, or Heroku
- Set environment variables in platform settings
- Consider upgrading to PostgreSQL for production
- Set up monitoring and logging

### Frontend Deployment
- Deploy to Vercel or Netlify
- Configure environment variable `REACT_APP_API_URL` to point to your backend
- Build will automatically happen on deployment

## Troubleshooting

### Backend Issues

**Error: "ANTHROPIC_API_KEY not found"**
- Make sure you created a `.env` file in the backend directory
- Verify your API key is correct

**No events/news showing**
- Trigger a manual scrape: `curl -X POST http://localhost:5000/api/scrape`
- Check backend logs for scraping errors
- Some websites may have changed their HTML structure

**Database errors**
- Delete `pokemon_go_news.db` and restart the backend to recreate the database

### Frontend Issues

**"Failed to fetch" errors**
- Verify backend is running on the correct port
- Check CORS settings in backend
- Verify `REACT_APP_API_URL` in frontend `.env`

**Styling not working**
- Run `npm run build` to rebuild Tailwind
- Clear browser cache

## Future Enhancements

- [ ] User accounts and saved favorites
- [ ] Push notifications for new events
- [ ] Export events to Google Calendar
- [ ] Mobile app (React Native)
- [ ] Event reminders
- [ ] Community comments and discussions
- [ ] Redis caching for improved performance
- [ ] More news sources (Reddit, Twitter, etc.)

## License

MIT License - feel free to use this project for your own purposes!

## Disclaimer

This project is not affiliated with Niantic, Pokemon, or The Pokemon Company. All Pokemon GO related trademarks and copyrights belong to their respective owners.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
