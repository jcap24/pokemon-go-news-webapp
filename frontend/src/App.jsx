import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import NewsFeed from './components/NewsFeed';
import EventsList from './components/EventsList';
import EventCalendar from './components/EventCalendar';
import RaidCountersPage from './components/RaidCountersPage';

const Navigation = () => {
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'News', icon: '📰' },
    { path: '/events', label: 'Events', icon: '🎉' },
    { path: '/calendar', label: 'Calendar', icon: '📅' },
    { path: '/raids', label: 'Raid Counters', icon: '⚔️' },
  ];

  return (
    <nav className="bg-gradient-to-r from-pogo-blue to-pogo-red shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center">
            <h1 className="text-white text-2xl font-bold">
              ⚡ Pokemon GO News Hub
            </h1>
          </div>

          {/* Navigation Links */}
          <div className="flex space-x-4">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`px-4 py-2 rounded-lg font-semibold transition-colors ${
                  location.pathname === item.path
                    ? 'bg-white text-pogo-blue'
                    : 'text-white hover:bg-white/20'
                }`}
              >
                <span className="mr-2">{item.icon}</span>
                {item.label}
              </Link>
            ))}
          </div>
        </div>
      </div>
    </nav>
  );
};

const Footer = () => {
  return (
    <footer className="bg-pogo-dark text-white py-8 mt-12">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* About */}
          <div>
            <h3 className="text-lg font-bold mb-3">About Pokemon GO News Hub</h3>
            <p className="text-gray-400 text-sm">
              Your one-stop destination for all Pokemon GO news and events.
              Powered by AI summarization to help you stay informed quickly.
            </p>
          </div>

          {/* Sources */}
          <div>
            <h3 className="text-lg font-bold mb-3">News Sources</h3>
            <ul className="text-gray-400 text-sm space-y-1">
              <li>• LeekDuck</li>
              <li>• Official Pokemon GO Blog</li>
              <li>• The Silph Road</li>
            </ul>
          </div>

          {/* Info */}
          <div>
            <h3 className="text-lg font-bold mb-3">Features</h3>
            <ul className="text-gray-400 text-sm space-y-1">
              <li>• AI-Powered Event Summaries</li>
              <li>• Real-time News Updates</li>
              <li>• Interactive Event Calendar</li>
              <li>• Raid Boss Counters</li>
              <li>• Multi-Source Aggregation</li>
            </ul>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-gray-700 text-center">
          <p className="text-gray-500 text-sm">
            © 2024 Pokemon GO News Hub. Not affiliated with Niantic or Pokemon Company.
          </p>
        </div>
      </div>
    </footer>
  );
};

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-pogo-light flex flex-col">
        <Navigation />

        <main className="container mx-auto px-4 py-8 flex-grow">
          <Routes>
            <Route path="/" element={<NewsFeed />} />
            <Route path="/events" element={<EventsList />} />
            <Route path="/calendar" element={<EventCalendar />} />
            <Route path="/raids" element={<RaidCountersPage />} />
          </Routes>
        </main>

        <Footer />
      </div>
    </Router>
  );
}

export default App;
