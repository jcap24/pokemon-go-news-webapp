import React, { useState, useEffect } from 'react';
import { eventsAPI, newsAPI } from '../services/api';

const FilterBar = ({ onFilterChange, filterType = 'events', currentFilters }) => {
  const [eventTypes, setEventTypes] = useState([]);
  const [sources, setSources] = useState([]);
  const [selectedTypes, setSelectedTypes] = useState([]);
  const [selectedSource, setSelectedSource] = useState('');

  useEffect(() => {
    if (filterType === 'events') {
      loadEventTypes();
    }
    loadSources();
  }, [filterType]);

  const loadEventTypes = async () => {
    try {
      const response = await eventsAPI.getTypes();
      if (response.success) {
        setEventTypes(response.data);
      }
    } catch (error) {
      console.error('Error loading event types:', error);
    }
  };

  const loadSources = async () => {
    try {
      const response = await newsAPI.getSources();
      if (response.success) {
        setSources(response.data);
      }
    } catch (error) {
      console.error('Error loading sources:', error);
    }
  };

  const handleTypeToggle = (type) => {
    let newTypes;
    if (selectedTypes.includes(type)) {
      newTypes = selectedTypes.filter((t) => t !== type);
    } else {
      newTypes = [...selectedTypes, type];
    }
    setSelectedTypes(newTypes);
    onFilterChange({ types: newTypes });
  };

  const handleSourceChange = (source) => {
    setSelectedSource(source);
    onFilterChange({ source });
  };

  const handleClearFilters = () => {
    setSelectedTypes([]);
    setSelectedSource('');
    onFilterChange({ types: [], source: '' });
  };

  const hasActiveFilters = selectedTypes.length > 0 || selectedSource !== '';

  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-6">
      <div className="flex flex-wrap gap-4">
        {/* Source Filter */}
        <div className="flex-1 min-w-[200px]">
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            Source
          </label>
          <select
            value={selectedSource}
            onChange={(e) => handleSourceChange(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pogo-blue focus:border-transparent"
          >
            <option value="">All Sources</option>
            {sources.map((source) => (
              <option key={source} value={source}>
                {source}
              </option>
            ))}
          </select>
        </div>

        {/* Event Type Filters (only for events) */}
        {filterType === 'events' && eventTypes.length > 0 && (
          <div className="flex-1 min-w-[300px]">
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Event Types
            </label>
            <div className="flex flex-wrap gap-2">
              {eventTypes.map((type) => (
                <button
                  key={type}
                  onClick={() => handleTypeToggle(type)}
                  className={`px-3 py-1.5 text-sm font-medium rounded-full transition-colors ${
                    selectedTypes.includes(type)
                      ? 'bg-pogo-blue text-white'
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  }`}
                >
                  {type}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Clear Filters */}
        {hasActiveFilters && (
          <div className="flex items-end">
            <button
              onClick={handleClearFilters}
              className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors font-medium text-sm"
            >
              Clear Filters
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default FilterBar;
