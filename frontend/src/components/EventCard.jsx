import React from 'react';
import { format } from 'date-fns';

const EventCard = ({ event }) => {
  const formatDate = (dateString) => {
    if (!dateString) return 'TBA';
    try {
      return format(new Date(dateString), 'MMM dd, yyyy HH:mm');
    } catch (e) {
      return dateString;
    }
  };

  const getEventTypeColor = (type) => {
    const colors = {
      'Community Day': 'bg-green-500',
      'Spotlight Hour': 'bg-yellow-500',
      'Raid Event': 'bg-red-500',
      'GO Battle League': 'bg-blue-500',
      'Research Event': 'bg-purple-500',
      'GO Fest': 'bg-pink-500',
      'Special Event': 'bg-indigo-500',
      'Season Event': 'bg-orange-500',
    };
    return colors[type] || 'bg-gray-500';
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow duration-200">
      {/* Event Type Badge */}
      {event.event_type && (
        <span
          className={`inline-block ${getEventTypeColor(
            event.event_type
          )} text-white text-xs font-semibold px-3 py-1 rounded-full mb-3`}
        >
          {event.event_type}
        </span>
      )}

      {/* Event Title */}
      <h3 className="text-xl font-bold text-pogo-dark mb-2">{event.title}</h3>

      {/* Event Dates */}
      <div className="text-sm text-gray-600 mb-3">
        <p>
          <span className="font-semibold">Start:</span>{' '}
          {formatDate(event.start_date)}
        </p>
        {event.end_date && (
          <p>
            <span className="font-semibold">End:</span>{' '}
            {formatDate(event.end_date)}
          </p>
        )}
      </div>

      {/* AI Summary */}
      {event.summary && (
        <div className="bg-pogo-light p-4 rounded-md mb-4">
          <p className="text-sm text-gray-800 leading-relaxed">
            {event.summary}
          </p>
        </div>
      )}

      {/* Description */}
      {event.description && (
        <p className="text-gray-700 text-sm mb-4 line-clamp-3">
          {event.description}
        </p>
      )}

      {/* Footer */}
      <div className="flex justify-between items-center mt-4 pt-4 border-t border-gray-200">
        <span className="text-xs text-gray-500">{event.source}</span>
        {event.url && (
          <a
            href={event.url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-pogo-blue hover:text-pogo-red font-semibold text-sm transition-colors"
          >
            Read More →
          </a>
        )}
      </div>
    </div>
  );
};

export default EventCard;
