import React, { useState } from "react";
import { Eye, EyeOff, Mail, Lock, User, ArrowRight } from "lucide-react";
import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";
import { useAuthStore } from "../../stores/getAuthStore";
import { SignIn, SignUp } from "@clerk/clerk-react";

const AuthPage = () => {
  const [state, setState] = useState("login");
  const [showPassword, setShowPassword] = useState(false);
  const { register, login, loading, error, clearError } = useAuthStore();
  const navigate = useNavigate();

  // Check if Clerk is available (ClerkProvider is present)
  const hasClerk = typeof window !== 'undefined' && window.Clerk;

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    clearError(); // Clear previous errors

    // Basic validation
    if (!formData.email || !formData.password) {
      toast.error("Please fill in all required fields");
      return;
    }

    if (state === "register" && !formData.name) {
      toast.error("Please enter your name");
      return;
    }

    try {
      let result;
      if (state === "login") {
        result = await login({
          email: formData.email,
          password: formData.password,
        });
      } else {
        result = await register({
          name: formData.name,
          email: formData.email,
          password: formData.password,
        });
      }

      if (result.success) {
        navigate("/");
      }
    } catch (error) {
      console.error("Authentication error:", error);
      // Error is already handled by the store and will show toast
    }
  };

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const toggleState = () => {
    setState(state === "login" ? "register" : "login");
    clearError(); // Clear errors when switching states
    setFormData({
      name: "",
      email: "",
      password: "",
    });
  };

  // If Clerk is not available, show fallback
  if (!hasClerk) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 to-indigo-100 flex items-center justify-center p-4">
        <div className="w-full max-w-md">
          <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
            <div className="bg-[#8400DD] px-8 py-6">
              <h2 className="text-2xl font-bold text-white text-center">
                Authentication Setup Required
              </h2>
              <p className="text-purple-200 text-center mt-1">
                Please configure Clerk authentication
              </p>
            </div>
            <div className="px-8 py-6 text-center">
              <p className="text-gray-600 mb-4">
                Authentication is not configured yet. Please set up your Clerk account first.
              </p>
              <button
                onClick={() => navigate("/")}
                className="bg-[#8400DD] hover:bg-purple-800 text-white font-semibold py-3 px-6 rounded-lg transition-all duration-200"
              >
                Back to Home
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Form Container */}
        <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
          {/* Header */}
          <div className="bg-[#8400DD] px-8 py-6">
            <h2 className="text-2xl font-bold text-white text-center">
              {state === "login" ? "Welcome Back" : "Create Account"}
            </h2>
            <p className="text-purple-200 text-center mt-1">
              {state === "login" ? "Sign in to continue" : "Join us today"}
            </p>
          </div>

          {/* Form Content */}
          <div className="px-8 py-6">
            {/* Error Message */}
            {error && (
              <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-red-600 text-sm">{error}</p>
              </div>
            )}

            {/* Clerk Sign In/Up Component */}
            {state === "login" ? (
              <SignIn
                path="/signin"
                routing="path"
                signUpUrl="/signup"
                appearance={{
                  baseTheme: undefined,
                  variables: {
                    colorPrimary: '#8400DD',
                    colorBackground: 'transparent',
                    colorInputBackground: 'rgba(255, 255, 255, 0.9)',
                    colorInputText: '#374151',
                    colorText: '#374151',
                    colorTextSecondary: '#6b7280',
                    borderRadius: '0.5rem'
                  },
                  elements: {
                    formButtonPrimary: 'bg-[#8400DD] hover:bg-purple-800 text-white font-semibold py-3 px-6 rounded-lg transition-all duration-200',
                    card: 'bg-transparent border-none shadow-none',
                    headerTitle: 'text-[#8400DD] text-xl font-bold',
                    headerSubtitle: 'text-gray-600',
                    socialButtonsBlockButton: 'bg-white border border-gray-200 hover:bg-gray-50 text-gray-700',
                    formFieldInput: 'bg-white border border-gray-200 text-gray-700 placeholder-gray-400 focus:border-[#8400DD] focus:ring-[#8400DD]',
                    formFieldLabel: 'text-gray-700',
                    footerActionText: 'text-gray-600',
                    footerActionLink: 'text-[#8400DD] hover:text-purple-800'
                  }
                }}
              />
            ) : (
              <SignUp
                path="/signup"
                routing="path"
                signInUrl="/signin"
                appearance={{
                  baseTheme: undefined,
                  variables: {
                    colorPrimary: '#8400DD',
                    colorBackground: 'transparent',
                    colorInputBackground: 'rgba(255, 255, 255, 0.9)',
                    colorInputText: '#374151',
                    colorText: '#374151',
                    colorTextSecondary: '#6b7280',
                    borderRadius: '0.5rem'
                  },
                  elements: {
                    formButtonPrimary: 'bg-[#8400DD] hover:bg-purple-800 text-white font-semibold py-3 px-6 rounded-lg transition-all duration-200',
                    card: 'bg-transparent border-none shadow-none',
                    headerTitle: 'text-[#8400DD] text-xl font-bold',
                    headerSubtitle: 'text-gray-600',
                    socialButtonsBlockButton: 'bg-white border border-gray-200 hover:bg-gray-50 text-gray-700',
                    formFieldInput: 'bg-white border border-gray-200 text-gray-700 placeholder-gray-400 focus:border-[#8400DD] focus:ring-[#8400DD]',
                    formFieldLabel: 'text-gray-700',
                    footerActionText: 'text-gray-600',
                    footerActionLink: 'text-[#8400DD] hover:text-purple-800'
                  }
                }}
              />
            )}

            {/* Divider */}
            <div className="relative flex items-center my-6">
              <div className="flex-grow border-t border-gray-200"></div>
              <span className="flex-shrink mx-4 text-gray-400 text-sm">or</span>
              <div className="flex-grow border-t border-gray-200"></div>
            </div>

            {/* Toggle Action */}
            <div className="text-center">
              <p className="text-gray-600">
                {state === "login"
                  ? "Don't have an account? "
                  : "Already have an account? "}
                <button
                  type="button"
                  onClick={toggleState}
                  className="text-[#8400DD] hover:text-purple-800 font-semibold transition-colors"
                >
                  {state === "login" ? "Sign up" : "Sign in"}
                </button>
              </p>
            </div>
          </div>
        </div>

        {/* Additional Links */}
        <div className="text-center mt-6">
          <p className="text-gray-600 text-sm">
            By continuing, you agree to our{" "}
            <a href="#" className="text-[#8400DD] hover:text-purple-800">
              Terms of Service
            </a>{" "}
            and{" "}
            <a href="#" className="text-[#8400DD] hover:text-purple-800">
              Privacy Policy
            </a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default AuthPage;
