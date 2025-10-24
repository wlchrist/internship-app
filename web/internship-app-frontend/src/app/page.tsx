'use client';

import { useState, useEffect, useMemo } from 'react';
import InternshipCard from './components/InternshipCard';
import LoadingSpinner from './components/LoadingSpinner';
import NotificationSubscription from './components/NotificationSubscription';
import FilterPanel from './components/FilterPanel';

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

interface FilterState {
  searchTerm: string;
  location: string;
  remoteOnly: boolean;
  salaryRange: string;
  company: string;
  jobType: string;
}

export default function Home() {
  const [internships, setInternships] = useState<Internship[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<FilterState>({
    searchTerm: '',
    location: '',
    remoteOnly: false,
    salaryRange: '',
    company: '',
    jobType: '',
  });

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

  // Filter internships based on current filters
  const filteredInternships = useMemo(() => {
    return internships.filter(internship => {
      // Search term filter
      if (filters.searchTerm) {
        const searchLower = filters.searchTerm.toLowerCase();
        const matchesSearch = 
          internship.title.toLowerCase().includes(searchLower) ||
          internship.description.toLowerCase().includes(searchLower) ||
          internship.company.toLowerCase().includes(searchLower) ||
          internship.location.toLowerCase().includes(searchLower);
        if (!matchesSearch) return false;
      }

      // Location filter
      if (filters.location && internship.location !== filters.location) {
        return false;
      }

      // Company filter
      if (filters.company && internship.company !== filters.company) {
        return false;
      }

      // Remote only filter
      if (filters.remoteOnly && !internship.remote) {
        return false;
      }

      // Salary range filter
      if (filters.salaryRange) {
        const salary = internship.salary?.toLowerCase() || '';
        switch (filters.salaryRange) {
          case 'paid':
            if (!salary.includes('paid') && !salary.includes('$') && !salary.includes('hourly') && !salary.includes('competitive')) {
              return false;
            }
            break;
          case 'unpaid':
            if (!salary.includes('unpaid') && !salary.includes('volunteer')) {
              return false;
            }
            break;
          case 'competitive':
            if (!salary.includes('competitive')) {
              return false;
            }
            break;
          case 'hourly':
            if (!salary.includes('hourly') && !salary.includes('$')) {
              return false;
            }
            break;
        }
      }

      // Job type filter
      if (filters.jobType && internship.job_type !== filters.jobType) {
        return false;
      }

      return true;
    });
  }, [internships, filters]);

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
                {filteredInternships.length} of {internships.length} internships
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

        {/* Filter Panel */}
        {!loading && internships.length > 0 && (
          <FilterPanel 
            filters={filters}
            onFiltersChange={setFilters}
            internships={internships}
          />
        )}

        {/* Notification Subscription Section */}
        <div className="mb-12">
          <NotificationSubscription />
        </div>

        {/* Loading State */}
        {loading && internships.length === 0 && <LoadingSpinner />}

        {/* Internships Grid */}
        {!loading && filteredInternships.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredInternships.map((internship) => (
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

        {/* No Results State */}
        {!loading && internships.length > 0 && filteredInternships.length === 0 && (
          <div className="text-center py-12">
            <div className="text-gray-400 text-6xl mb-4">🔍</div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              No internships match your filters
            </h3>
            <p className="text-gray-500 mb-4">
              Try adjusting your search criteria or clearing the filters.
            </p>
            <button
              onClick={() => setFilters({
                searchTerm: '',
                location: '',
                remoteOnly: false,
                salaryRange: '',
                company: '',
                jobType: '',
              })}
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium"
            >
              Clear All Filters
            </button>
          </div>
        )}
      </div>
    </div>
  );
}