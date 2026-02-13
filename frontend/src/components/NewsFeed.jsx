import React, { useState, useEffect } from 'react';
import { newsAPI } from '../services/api';
import NewsItem from './NewsItem';
import FilterBar from './FilterBar';

const NewsFeed = () => {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    source: '',
    page: 1,
  });
  const [pagination, setPagination] = useState(null);

  useEffect(() => {
    loadNews();
    // eslint-disable-next-line
  }, [filters]);

  const loadNews = async () => {
    setLoading(true);
    setError(null);

    try {
      const params = {
        page: filters.page,
        per_page: 20,
      };

      if (filters.source) {
        params.source = filters.source;
      }

      const response = await newsAPI.getAll(params);

      if (response.success) {
        setNews(response.data);
        setPagination(response.pagination);
      } else {
        setError('Failed to load news');
      }
    } catch (err) {
      setError('Error connecting to server. Please try again later.');
      console.error('Error loading news:', err);
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
          Latest Pokemon GO News
        </h1>
        <p className="text-gray-600">
          Stay updated with the latest announcements and events
        </p>
      </div>

      {/* Filters */}
      <FilterBar
        onFilterChange={handleFilterChange}
        filterType="news"
        currentFilters={filters}
      />

      {/* Loading State */}
      {loading && (
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-pogo-blue"></div>
          <p className="mt-4 text-gray-600">Loading news...</p>
        </div>
      )}

      {/* Error State */}
      {error && !loading && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          <p>{error}</p>
        </div>
      )}

      {/* News List */}
      {!loading && !error && (
        <>
          {news.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-500">No news found</p>
            </div>
          ) : (
            <div className="space-y-4">
              {news.map((item) => (
                <NewsItem key={item.id} news={item} />
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

export default NewsFeed;
