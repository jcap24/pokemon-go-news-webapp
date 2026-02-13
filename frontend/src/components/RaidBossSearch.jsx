import React, { useState, useEffect, useRef } from 'react';
import { raidsAPI } from '../services/api';

const RaidBossSearch = ({ onBossSelect }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const [currentRaidBosses, setCurrentRaidBosses] = useState([]);
  const [loading, setLoading] = useState(false);
  const searchRef = useRef(null);

  useEffect(() => {
    // Load current raid bosses for quick select
    loadCurrentRaidBosses();

    // Click outside handler to close dropdown
    const handleClickOutside = (event) => {
      if (searchRef.current && !searchRef.current.contains(event.target)) {
        setShowDropdown(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  useEffect(() => {
    // Debounced search
    if (searchQuery.length >= 2) {
      const timeoutId = setTimeout(() => {
        performSearch(searchQuery);
      }, 300);

      return () => clearTimeout(timeoutId);
    } else {
      setSearchResults([]);
      setShowDropdown(false);
    }
    // eslint-disable-next-line
  }, [searchQuery]);

  const loadCurrentRaidBosses = async () => {
    try {
      console.log('🔍 Loading current raid bosses...');
      const response = await raidsAPI.getAll({ active: true, per_page: 50 });
      console.log('📡 API Response:', response);
      if (response.success) {
        console.log(`✅ Found ${response.data.length} raid bosses:`, response.data);
        setCurrentRaidBosses(response.data);
      } else {
        console.error('❌ API returned success: false');
      }
    } catch (err) {
      console.error('❌ Error loading current raid bosses:', err);
    }
  };

  const performSearch = async (query) => {
    setLoading(true);
    try {
      const response = await raidsAPI.search(query);
      if (response.success) {
        setSearchResults(response.data);
        setShowDropdown(true);
      }
    } catch (err) {
      console.error('Error searching raid bosses:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleBossClick = (boss) => {
    setSearchQuery(boss.name);
    setShowDropdown(false);
    onBossSelect(boss);
  };

  const getTierColor = (tier) => {
    const colors = {
      '1': 'bg-gray-400',
      '3': 'bg-yellow-500',
      '5': 'bg-purple-600',
      'Mega': 'bg-pink-600',
      'Shadow': 'bg-gray-800',
    };
    return colors[tier] || 'bg-gray-500';
  };

  const getTypeColor = (type) => {
    const colors = {
      Normal: 'bg-gray-400',
      Fire: 'bg-red-500',
      Water: 'bg-blue-500',
      Electric: 'bg-yellow-400',
      Grass: 'bg-green-500',
      Ice: 'bg-blue-300',
      Fighting: 'bg-red-700',
      Poison: 'bg-purple-500',
      Ground: 'bg-yellow-700',
      Flying: 'bg-blue-400',
      Psychic: 'bg-pink-500',
      Bug: 'bg-green-600',
      Rock: 'bg-yellow-800',
      Ghost: 'bg-purple-700',
      Dragon: 'bg-indigo-700',
      Dark: 'bg-gray-800',
      Steel: 'bg-gray-500',
      Fairy: 'bg-pink-300',
    };
    return colors[type] || 'bg-gray-400';
  };

  return (
    <div className="space-y-6">
      {/* Search Input */}
      <div className="relative" ref={searchRef}>
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search for a raid boss (e.g., Dialga, Palkia)..."
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pogo-blue focus:border-transparent text-lg"
        />

        {loading && (
          <div className="absolute right-3 top-3">
            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-pogo-blue"></div>
          </div>
        )}

        {/* Autocomplete Dropdown */}
        {showDropdown && searchResults.length > 0 && (
          <div className="absolute z-10 w-full mt-2 bg-white border border-gray-300 rounded-lg shadow-lg max-h-96 overflow-y-auto">
            {searchResults.map((boss) => (
              <div
                key={boss.id}
                onClick={() => handleBossClick(boss)}
                className="px-4 py-3 hover:bg-gray-100 cursor-pointer border-b border-gray-200 last:border-b-0"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <span className="font-semibold text-pogo-dark">{boss.name}</span>
                    {boss.types && boss.types.length > 0 && (
                      <div className="flex gap-1">
                        {boss.types.map((type, idx) => (
                          <span
                            key={idx}
                            className={`${getTypeColor(type)} text-white text-xs px-2 py-1 rounded-full`}
                          >
                            {type}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                  {boss.tier && (
                    <span
                      className={`${getTierColor(boss.tier)} text-white text-xs font-semibold px-3 py-1 rounded-full`}
                    >
                      Tier {boss.tier}
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Quick Select Grid - Current Raid Bosses */}
      {currentRaidBosses.length > 0 ? (
        <div>
          <h3 className="text-lg font-semibold text-pogo-dark mb-3">
            Current Raid Bosses ({currentRaidBosses.length})
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
            {currentRaidBosses.map((boss) => (
              <div
                key={boss.id}
                onClick={() => handleBossClick(boss)}
                className="bg-white rounded-lg shadow-md p-4 cursor-pointer hover:shadow-lg hover:scale-105 transition-all duration-200"
              >
                <div className="flex flex-col items-center space-y-2">
                  <span className="font-semibold text-pogo-dark text-center">
                    {boss.name}
                  </span>
                  {boss.tier && (
                    <span
                      className={`${getTierColor(boss.tier)} text-white text-xs font-semibold px-3 py-1 rounded-full`}
                    >
                      Tier {boss.tier}
                    </span>
                  )}
                  {boss.types && boss.types.length > 0 && (
                    <div className="flex gap-1 flex-wrap justify-center">
                      {boss.types.map((type, idx) => (
                        <span
                          key={idx}
                          className={`${getTypeColor(type)} text-white text-xs px-2 py-1 rounded-full`}
                        >
                          {type}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div className="text-center py-8 bg-gray-50 rounded-lg">
          <p className="text-gray-500">Loading raid bosses... (Check console for details)</p>
        </div>
      )}
    </div>
  );
};

export default RaidBossSearch;
