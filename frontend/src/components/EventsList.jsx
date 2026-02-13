import React, { useState, useEffect } from 'react';
import { eventsAPI } from '../services/api';
import EventCard from './EventCard';
import FilterBar from './FilterBar';

const EventsList = () => {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    types: [],
    source: '',
    page: 1,
  });
  const [pagination, setPagination] = useState(null);

  useEffect(() => {
    loadEvents();
    // eslint-disable-next-line
  }, [filters]);

  const loadEvents = async () => {
    setLoading(true);
    setError(null);

    try {
      const params = {
        page: filters.page,
        per_page: 12,
      };

      if (filters.source) {
        params.source = filters.source;
      }

      if (filters.types && filters.types.length > 0) {
        // Note: This assumes backend supports filtering by multiple types
        // If not, you may need to filter client-side or request one type at a time
        params.type = filters.types[0];
      }

      const response = await eventsAPI.getAll(params);

      if (response.success) {
        // If multiple types are selected, filter client-side
        let filteredEvents = response.data;
        if (filters.types && filters.types.length > 1) {
          filteredEvents = response.data.filter((event) =>
            filters.types.includes(event.event_type)
          );
        }
        setEvents(filteredEvents);
        setPagination(response.pagination);
      } else {
        setError('Failed to load events');
      }
    } catch (err) {
      setError('Error connecting to server. Please try again later.');
      console.error('Error loading events:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (newFilters) => {
    setFilters({ ...filters, ...newFilters, page: 1 });
  };

  const handlePageChange = (newPage) => {
    setFilters({ ...filters, page: newPage });
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-pogo-dark mb-2">
          Upcoming Events
        </h1>
        <p className="text-gray-600">
          Browse all Pokemon GO events and special activities
        </p>
      </div>

      {/* Filters */}
      <FilterBar
        onFilterChange={handleFilterChange}
        filterType="events"
        currentFilters={filters}
      />

      {/* Loading State */}
      {loading && (
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-pogo-blue"></div>
          <p className="mt-4 text-gray-600">Loading events...</p>
        </div>
      )}

      {/* Error State */}
      {error && !loading && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          <p>{error}</p>
        </div>
      )}

      {/* Events Grid */}
      {!loading && !error && (
        <>
          {events.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-500">No events found</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {events.map((event) => (
                <EventCard key={event.id} event={event} />
              ))}
            </div>
          )}

          {/* Pagination */}
          {pagination && pagination.pages > 1 && (
            <div className="flex justify-center items-center gap-2 mt-8">
              <button
                onClick={() => handlePageChange(filters.page - 1)}
                disabled={filters.page === 1}
                className="px-4 py-2 bg-pogo-blue text-white rounded-lg disabled:bg-gray-300 disabled:cursor-not-allowed hover:bg-pogo-red transition-colors"
              >
                Previous
              </button>

              <span className="text-gray-700 px-4">
                Page {filters.page} of {pagination.pages}
              </span>

              <button
                onClick={() => handlePageChange(filters.page + 1)}
                disabled={filters.page === pagination.pages}
                className="px-4 py-2 bg-pogo-blue text-white rounded-lg disabled:bg-gray-300 disabled:cursor-not-allowed hover:bg-pogo-red transition-colors"
              >
                Next
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default EventsList;
