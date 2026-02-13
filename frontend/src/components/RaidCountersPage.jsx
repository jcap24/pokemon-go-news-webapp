import React, { useState, useEffect } from 'react';
import { raidsAPI } from '../services/api';
import RaidBossSearch from './RaidBossSearch';
import RaidBossInfo from './RaidBossInfo';
import CountersList from './CountersList';

const RaidCountersPage = () => {
  const [selectedBoss, setSelectedBoss] = useState(null);
  const [bossData, setBossData] = useState(null);
  const [counters, setCounters] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    include_shadow: true,
    include_mega: true,
    include_legendary: true,
  });

  useEffect(() => {
    if (selectedBoss) {
      loadCounters(selectedBoss);
    }
    // eslint-disable-next-line
  }, [selectedBoss, filters]);

  const loadCounters = async (bossName) => {
    setLoading(true);
    setError(null);

    try {
      const response = await raidsAPI.getCounters(bossName, {
        limit: 20,
        ...filters,
      });

      if (response.success) {
        setBossData(response.data.boss);
        setCounters(response.data.counters);
      } else {
        setError(`Failed to load counters for ${bossName}`);
      }
    } catch (err) {
      setError('Error connecting to server. Please try again later.');
      console.error('Error loading counters:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleBossSelect = (boss) => {
    setSelectedBoss(boss.name);
  };

  const handleFilterChange = (filterName, value) => {
    setFilters({ ...filters, [filterName]: value });
  };

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-pogo-dark mb-2">
          Raid Counters
        </h1>
        <p className="text-gray-600">
          Find the best counters for any raid boss
        </p>
      </div>

      {/* Search Section */}
      <RaidBossSearch onBossSelect={handleBossSelect} />

      {/* Error State */}
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mt-6">
          <p>{error}</p>
        </div>
      )}

      {/* Loading State */}
      {loading && (
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-pogo-blue"></div>
          <p className="mt-4 text-gray-600">Loading counters...</p>
        </div>
      )}

      {/* Boss Info and Counters */}
      {!loading && bossData && counters.length > 0 && (
        <div className="mt-6 space-y-6">
          {/* Boss Information */}
          <RaidBossInfo boss={bossData} />

          {/* Filter Controls */}
          <div className="bg-white rounded-lg shadow-md p-4">
            <h3 className="text-lg font-semibold text-pogo-dark mb-3">
              Filter Counters
            </h3>
            <div className="flex flex-wrap gap-4">
              <label className="flex items-center space-x-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={filters.include_shadow}
                  onChange={(e) => handleFilterChange('include_shadow', e.target.checked)}
                  className="w-4 h-4 text-pogo-blue rounded focus:ring-2 focus:ring-pogo-blue"
                />
                <span className="text-gray-700">Include Shadow</span>
              </label>

              <label className="flex items-center space-x-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={filters.include_mega}
                  onChange={(e) => handleFilterChange('include_mega', e.target.checked)}
                  className="w-4 h-4 text-pogo-blue rounded focus:ring-2 focus:ring-pogo-blue"
                />
                <span className="text-gray-700">Include Mega</span>
              </label>

              <label className="flex items-center space-x-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={filters.include_legendary}
                  onChange={(e) => handleFilterChange('include_legendary', e.target.checked)}
                  className="w-4 h-4 text-pogo-blue rounded focus:ring-2 focus:ring-pogo-blue"
                />
                <span className="text-gray-700">Include Legendary</span>
              </label>
            </div>
          </div>

          {/* Counters List */}
          <CountersList counters={counters} />
        </div>
      )}

      {/* Empty State */}
      {!loading && !error && !bossData && (
        <div className="text-center py-12 bg-white rounded-lg shadow-md mt-6">
          <div className="text-6xl mb-4">🔍</div>
          <p className="text-gray-500 text-lg">
            Search for a raid boss to see the best counters
          </p>
        </div>
      )}

      {/* No Counters State */}
      {!loading && bossData && counters.length === 0 && (
        <div className="text-center py-12 bg-white rounded-lg shadow-md mt-6">
          <div className="text-6xl mb-4">📊</div>
          <p className="text-gray-500 text-lg">
            No counters found for {bossData.name}
          </p>
        </div>
      )}
    </div>
  );
};

export default RaidCountersPage;
