import { Home, ArrowLeft, Search } from "lucide-react";
import { Link } from "react-router-dom"

export default function Error404Page() {
  return (
    <div className="min-h-screen bg-black flex items-center justify-center px-4">
      <div className="text-center max-w-md mx-auto">
        {/* Large 404 Number */}
        <div className="mb-8">
          <h1 className="text-9xl font-bold text-purple-600 mb-4 tracking-tight">
            404
          </h1>
          <div className="h-1 w-24 bg-purple-500 mx-auto rounded-full"></div>
        </div>
        
        {/* Error Message */}
        <div className="mb-8">
          <h2 className="text-2xl font-semibold text-purple-800 mb-3">
            Page Not Found
          </h2>
          <p className="text-purple-600 leading-relaxed">
            The page you're looking for doesn't exist or is currently in production...
          </p>
        </div>
        
        {/* Action Buttons */}
        <div className="space-y-4">
         <Link to="/">  
          <button className="w-full bg-purple-600 hover:bg-purple-700 text-white font-medium py-3 px-6 rounded-lg transition-colors duration-200 flex items-center justify-center gap-2 group">
            <Home className="w-5 h-5 group-hover:scale-110 transition-transform duration-200" />
            Go to Homepage
          </button>
          </Link> 
        </div>
        
        {/* Decorative Elements */}
        <div className="mt-12 flex justify-center space-x-2">
          <div className="w-2 h-2 bg-purple-400 rounded-full animate-pulse"></div>
          <div className="w-2 h-2 bg-purple-500 rounded-full animate-pulse delay-75"></div>
          <div className="w-2 h-2 bg-purple-600 rounded-full animate-pulse delay-150"></div>
        </div>
      </div>
      
      {/* Background Decoration */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-10 w-32 h-32 bg-purple-700 rounded-full opacity-20 blur-xl"></div>
        <div className="absolute bottom-20 right-10 w-40 h-40 bg-purple-600 rounded-full opacity-15 blur-2xl"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-60 h-60 bg-purple-800 rounded-full opacity-10 blur-3xl"></div>
      </div>
    </div>
  );
}