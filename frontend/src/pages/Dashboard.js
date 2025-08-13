import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Dashboard = () => {
  const { user } = useAuth();

  const features = [
    {
      title: 'Document Management',
      description: 'Upload and manage your insurance documents (PDF, DOCX)',
      icon: '📄',
      link: '/documents',
      color: 'bg-blue-500',
    },
    {
      title: 'Query Processing',
      description: 'Ask questions about insurance policies and get instant answers',
      icon: '🔍',
      link: '/query',
      color: 'bg-green-500',
    },
    {
      title: 'Smart Analysis',
      description: 'AI-powered analysis of your insurance documents',
      icon: '🤖',
      link: '/documents',
      color: 'bg-purple-500',
    },
  ];

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Welcome back, {user?.username}!
        </h1>
        <p className="text-gray-600">
          Manage your insurance documents and get instant answers to your queries.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        {features.map((feature, index) => (
          <Link
            key={index}
            to={feature.link}
            className="block group"
          >
            <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow duration-200">
              <div className="flex items-center mb-4">
                <div className={`${feature.color} text-white rounded-lg p-3 mr-4`}>
                  <span className="text-2xl">{feature.icon}</span>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 group-hover:text-primary-600">
                  {feature.title}
                </h3>
              </div>
              <p className="text-gray-600">{feature.description}</p>
            </div>
          </Link>
        ))}
      </div>

      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Getting Started</h2>
        <div className="space-y-4">
          <div className="flex items-start">
            <div className="bg-primary-100 text-primary-600 rounded-full w-8 h-8 flex items-center justify-center text-sm font-semibold mr-3 mt-1">
              1
            </div>
            <div>
              <h3 className="font-medium text-gray-900">Upload Documents</h3>
              <p className="text-gray-600">
                Start by uploading your insurance documents (PDF or DOCX format) in the Documents section.
              </p>
            </div>
          </div>
          
          <div className="flex items-start">
            <div className="bg-primary-100 text-primary-600 rounded-full w-8 h-8 flex items-center justify-center text-sm font-semibold mr-3 mt-1">
              2
            </div>
            <div>
              <h3 className="font-medium text-gray-900">Build Index</h3>
              <p className="text-gray-600">
                After uploading, build the search index to enable AI-powered query processing.
              </p>
            </div>
          </div>
          
          <div className="flex items-start">
            <div className="bg-primary-100 text-primary-600 rounded-full w-8 h-8 flex items-center justify-center text-sm font-semibold mr-3 mt-1">
              3
            </div>
            <div>
              <h3 className="font-medium text-gray-900">Ask Questions</h3>
              <p className="text-gray-600">
                Use the Query section to ask questions about your insurance policies and get instant answers.
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="mt-8 bg-gradient-to-r from-primary-50 to-blue-50 rounded-lg p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-2">Need Help?</h2>
        <p className="text-gray-600 mb-4">
          This system uses advanced AI to analyze your insurance documents and provide instant answers to your queries.
        </p>
        <div className="text-sm text-gray-500">
          <p>• Supported file formats: PDF, DOCX</p>
          <p>• Maximum file size: 16MB</p>
          <p>• Your documents are processed securely and privately</p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;