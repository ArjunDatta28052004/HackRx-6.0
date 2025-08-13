import React, { useState, useEffect } from 'react';
import { useDropzone } from 'react-dropzone';
import { documentService } from '../services/documentService';
import toast from 'react-hot-toast';

const DocumentsPage = () => {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [buildingIndex, setBuildingIndex] = useState(false);

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    try {
      const response = await documentService.getDocuments();
      setDocuments(response.documents || []);
    } catch (error) {
      toast.error(error.message);
    }
  };

  const onDrop = async (acceptedFiles) => {
    if (acceptedFiles.length === 0) return;

    setLoading(true);
    try {
      for (const file of acceptedFiles) {
        await documentService.uploadFile(file);
        toast.success(`${file.name} uploaded successfully!`);
      }
      fetchDocuments(); // Refresh the documents list
    } catch (error) {
      toast.error(error.message);
    } finally {
      setLoading(false);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    },
    maxSize: 16 * 1024 * 1024, // 16MB
  });

  const handleBuildIndex = async () => {
    if (documents.length === 0) {
      toast.error('No documents to process');
      return;
    }

    setBuildingIndex(true);
    try {
      await documentService.buildIndex();
      toast.success('Index built successfully! You can now use the query system.');
      fetchDocuments(); // Refresh to update processed status
    } catch (error) {
      toast.error(error.message);
    } finally {
      setBuildingIndex(false);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const getFileIcon = (fileType) => {
    return fileType === 'pdf' ? '📄' : '📝';
  };

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Document Management</h1>
        <p className="text-gray-600">
          Upload and manage your insurance documents. Supported formats: PDF, DOCX (max 16MB)
        </p>
      </div>

      {/* File Upload Area */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Upload Documents</h2>
        
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
            isDragActive
              ? 'border-primary-500 bg-primary-50'
              : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
          }`}
        >
          <input {...getInputProps()} />
          <div className="space-y-4">
            <div className="text-4xl">📁</div>
            {isDragActive ? (
              <p className="text-primary-600 font-medium">Drop the files here...</p>
            ) : (
              <>
                <p className="text-gray-600">
                  Drag and drop files here, or <span className="text-primary-600 font-medium">click to select files</span>
                </p>
                <p className="text-sm text-gray-500">
                  Supports PDF and DOCX files up to 16MB
                </p>
              </>
            )}
          </div>
        </div>

        {loading && (
          <div className="mt-4 text-center">
            <div className="inline-flex items-center px-4 py-2 bg-blue-100 text-blue-800 rounded-md">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-800 mr-2"></div>
              Uploading...
            </div>
          </div>
        )}
      </div>

      {/* Documents List */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-semibold text-gray-900">Your Documents</h2>
          <button
            onClick={handleBuildIndex}
            disabled={buildingIndex || documents.length === 0}
            className="bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white px-4 py-2 rounded-md font-medium transition-colors disabled:cursor-not-allowed"
          >
            {buildingIndex ? 'Building Index...' : 'Build Index'}
          </button>
        </div>

        {documents.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            <div className="text-4xl mb-4">📄</div>
            <p>No documents uploaded yet.</p>
            <p className="text-sm">Upload some documents to get started!</p>
          </div>
        ) : (
          <div className="space-y-4">
            {documents.map((doc) => (
              <div
                key={doc.id}
                className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-center space-x-4">
                  <div className="text-2xl">{getFileIcon(doc.file_type)}</div>
                  <div>
                    <h3 className="font-medium text-gray-900">{doc.filename}</h3>
                    <p className="text-sm text-gray-500">
                      Uploaded {formatDate(doc.uploaded_at)}
                    </p>
                  </div>
                </div>
                
                <div className="flex items-center space-x-2">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    doc.processed
                      ? 'bg-green-100 text-green-800'
                      : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {doc.processed ? 'Processed' : 'Pending'}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Instructions */}
      <div className="bg-blue-50 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-blue-900 mb-3">How it works:</h3>
        <div className="space-y-2 text-blue-800">
          <p>1. Upload your insurance documents (PDF or DOCX format)</p>
          <p>2. Click "Build Index" to process your documents</p>
          <p>3. Once processed, you can use the Query system to ask questions</p>
          <p>4. The AI will analyze your documents and provide relevant answers</p>
        </div>
      </div>
    </div>
  );
};

export default DocumentsPage;