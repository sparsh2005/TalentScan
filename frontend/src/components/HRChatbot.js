import React, { useState } from 'react';
import axios from 'axios';
import { toast } from 'react-toastify';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function HRChatbot() {
  const [query, setQuery] = useState('');
  const [role, setRole] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    try {
      const response = await axios.post(`${API_URL}/api/chat`, {
        query: query.trim(),
        role: role.trim() || undefined
      });

      setResponse(response.data.response);
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Error getting response');
      console.error('Chat error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white shadow sm:rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900">
            HR Assistant
          </h3>
          <div className="mt-2 max-w-xl text-sm text-gray-500">
            <p>Ask questions about candidates or rank them for specific roles.</p>
          </div>
          <form onSubmit={handleSubmit} className="mt-5">
            <div className="space-y-4">
              <div>
                <label htmlFor="role" className="block text-sm font-medium text-gray-700">
                  Role (optional)
                </label>
                <input
                  type="text"
                  name="role"
                  id="role"
                  value={role}
                  onChange={(e) => setRole(e.target.value)}
                  className="mt-1 block w-full shadow-sm sm:text-sm focus:ring-indigo-500 focus:border-indigo-500 border-gray-300 rounded-md"
                  placeholder="e.g., Senior Software Engineer"
                />
              </div>
              <div>
                <label htmlFor="query" className="block text-sm font-medium text-gray-700">
                  Your Question
                </label>
                <div className="mt-1">
                  <textarea
                    id="query"
                    name="query"
                    rows={3}
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md"
                    placeholder="e.g., Who has the most experience with Python? or Rank candidates for the AI Engineer role"
                  />
                </div>
              </div>
              <div>
                <button
                  type="submit"
                  disabled={loading}
                  className={`inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500
                    ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
                >
                  {loading ? 'Processing...' : 'Ask Question'}
                </button>
              </div>
            </div>
          </form>

          {response && (
            <div className="mt-6">
              <h4 className="text-sm font-medium text-gray-900">Response:</h4>
              <div className="mt-2 p-4 bg-gray-50 rounded-md">
                <pre className="whitespace-pre-wrap text-sm text-gray-700">
                  {response}
                </pre>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default HRChatbot; 