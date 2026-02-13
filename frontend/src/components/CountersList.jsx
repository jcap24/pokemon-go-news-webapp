import React from 'react';

const CountersList = ({ counters }) => {
  const getRankBadgeColor = (rank) => {
    if (rank === 1) return 'bg-yellow-500 text-white'; // Gold
    if (rank === 2) return 'bg-gray-400 text-white'; // Silver
    if (rank === 3) return 'bg-orange-600 text-white'; // Bronze
    return 'bg-gray-200 text-gray-700';
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
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <div className="px-6 py-4 bg-pogo-dark">
        <h2 className="text-xl font-bold text-white">Best Counters</h2>
      </div>

      {/* Desktop Table View */}
      <div className="hidden md:block overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-100">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">
                Rank
              </th>
              <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">
                Pokemon
              </th>
              <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">
                Type
              </th>
              <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">
                Fast Move
              </th>
              <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">
                Charge Move
              </th>
              <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">
                DPS
              </th>
              <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">
                TDO
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {counters.map((counter) => (
              <tr
                key={counter.id}
                className="hover:bg-gray-50 transition-colors"
              >
                {/* Rank */}
                <td className="px-4 py-4">
                  <span
                    className={`inline-flex items-center justify-center w-8 h-8 rounded-full ${getRankBadgeColor(
                      counter.rank
                    )} font-bold text-sm`}
                  >
                    {counter.rank}
                  </span>
                </td>

                {/* Pokemon Name */}
                <td className="px-4 py-4">
                  <div className="flex items-center space-x-2">
                    <span className="font-semibold text-pogo-dark">
                      {counter.pokemon_name}
                    </span>
                    <div className="flex gap-1">
                      {counter.is_shadow && (
                        <span className="bg-purple-600 text-white text-xs px-2 py-1 rounded-full">
                          Shadow
                        </span>
                      )}
                      {counter.is_mega && (
                        <span className="bg-pink-600 text-white text-xs px-2 py-1 rounded-full">
                          Mega
                        </span>
                      )}
                      {counter.is_legendary && (
                        <span className="bg-yellow-600 text-white text-xs px-2 py-1 rounded-full">
                          Legendary
                        </span>
                      )}
                    </div>
                  </div>
                </td>

                {/* Types */}
                <td className="px-4 py-4">
                  {counter.pokemon_types && counter.pokemon_types.length > 0 && (
                    <div className="flex gap-1">
                      {counter.pokemon_types.map((type, idx) => (
                        <span
                          key={idx}
                          className={`${getTypeColor(type)} text-white text-xs px-2 py-1 rounded-full`}
                        >
                          {type}
                        </span>
                      ))}
                    </div>
                  )}
                </td>

                {/* Fast Move */}
                <td className="px-4 py-4">
                  <span className="text-gray-700 text-sm">
                    {counter.fast_move || '-'}
                  </span>
                </td>

                {/* Charge Move */}
                <td className="px-4 py-4">
                  <span className="text-gray-700 text-sm">
                    {counter.charge_move || '-'}
                  </span>
                </td>

                {/* DPS */}
                <td className="px-4 py-4">
                  {counter.dps && (
                    <span className="text-gray-700 font-semibold text-sm">
                      {counter.dps.toFixed(2)}
                    </span>
                  )}
                </td>

                {/* TDO */}
                <td className="px-4 py-4">
                  {counter.tdo && (
                    <span className="text-gray-700 font-semibold text-sm">
                      {counter.tdo.toFixed(0)}
                    </span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Mobile Card View */}
      <div className="md:hidden divide-y divide-gray-200">
        {counters.map((counter) => (
          <div key={counter.id} className="p-4">
            {/* Rank and Name */}
            <div className="flex items-center space-x-3 mb-3">
              <span
                className={`inline-flex items-center justify-center w-10 h-10 rounded-full ${getRankBadgeColor(
                  counter.rank
                )} font-bold`}
              >
                {counter.rank}
              </span>
              <div className="flex-1">
                <h3 className="font-semibold text-pogo-dark">
                  {counter.pokemon_name}
                </h3>
                <div className="flex gap-1 mt-1 flex-wrap">
                  {counter.is_shadow && (
                    <span className="bg-purple-600 text-white text-xs px-2 py-1 rounded-full">
                      Shadow
                    </span>
                  )}
                  {counter.is_mega && (
                    <span className="bg-pink-600 text-white text-xs px-2 py-1 rounded-full">
                      Mega
                    </span>
                  )}
                  {counter.is_legendary && (
                    <span className="bg-yellow-600 text-white text-xs px-2 py-1 rounded-full">
                      Legendary
                    </span>
                  )}
                </div>
              </div>
            </div>

            {/* Types */}
            {counter.pokemon_types && counter.pokemon_types.length > 0 && (
              <div className="mb-2">
                <div className="flex gap-1">
                  {counter.pokemon_types.map((type, idx) => (
                    <span
                      key={idx}
                      className={`${getTypeColor(type)} text-white text-xs px-2 py-1 rounded-full`}
                    >
                      {type}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Moves and Stats */}
            <div className="grid grid-cols-2 gap-2 text-sm">
              <div>
                <span className="text-gray-600">Fast:</span>{' '}
                <span className="text-gray-800">{counter.fast_move || '-'}</span>
              </div>
              <div>
                <span className="text-gray-600">Charge:</span>{' '}
                <span className="text-gray-800">{counter.charge_move || '-'}</span>
              </div>
              {counter.dps && (
                <div>
                  <span className="text-gray-600">DPS:</span>{' '}
                  <span className="text-gray-800 font-semibold">
                    {counter.dps.toFixed(2)}
                  </span>
                </div>
              )}
              {counter.tdo && (
                <div>
                  <span className="text-gray-600">TDO:</span>{' '}
                  <span className="text-gray-800 font-semibold">
                    {counter.tdo.toFixed(0)}
                  </span>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default CountersList;
