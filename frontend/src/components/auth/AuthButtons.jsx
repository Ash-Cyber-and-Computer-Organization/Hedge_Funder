import { SignedIn, SignedOut, SignInButton, UserButton } from "@clerk/clerk-react";
import { Link } from "react-router-dom";

const AuthButtons = ({ onMobileMenuClose }) => {
  // Check if Clerk is available (ClerkProvider is present)
  const hasClerk = typeof window !== 'undefined' && window.Clerk;

  if (!hasClerk) {
    // Fallback when Clerk is not available
    return (
      <>
        <Link
          to="/signin"
          className="text-gray-300 hover:text-purple-400 font-medium transition-colors"
          onClick={onMobileMenuClose}
        >
          Sign In
        </Link>
        <Link
          to="/signin"
          className="bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-500 hover:to-purple-600 text-white font-medium py-2 px-10 rounded-full text-lg transition-all duration-300 shadow-lg hover:shadow-purple-500/25"
          onClick={onMobileMenuClose}
        >
          Get Started
        </Link>
      </>
    );
  }

  return (
    <>
      <SignedOut>
        <SignInButton mode="modal">
          <button
            className="text-gray-300 hover:text-purple-400 font-medium transition-colors"
            onClick={onMobileMenuClose}
          >
            Sign In
          </button>
        </SignInButton>
        <SignInButton mode="modal">
          <button
            className="bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-500 hover:to-purple-600 text-white font-medium py-2 px-10 rounded-full text-lg transition-all duration-300 shadow-lg hover:shadow-purple-500/25"
            onClick={onMobileMenuClose}
          >
            Get Started
          </button>
        </SignInButton>
      </SignedOut>
      <SignedIn>
        <div className="text-gray-300">Welcome back!</div>
        <UserButton
          appearance={{
            elements: {
              avatarBox: "w-8 h-8"
            }
          }}
        />
      </SignedIn>
    </>
  );
};

export default AuthButtons;
