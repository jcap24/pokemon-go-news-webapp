import React from 'react';

const RaidBossInfo = ({ boss }) => {
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
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex items-start justify-between mb-4">
        <div>
          <h2 className="text-2xl font-bold text-pogo-dark mb-2">{boss.name}</h2>
          {boss.tier && (
            <span
              className={`${getTierColor(boss.tier)} text-white text-sm font-semibold px-4 py-1 rounded-full inline-block`}
            >
              Tier {boss.tier} Raid Boss
            </span>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Types */}
        {boss.types && boss.types.length > 0 && (
          <div>
            <h3 className="text-sm font-semibold text-gray-600 mb-2">Type</h3>
            <div className="flex gap-2">
              {boss.types.map((type, idx) => (
                <span
                  key={idx}
                  className={`${getTypeColor(type)} text-white text-sm font-semibold px-4 py-2 rounded-lg`}
                >
                  {type}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Weaknesses */}
        {boss.weaknesses && boss.weaknesses.length > 0 && (
          <div>
            <h3 className="text-sm font-semibold text-gray-600 mb-2">Weaknesses</h3>
            <div className="flex flex-wrap gap-2">
              {boss.weaknesses.map((weakness, idx) => (
                <span
                  key={idx}
                  className={`${getTypeColor(weakness)} text-white text-sm px-3 py-1 rounded-full`}
                >
                  {weakness}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* CP Range */}
        {boss.cp_min && boss.cp_max && (
          <div>
            <h3 className="text-sm font-semibold text-gray-600 mb-2">CP Range</h3>
            <div className="bg-pogo-light p-3 rounded-lg">
              <p className="text-pogo-dark font-semibold">
                {boss.cp_min} - {boss.cp_max}
              </p>
              {boss.cp_boosted_min && boss.cp_boosted_max && (
                <p className="text-gray-600 text-sm mt-1">
                  Boosted: {boss.cp_boosted_min} - {boss.cp_boosted_max}
                </p>
              )}
            </div>
          </div>
        )}

        {/* Weather Boost */}
        {boss.weather_boost && boss.weather_boost.length > 0 && (
          <div>
            <h3 className="text-sm font-semibold text-gray-600 mb-2">Weather Boost</h3>
            <div className="bg-pogo-light p-3 rounded-lg">
              <div className="flex flex-wrap gap-2">
                {boss.weather_boost.map((weather, idx) => (
                  <span
                    key={idx}
                    className="bg-blue-500 text-white text-sm px-3 py-1 rounded-full"
                  >
                    {weather}
                  </span>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Active Status */}
      {boss.is_active !== undefined && (
        <div className="mt-4 pt-4 border-t border-gray-200">
          <span
            className={`inline-flex items-center text-sm font-semibold ${
              boss.is_active ? 'text-green-600' : 'text-gray-500'
            }`}
          >
            <span
              className={`w-2 h-2 rounded-full mr-2 ${
                boss.is_active ? 'bg-green-600' : 'bg-gray-400'
              }`}
            ></span>
            {boss.is_active ? 'Currently Active' : 'Not Currently Active'}
          </span>
        </div>
      )}
    </div>
  );
};

export default RaidBossInfo;
