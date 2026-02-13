import React, { useState, useEffect, useCallback } from 'react';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
import { eventsAPI } from '../services/api';
import { format, isSameDay } from 'date-fns';

const EventCalendar = () => {
  const [date, setDate] = useState(new Date());
  const [events, setEvents] = useState([]);
  const [selectedDateEvents, setSelectedDateEvents] = useState([]);
  const [loading, setLoading] = useState(false);

  const filterEventsForDate = useCallback((selectedDate, allEvents) => {
    const eventsOnDate = allEvents.filter((event) => {
      if (!event.start) return false;
      try {
        const eventDate = new Date(event.start);
        return isSameDay(eventDate, selectedDate);
      } catch (e) {
        return false;
      }
    });
    setSelectedDateEvents(eventsOnDate);
  }, []);

  const loadCalendarEvents = useCallback(async (month, year) => {
    setLoading(true);
    try {
      const response = await eventsAPI.getCalendar(month, year);
      if (response.success) {
        setEvents(response.data);
        filterEventsForDate(date, response.data);
      }
    } catch (error) {
      console.error('Error loading calendar events:', error);
    } finally {
      setLoading(false);
    }
  }, [date, filterEventsForDate]);

  useEffect(() => {
    loadCalendarEvents(date.getMonth() + 1, date.getFullYear());
  }, [date, loadCalendarEvents]);

  const handleDateChange = (newDate) => {
    setDate(newDate);
    filterEventsForDate(newDate, events);
  };

  const handleMonthChange = ({ activeStartDate }) => {
    setDate(activeStartDate);
  };

  const tileContent = ({ date, view }) => {
    if (view !== 'month') return null;

    const eventsOnDay = events.filter((event) => {
      if (!event.start) return false;
      try {
        const eventDate = new Date(event.start);
        return isSameDay(eventDate, date);
      } catch (e) {
        return false;
      }
    });

    if (eventsOnDay.length > 0) {
      return (
        <div className="flex justify-center mt-1">
          <span className="w-2 h-2 bg-pogo-red rounded-full"></span>
        </div>
      );
    }
    return null;
  };

  const getEventTypeColor = (type) => {
    const colors = {
      'Community Day': 'border-green-500',
      'Spotlight Hour': 'border-yellow-500',
      'Raid Event': 'border-red-500',
      'GO Battle League': 'border-blue-500',
      'Research Event': 'border-purple-500',
      'GO Fest': 'border-pink-500',
      'Special Event': 'border-indigo-500',
    };
    return colors[type] || 'border-gray-500';
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Calendar */}
      <div className="lg:col-span-2 bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-pogo-dark mb-4">
          Event Calendar
        </h2>
        {loading && <p className="text-gray-500 mb-4">Loading events...</p>}
        <div className="calendar-container">
          <Calendar
            onChange={handleDateChange}
            onActiveStartDateChange={handleMonthChange}
            value={date}
            tileContent={tileContent}
            className="rounded-lg border-0 shadow-sm w-full"
          />
        </div>
      </div>

      {/* Events for Selected Date */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-xl font-bold text-pogo-dark mb-4">
          Events on {format(date, 'MMM dd, yyyy')}
        </h3>

        {selectedDateEvents.length === 0 ? (
          <p className="text-gray-500 text-sm">No events on this date</p>
        ) : (
          <div className="space-y-4">
            {selectedDateEvents.map((event) => (
              <div
                key={event.id}
                className={`border-l-4 ${getEventTypeColor(
                  event.type
                )} bg-gray-50 p-4 rounded-r-md`}
              >
                <h4 className="font-semibold text-pogo-dark mb-1">
                  {event.title}
                </h4>
                {event.type && (
                  <span className="text-xs text-gray-600 font-medium">
                    {event.type}
                  </span>
                )}
                {event.summary && (
                  <p className="text-sm text-gray-700 mt-2">{event.summary}</p>
                )}
                {event.url && (
                  <a
                    href={event.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-pogo-blue hover:text-pogo-red text-sm font-semibold mt-2 inline-block"
                  >
                    View Details →
                  </a>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default EventCalendar;
