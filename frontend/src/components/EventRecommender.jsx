import React, { useState } from 'react';
import { assistantAPI } from '../services/api';

const EventRecommender = () => {
  const [preferences, setPreferences] = useState({
    playstyle: 'moderate',
    goals: [],
    time_available: 'moderate',
    additional_notes: '',
  });
  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(false);
  const [eventsAnalyzed, setEventsAnalyzed] = useState(0);

  const playstyleOptions = [
    { value: 'casual', label: 'Casual', description: 'I play occasionally when I have time' },
    { value: 'moderate', label: 'Moderate', description: 'I play regularly but not obsessively' },
    { value: 'hardcore', label: 'Hardcore', description: 'I play daily and optimize everything' },
  ];

  const goalOptions = [
    { value: 'shiny_hunting', label: 'Shiny Hunting', icon: '✨' },
    { value: 'pvp', label: 'PvP/GO Battle League', icon: '⚔️' },
    { value: 'raids', label: 'Raid Battles', icon: '🎯' },
    { value: 'collecting', label: 'Pokédex Completion', icon: '📖' },
    { value: 'xp', label: 'XP Grinding/Leveling', icon: '⬆️' },
    { value: 'stardust', label: 'Stardust Farming', icon: '⭐' },
  ];

  const timeOptions = [
    { value: 'limited', label: 'Limited', description: '1-2 hours per week' },
    { value: 'moderate', label: 'Moderate', description: '3-7 hours per week' },
    { value: 'plenty', label: 'Plenty', description: '8+ hours per week' },
  ];

  const handlePlaystyleChange = (value) => {
    setPreferences({ ...preferences, playstyle: value });
  };

  const handleGoalToggle = (goal) => {
    const newGoals = preferences.goals.includes(goal)
      ? preferences.goals.filter((g) => g !== goal)
      : [...preferences.goals, goal];
    setPreferences({ ...preferences, goals: newGoals });
  };

  const handleTimeChange = (value) => {
    setPreferences({ ...preferences, time_available: value });
  };

  const handleNotesChange = (e) => {
    setPreferences({ ...preferences, additional_notes: e.target.value });
  };

  const handleGetRecommendations = async () => {
    setLoading(true);
    setRecommendations(null);

    try {
      const response = await assistantAPI.getEventRecommendations(preferences);

      if (response.success) {
        setRecommendations(response.recommendations);
        setEventsAnalyzed(response.events_analyzed || 0);
      } else {
        setRecommendations('Sorry, I encountered an error getting recommendations. Please try again!');
        setEventsAnalyzed(0);
      }
    } catch (err) {
      console.error('Error getting recommendations:', err);
      setRecommendations('Sorry, I encountered an error. Please try again later!');
      setEventsAnalyzed(0);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-pogo-dark mb-2">
          🎯 Smart Event Recommender
        </h1>
        <p className="text-gray-600">
          Tell me about your playstyle and goals, and I'll recommend which events to prioritize!
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Preferences Form */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-bold text-pogo-dark mb-4">Your Preferences</h2>

          {/* Playstyle */}
          <div className="mb-6">
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Playstyle
            </label>
            <div className="space-y-2">
              {playstyleOptions.map((option) => (
                <button
                  key={option.value}
                  onClick={() => handlePlaystyleChange(option.value)}
                  className={`w-full text-left px-4 py-3 rounded-lg border-2 transition-colors ${
                    preferences.playstyle === option.value
                      ? 'border-pogo-blue bg-pogo-light text-pogo-dark'
                      : 'border-gray-300 hover:border-gray-400'
                  }`}
                >
                  <div className="font-semibold">{option.label}</div>
                  <div className="text-sm text-gray-600">{option.description}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Goals */}
          <div className="mb-6">
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Primary Goals (select all that apply)
            </label>
            <div className="grid grid-cols-2 gap-2">
              {goalOptions.map((goal) => (
                <button
                  key={goal.value}
                  onClick={() => handleGoalToggle(goal.value)}
                  className={`px-3 py-2 rounded-lg border-2 transition-colors text-sm ${
                    preferences.goals.includes(goal.value)
                      ? 'border-pogo-blue bg-pogo-light text-pogo-dark'
                      : 'border-gray-300 hover:border-gray-400'
                  }`}
                >
                  <span className="mr-1">{goal.icon}</span>
                  {goal.label}
                </button>
              ))}
            </div>
          </div>

          {/* Time Available */}
          <div className="mb-6">
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Time Available to Play
            </label>
            <div className="space-y-2">
              {timeOptions.map((option) => (
                <button
                  key={option.value}
                  onClick={() => handleTimeChange(option.value)}
                  className={`w-full text-left px-4 py-3 rounded-lg border-2 transition-colors ${
                    preferences.time_available === option.value
                      ? 'border-pogo-blue bg-pogo-light text-pogo-dark'
                      : 'border-gray-300 hover:border-gray-400'
                  }`}
                >
                  <div className="font-semibold">{option.label}</div>
                  <div className="text-sm text-gray-600">{option.description}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Additional Notes */}
          <div className="mb-6">
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Additional Notes (Optional)
            </label>
            <textarea
              value={preferences.additional_notes}
              onChange={handleNotesChange}
              placeholder="Any other preferences or constraints? (e.g., 'I need more Candy XL', 'Looking to build a PvP team', etc.)"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pogo-blue focus:border-transparent resize-none"
              rows="3"
            />
          </div>

          {/* Submit Button */}
          <button
            onClick={handleGetRecommendations}
            disabled={loading || preferences.goals.length === 0}
            className="w-full px-6 py-3 bg-pogo-blue text-white rounded-lg hover:bg-pogo-red transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed font-semibold"
          >
            {loading ? 'Analyzing Events...' : 'Get Recommendations'}
          </button>

          {preferences.goals.length === 0 && (
            <p className="text-sm text-red-600 mt-2">
              Please select at least one goal to get recommendations
            </p>
          )}
        </div>

        {/* Recommendations Display */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-bold text-pogo-dark mb-4">
            Recommendations
          </h2>

          {!recommendations && !loading && (
            <div className="text-center py-12">
              <div className="text-6xl mb-4">🎯</div>
              <p className="text-gray-600">
                Select your preferences and click "Get Recommendations" to see personalized event suggestions!
              </p>
            </div>
          )}

          {loading && (
            <div className="text-center py-12">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-pogo-blue mb-4"></div>
              <p className="text-gray-600">
                Analyzing upcoming events and matching them to your preferences...
              </p>
            </div>
          )}

          {recommendations && !loading && (
            <div>
              {eventsAnalyzed > 0 && (
                <div className="bg-pogo-light border border-pogo-blue rounded-lg px-4 py-2 mb-4">
                  <p className="text-sm text-pogo-dark">
                    ✓ Analyzed <strong>{eventsAnalyzed}</strong> upcoming event{eventsAnalyzed !== 1 ? 's' : ''}
                  </p>
                </div>
              )}

              <div className="prose max-w-none">
                <div className="whitespace-pre-wrap text-gray-800 leading-relaxed">
                  {recommendations}
                </div>
              </div>

              <button
                onClick={handleGetRecommendations}
                className="mt-6 w-full px-6 py-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors font-semibold"
              >
                🔄 Refresh Recommendations
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default EventRecommender;
