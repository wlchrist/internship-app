'use client';

import { useState, useEffect } from 'react';
import InternshipCard from './components/InternshipCard';
import LoadingSpinner from './components/LoadingSpinner';

interface Internship {
  id: string;
  title: string;
  company: string;
  location: string;
  description: string;
  requirements?: string;
  salary?: string;
  duration?: string;
  posted_date: string;
  source_url: string;
  source: string;
  remote?: boolean;
  job_type?: string;
}

export default function Home() {
  const [internships, setInternships] = useState<Internship[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchInternships = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:8000/internships');
      if (!response.ok) {
        throw new Error('Failed to fetch internships');
      }
      const data = await response.json();
      setInternships(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    try {
      setLoading(true);
      console.log('Triggering refresh on backend');
      // Trigger refresh on backend
      await fetch('http://localhost:8000/internships/refresh');
      console.log('Refresh triggered, fetching updated data');
      // Then fetch updated data
      await fetchInternships();
    } catch (err) {
      console.error('Error refreshing:', err);
      setError(err instanceof Error ? err.message : 'Failed to refresh');
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchInternships();
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            🎯 Internship Aggregator
          </h1>
          <p className="text-lg text-gray-600 mb-6">
            Discover amazing internship opportunities from top companies
          </p>
          
          
          <div className="flex justify-center items-center gap-4 mb-6">
            <button
              onClick={handleRefresh}
              disabled={loading}
              className="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white px-6 py-2 rounded-lg font-medium transition-colors duration-200 flex items-center gap-2"
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  Refreshing...
                </>
              ) : (
                <>
                  🔄 Refresh Data
                </>
              )}
            </button>
            
            {!loading && internships.length > 0 && (
              <span className="text-sm text-gray-500">
                {internships.length} internships available
              </span>
            )}
          </div>
        </div>

        {/* Error State */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <div className="flex">
              <div className="flex-shrink-0">
                <span className="text-red-400">⚠️</span>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">
                  Error loading internships
                </h3>
                <div className="mt-2 text-sm text-red-700">
                  {error}
                </div>
                <div className="mt-4">
                  <button
                    onClick={fetchInternships}
                    className="bg-red-100 hover:bg-red-200 text-red-800 px-3 py-1 rounded text-sm font-medium"
                  >
                    Try Again
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Loading State */}
        {loading && internships.length === 0 && <LoadingSpinner />}

        {/* Internships Grid */}
        {!loading && internships.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {internships.map((internship) => (
              <InternshipCard key={internship.id} internship={internship} />
            ))}
          </div>
        )}

        {/* Empty State */}
        {!loading && internships.length === 0 && !error && (
          <div className="text-center py-12">
            <div className="text-gray-400 text-6xl mb-4">📋</div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              No internships found
            </h3>
            <p className="text-gray-500 mb-4">
              Try refreshing the data or check back later.
            </p>
            <button
              onClick={fetchInternships}
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium"
            >
              Refresh Data
            </button>
          </div>
        )}
      </div>
    </div>
  );
}