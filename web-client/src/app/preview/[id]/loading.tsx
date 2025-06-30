import { Loader2, FileText } from 'lucide-react';

export default function Loading() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
      <div className="text-center">
        <div className="relative mb-6">
          <FileText className="h-16 w-16 text-blue-200 mx-auto" />
          <Loader2 className="h-8 w-8 animate-spin text-blue-600 absolute top-4 left-1/2 transform -translate-x-1/2" />
        </div>
        <h2 className="text-2xl font-semibold text-gray-900 mb-2">Loading README Preview</h2>
        <p className="text-gray-600 max-w-md">
          Fetching your professionally generated README content...
        </p>
        <div className="mt-6 flex items-center justify-center space-x-2">
          <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce"></div>
          <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
          <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
        </div>
      </div>
    </div>
  );
}
