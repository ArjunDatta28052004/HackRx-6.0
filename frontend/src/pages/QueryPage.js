import React, { useState } from 'react';
import { queryService } from '../services/queryService';
import toast from 'react-hot-toast';

const QueryPage = () => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!query.trim()) {
      toast.error('Please enter a query');
      return;
    }

    setLoading(true);
    try {
      const response = await queryService.processQuery(query.trim());
      setResult(response);
      toast.success('Query processed successfully!');
    } catch (error) {
      toast.error(error.message);
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  const exampleQueries = [
    "A 45-year-old male from Mumbai needs knee surgery with a 2-year policy",
    "Female patient aged 32 from Delhi requires heart surgery with 18-month coverage",
    "60-year-old male from Bangalore needs hip replacement with 3-year policy",
    "35-year-old female from Chennai requires eye surgery with 1-year coverage"
  ];

  const handleExampleClick = (exampleQuery) => {
    setQuery(exampleQuery);
  };

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Insurance Query System</h1>
        <p className="text-gray-600">
          Ask questions about insurance policies and get instant AI-powered answers based on your uploaded documents.
        </p>
      </div>

      {/* Query Form */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Ask Your Question</h2>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="query" className="block text-sm font-medium text-gray-700 mb-2">
              Describe your insurance query
            </label>
            <textarea
              id="query"
              rows="4"
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              placeholder="Example: A 45-year-old male from Mumbai needs knee surgery with a 2-year policy"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              disabled={loading}
            />
          </div>
          
          <button
            type="submit"
            disabled={loading || !query.trim()}
            className="w-full bg-primary-600 hover:bg-primary-700 disabled:bg-gray-400 text-white px-6 py-3 rounded-md font-medium transition-colors disabled:cursor-not-allowed"
          >
            {loading ? 'Processing...' : 'Process Query'}
          </button>
        </form>
      </div>

      {/* Example Queries */}
      <div className="bg-gray-50 rounded-lg p-6 mb-8">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Example Queries</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {exampleQueries.map((example, index) => (
            <button
              key={index}
              onClick={() => handleExampleClick(example)}
              className="text-left p-3 bg-white rounded-md border border-gray-200 hover:border-primary-300 hover:bg-primary-50 transition-colors text-sm text-gray-700"
            >
              {example}
            </button>
          ))}
        </div>
      </div>

      {/* Results */}
      {result && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Query Results</h2>
          
          {/* Parsed Information */}
          <div className="mb-6">
            <h3 className="text-lg font-medium text-gray-900 mb-3">Parsed Information</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div className="bg-gray-50 rounded-lg p-3">
                <span className="text-sm font-medium text-gray-500">Age:</span>
                <p className="text-gray-900">{result.parsed_info.age}</p>
              </div>
              <div className="bg-gray-50 rounded-lg p-3">
                <span className="text-sm font-medium text-gray-500">Gender:</span>
                <p className="text-gray-900">{result.parsed_info.gender}</p>
              </div>
              <div className="bg-gray-50 rounded-lg p-3">
                <span className="text-sm font-medium text-gray-500">Procedure:</span>
                <p className="text-gray-900">{result.parsed_info.procedure}</p>
              </div>
              <div className="bg-gray-50 rounded-lg p-3">
                <span className="text-sm font-medium text-gray-500">Location:</span>
                <p className="text-gray-900">{result.parsed_info.location}</p>
              </div>
              <div className="bg-gray-50 rounded-lg p-3">
                <span className="text-sm font-medium text-gray-500">Policy Duration:</span>
                <p className="text-gray-900">{result.parsed_info.policy_duration}</p>
              </div>
            </div>
          </div>

          {/* Decision */}
          <div className="mb-6">
            <h3 className="text-lg font-medium text-gray-900 mb-3">Decision</h3>
            <div className={`inline-flex items-center px-4 py-2 rounded-md font-medium ${
              result.decision === 'Approved' 
                ? 'bg-green-100 text-green-800' 
                : 'bg-red-100 text-red-800'
            }`}>
              {result.decision}
            </div>
            <p className="mt-2 text-gray-700">{result.justification}</p>
          </div>

          {/* Policy Clauses */}
          {result.policy_clauses && result.policy_clauses.length > 0 && (
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-3">Relevant Policy Clauses</h3>
              <div className="space-y-3">
                {result.policy_clauses.map((clause, index) => (
                  <div key={index} className="bg-blue-50 rounded-lg p-3 border-l-4 border-blue-400">
                    <p className="text-gray-800 text-sm">{clause}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* How it works */}
      <div className="mt-8 bg-gradient-to-r from-green-50 to-blue-50 rounded-lg p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-3">How the Query System Works</h2>
        <div className="space-y-2 text-gray-700">
          <p>• <strong>Natural Language Processing:</strong> The system understands queries in plain English</p>
          <p>• <strong>Smart Parsing:</strong> Automatically extracts age, gender, procedure, location, and policy duration</p>
          <p>• <strong>AI Analysis:</strong> Uses your uploaded documents to provide relevant policy clauses</p>
          <p>• <strong>Instant Decisions:</strong> Provides immediate approval/rejection based on policy rules</p>
        </div>
      </div>
    </div>
  );
};

export default QueryPage;