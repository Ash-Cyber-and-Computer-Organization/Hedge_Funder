"use client"

import { SignIn } from "@clerk/clerk-react"
import { motion } from "framer-motion"
import { Link } from "react-router-dom"

const SignupPage = () => {
  // Check if Clerk is available (ClerkProvider is present)
  const hasClerk = typeof window !== 'undefined' && window.Clerk;

  if (!hasClerk) {
    // Fallback when Clerk is not available
    return (
      <div className="min-h-screen flex items-center justify-center p-4 overflow-x-hidden relative">
        <div className="absolute inset-0 z-0 bg-gradient-to-br from-purple-950 via-gray-950 to-black" />

        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
          className="relative z-10 w-full max-w-md"
        >
          <div className="bg-white/10 backdrop-blur-sm rounded-3xl border border-white/20 shadow-2xl shadow-purple-900/40 p-8">
            <div className="text-center mb-6">
              <h1 className="text-2xl font-bold text-purple-600 mb-1">Elite Trader</h1>
              <p className="text-sm text-gray-300">Authentication Setup Required</p>
            </div>

            <div className="text-center">
              <p className="text-gray-300 mb-4">
                Authentication is not configured yet. Please set up your Clerk account first.
              </p>
              <Link
                to="/"
                className="inline-block bg-purple-600 hover:bg-purple-700 text-white font-semibold py-2 px-4 rounded-full transition-colors"
              >
                Back to Home
              </Link>
            </div>
          </div>
        </motion.div>
      </div>
    )
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4 overflow-x-hidden relative">
      <div className="absolute inset-0 z-0 bg-gradient-to-br from-purple-950 via-gray-950 to-black" />

      <motion.div
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: "easeOut" }}
        className="relative z-10 w-full max-w-md"
      >
        <div className="bg-white/10 backdrop-blur-sm rounded-3xl border border-white/20 shadow-2xl shadow-purple-900/40 p-8">
          <div className="text-center mb-6">
            <h1 className="text-2xl font-bold text-purple-600 mb-1">Elite Trader</h1>
            <p className="text-sm text-gray-300">Sign in to your account</p>
          </div>

          <SignIn
            path="/signin"
            routing="path"
            signUpUrl="/signup"
            appearance={{
              baseTheme: undefined,
              variables: {
                colorPrimary: '#9333ea',
                colorBackground: 'transparent',
                colorInputBackground: 'rgba(255, 255, 255, 0.05)',
                colorInputText: '#ffffff',
                colorText: '#ffffff',
                colorTextSecondary: '#9ca3af',
                borderRadius: '0.75rem'
              },
              elements: {
                formButtonPrimary: 'bg-purple-600 hover:bg-purple-700 text-white font-semibold py-2 px-4 rounded-full',
                card: 'bg-transparent border-none shadow-none',
                headerTitle: 'text-white text-xl font-bold',
                headerSubtitle: 'text-gray-300',
                socialButtonsBlockButton: 'bg-white/5 backdrop-blur-sm border border-white/20 hover:bg-white/20 text-white',
                formFieldInput: 'bg-white/5 border border-white/20 text-white placeholder-gray-400 focus:border-purple-500',
                formFieldLabel: 'text-gray-300',
                footerActionText: 'text-gray-300',
                footerActionLink: 'text-purple-400 hover:text-purple-300'
              }
            }}
          />
        </div>
      </motion.div>
    </div>
  )
}

export default SignupPage
