import React from 'react';
import { format } from 'date-fns';

const NewsItem = ({ news }) => {
  const formatDate = (dateString) => {
    if (!dateString) return '';
    try {
      return format(new Date(dateString), 'MMM dd, yyyy');
    } catch (e) {
      return dateString;
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow duration-200 mb-4">
      {/* News Title */}
      <h3 className="text-xl font-bold text-pogo-dark mb-2">{news.title}</h3>

      {/* Date and Source */}
      <div className="flex items-center gap-3 text-sm text-gray-600 mb-3">
        {news.published_date && (
          <span className="flex items-center">
            <svg
              className="w-4 h-4 mr-1"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
              />
            </svg>
            {formatDate(news.published_date)}
          </span>
        )}
        <span className="text-pogo-blue font-semibold">{news.source}</span>
      </div>

      {/* AI Summary */}
      {news.summary && (
        <div className="bg-blue-50 border-l-4 border-pogo-blue p-4 rounded-r-md mb-4">
          <p className="text-sm text-gray-800 leading-relaxed font-medium">
            📋 {news.summary}
          </p>
        </div>
      )}

      {/* Content Preview */}
      {news.content && (
        <p className="text-gray-700 text-sm mb-4 line-clamp-4">
          {news.content}
        </p>
      )}

      {/* Read More Link */}
      {news.url && (
        <a
          href={news.url}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center text-pogo-blue hover:text-pogo-red font-semibold text-sm transition-colors"
        >
          Read Full Article
          <svg
            className="w-4 h-4 ml-1"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
            />
          </svg>
        </a>
      )}
    </div>
  );
};

export default NewsItem;
