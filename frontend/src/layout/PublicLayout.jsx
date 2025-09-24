"use client";

import { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { Facebook, Twitter, Instagram, Youtube } from "lucide-react";
import AuthButtons from "../components/auth/AuthButtons";

const PublicLayout = ({ children }) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const location = useLocation();

  const navigation = [
    { name: "Home", href: "/" },
    { name: "About", href: "/about" },
    { name: "Pricing", href: "/pricing" },
    { name: "Contact", href: "/contact" },
  ];

  return (
    <div className="min-h-screen bg-gray-950 text-gray-300">
      {/* Header */}
      <header className="fixed inset-x-0 top-0 z-50">
        <div className="bg-gray-950/90 backdrop-blur-md ">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between h-16">
              {/* Logo */}
              <Link to="/" className="flex items-center">
                <div className="text-2xl font-bold text-purple-500">
                  Elite Trader
                </div>
              </Link>

              {/* Desktop Navigation */}
              <nav className="hidden md:flex space-x-8">
                {navigation.map((item) => (
                  <Link
                    key={item.name}
                    to={item.href}
                    className={`text-sm font-medium transition-colors ${
                      location.pathname === item.href
                        ? "text-purple-400"
                        : "text-gray-300 hover:text-purple-400"
                    }`}
                  >
                    {item.name}
                  </Link>
                ))}
              </nav>

              {/* Auth Buttons */}
              <div className="hidden md:flex items-center space-x-4">
                <AuthButtons onMobileMenuClose={() => setMobileMenuOpen(false)} />
              </div>

              {/* Mobile menu button */}
              <button
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                className="md:hidden p-2 rounded-md text-gray-300 hover:bg-gray-800"
              >
                <svg
                  className="w-6 h-6"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d={
                      mobileMenuOpen
                        ? "M6 18L18 6M6 6l12 12"
                        : "M4 6h16M4 12h16M4 18h16"
                    }
                  />
                </svg>
              </button>
            </div>

            {/* Mobile menu */}
            {mobileMenuOpen && (
              <div className="md:hidden py-4 border-t border-gray-800">
                <div className="flex flex-col space-y-2">
                  {navigation.map((item) => (
                    <Link
                      key={item.name}
                      to={item.href}
                      className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                        location.pathname === item.href
                          ? "text-purple-400 bg-gray-800"
                          : "text-gray-300 hover:text-purple-400 hover:bg-gray-800"
                      }`}
                      onClick={() => setMobileMenuOpen(false)}
                    >
                      {item.name}
                    </Link>
                  ))}
                  <div className="pt-4 border-t border-gray-800 mt-4">
                    <div className="flex flex-col space-y-2">
                      <AuthButtons onMobileMenuClose={() => setMobileMenuOpen(false)} />
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="pt-16">{children}</main>

      {/* Footer */}
      <footer className="bg-gray-950 text-white py-12 border-t border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-8">
            {/* Company Info */}
            <div className="flex-1 text-center md:text-left">
              <h2 className="text-2xl font-extrabold mb-2">
                <span className="text-white">Elite</span>
                <span className="text-purple-400">Trader</span>
              </h2>
              <p className="text-gray-400 text-sm max-w-sm mx-auto md:mx-0">
                The premier cryptocurrency trading platform for professionals
                and beginners.
              </p>
            </div>

            {/* Social Icons */}
            <div className="flex justify-center md:justify-start space-x-5 mt-4 md:mt-0">
              <a
                href="#"
                aria-label="Facebook"
                className="text-gray-400 hover:text-purple-400 transition-colors duration-300"
              >
                <Facebook className="w-5 h-5" />
              </a>
              <a
                href="#"
                aria-label="Twitter"
                className="text-gray-400 hover:text-purple-400 transition-colors duration-300"
              >
                <Twitter className="w-5 h-5" />
              </a>
              <a
                href="#"
                aria-label="Instagram"
                className="text-gray-400 hover:text-purple-400 transition-colors duration-300"
              >
                <Instagram className="w-5 h-5" />
              </a>
              <a
                href="#"
                aria-label="YouTube"
                className="text-gray-400 hover:text-purple-400 transition-colors duration-300"
              >
                <Youtube className="w-5 h-5" />
              </a>
            </div>

            {/* Links */}
            <div className="flex-1 text-center md:text-right">
              <div className="flex flex-col space-y-2 text-sm">
                <Link
                  to="/about"
                  className="text-gray-400 hover:text-purple-400 transition-colors duration-300"
                >
                  About Us
                </Link>
                <Link
                  to="/pricing"
                  className="text-gray-400 hover:text-purple-400 transition-colors duration-300"
                >
                  Pricing
                </Link>
                <Link
                  to="/contact"
                  className="text-gray-400 hover:text-purple-400 transition-colors duration-300"
                >
                  Contact
                </Link>
                <Link
                  to="/contact"
                  className="text-gray-400 hover:text-purple-400 transition-colors duration-300"
                >
                  Help Center
                </Link>
              </div>
            </div>
          </div>

          {/* Legal and Copyright Section */}
          <div className="mt-8 pt-6 border-t border-gray-800 text-xs flex flex-col md:flex-row items-center justify-between space-y-3 md:space-y-0">
            <p className="text-gray-500 text-center md:text-left">
              © 2025 Elite Trader Inc. All rights reserved.
            </p>
            <div className="flex space-x-4 text-gray-500">
              <a
                href="#"
                className="hover:text-purple-400 transition-colors duration-300"
              >
                Privacy Policy
              </a>
              <a
                href="#"
                className="hover:text-purple-400 transition-colors duration-300"
              >
                Risk Disclosure
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default PublicLayout;
