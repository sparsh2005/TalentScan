import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { toast } from 'react-toastify';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function ResumeUpload() {
  const [uploading, setUploading] = useState(false);

  const onDrop = useCallback(async (acceptedFiles) => {
    const file = acceptedFiles[0];
    if (!file) return;

    // Log file details
    console.log('File details:', {
      name: file.name,
      type: file.type,
      size: file.size
    });

    // Validate file type
    if (!['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
        .includes(file.type)) {
      toast.error('Please upload only PDF or DOCX files');
      return;
    }

    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      console.log('Sending request to:', `${API_URL}/api/resume/upload`);
      const response = await axios.post(`${API_URL}/api/resume/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      toast.success('Resume uploaded and processed successfully!');
      console.log('Processed candidate:', response.data.candidate);
    } catch (error) {
      console.error('Upload error details:', {
        message: error.message,
        response: error.response?.data,
        status: error.response?.status
      });
      
      // Show more specific error message
      const errorMessage = error.response?.data?.detail || 
                         error.message || 
                         'Error uploading resume';
      toast.error(errorMessage);
    } finally {
      setUploading(false);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx']
    },
    multiple: false
  });

  return (
    <div className="max-w-3xl mx-auto">
      <div className="bg-white shadow sm:rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900">
            Upload Resume
          </h3>
          <div className="mt-2 max-w-xl text-sm text-gray-500">
            <p>Upload a PDF or DOCX file to process the candidate's resume.</p>
          </div>
          <div
            {...getRootProps()}
            className={`mt-4 flex justify-center px-6 pt-5 pb-6 border-2 border-dashed rounded-md
              ${isDragActive ? 'border-indigo-500 bg-indigo-50' : 'border-gray-300'}
              ${uploading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
          >
            <div className="space-y-1 text-center">
              <svg
                className="mx-auto h-12 w-12 text-gray-400"
                stroke="currentColor"
                fill="none"
                viewBox="0 0 48 48"
                aria-hidden="true"
              >
                <path
                  d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                  strokeWidth={2}
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
              <div className="flex text-sm text-gray-600">
                <input {...getInputProps()} />
                <p className="pl-1">
                  {isDragActive
                    ? 'Drop the file here'
                    : 'Drag and drop a resume file, or click to select'}
                </p>
              </div>
              <p className="text-xs text-gray-500">PDF or DOCX up to 10MB</p>
            </div>
          </div>
          {uploading && (
            <div className="mt-4 text-center text-sm text-gray-500">
              Processing resume... Please wait.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default ResumeUpload; 