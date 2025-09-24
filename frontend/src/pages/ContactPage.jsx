"use client"

import { motion } from "framer-motion"
import { Mail, Phone, MapPin, Clock, Send, XCircle } from "lucide-react"
import { useState } from "react"
import PublicLayout from "../layout/PublicLayout"

// Smooth scroll animation variants
const fadeInUp = {
  initial: { opacity: 0, y: 60 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.8, ease: "easeOut" },
}

const staggerContainer = {
  animate: {
    transition: {
      staggerChildren: 0.1,
    },
  },
}

const ContactPage = () => {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    subject: "",
    message: "",
  })
  const [showSuccessMessage, setShowSuccessMessage] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()

    // Simulate an API call
    console.log("Submitting form data:", formData)

    try {
      // Simulate a network request with a delay
      await new Promise(resolve => setTimeout(resolve, 1000));

      // Assuming the submission was successful
      setShowSuccessMessage(true)
      setFormData({ name: "", email: "", subject: "", message: "" }) // Clear form on success
    } catch (error) {
      console.error("Form submission failed:", error)
      alert("Failed to send message. Please try again later.")
    }
  }

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    })
  }

  const contactInfo = [
    {
      icon: Mail,
      title: "Email Us",
      details: "support@hedge-funder.com",
      description: "Send us an email anytime",
    },
    {
      icon: Phone,
      title: "Call Us",
      details: "+1 (555) 123-4567",
      description: "24/7 customer support",
    },
    {
      icon: MapPin,
      title: "Visit Us",
      details: "123 Financial District, New York, NY 10004",
      description: "Our headquarters",
    },
    {
      icon: Clock,
      title: "Business Hours",
      details: "Mon-Fri: 9AM-6PM EST",
      description: "We're here to help",
    },
  ]

  return (
    <PublicLayout>
    <div className="min-h-screen bg-gradient-to-t from-gray-950 to-black text-gray-300 font-inter">
      {/* Success Message Modal */}
      {showSuccessMessage && (
        <div
          className="fixed top-4 left-1/2 -translate-x-1/2 z-50 p-3 rounded-lg bg-green-500 text-white flex items-center justify-between shadow-lg text-sm"
        >
          <span>Thank you for your message! We'll get back to you soon.</span>
          <button onClick={() => setShowSuccessMessage(false)} className="ml-3">
            <XCircle className="w-4 h-4" />
          </button>
        </div>
      )}

      {/* Hero Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 text-center">
        <div className="max-w-7xl mx-auto space-y-4">
          <h1 className="text-3xl lg:text-5xl font-bold text-white mb-4">
            Get in <span className="text-purple-500">Touch</span>
          </h1>
          <p className="text-lg text-gray-400 max-w-2xl mx-auto leading-relaxed">
            Have questions about Elite Trader? Our expert team is here to help you succeed in your trading journey.
          </p>
        </div>
      </section>

      {/* Contact Info Cards */}
      <section className="py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
          >
            {contactInfo.map((info) => (
              <div
                key={info.title}
                className="bg-gray-800/80 backdrop-blur-sm p-6 rounded-xl text-center border border-gray-700/50 hover:border-purple-500/50 transition-colors duration-300"
              >
                <div className="bg-purple-600/20 w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-3 border border-purple-500/30">
                  <info.icon className="w-6 h-6 text-purple-400" />
                </div>
                <h3 className="text-lg font-semibold text-white mb-1">{info.title}</h3>
                <p className="text-purple-400 font-medium text-sm mb-1">{info.details}</p>
                <p className="text-gray-400 text-xs">{info.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Contact Form */}
      <section className="py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto">
          <div className="p-6 bg-gray-800/80 backdrop-blur-sm rounded-xl border border-gray-700/50">
            <h2 className="text-2xl font-bold text-white mb-4">Send us a Message</h2>
            <p className="text-gray-400 text-sm mb-6">Fill out the form below and we'll get back to you within 24 hours.</p>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label htmlFor="name" className="block text-xs font-medium text-gray-300 mb-1">
                    Full Name
                  </label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    required
                    className="w-full p-2 rounded-lg bg-gray-900/70 border border-gray-700/50 text-white placeholder-gray-500 focus:outline-none focus:ring-1 focus:ring-purple-500/50 transition-colors text-sm"
                    placeholder="Your full name"
                  />
                </div>
                <div>
                  <label htmlFor="email" className="block text-xs font-medium text-gray-300 mb-1">
                    Email Address
                  </label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                    className="w-full p-2 rounded-lg bg-gray-900/70 border border-gray-700/50 text-white placeholder-gray-500 focus:outline-none focus:ring-1 focus:ring-purple-500/50 transition-colors text-sm"
                    placeholder="your@email.com"
                  />
                </div>
              </div>

              <div>
                <label htmlFor="subject" className="block text-xs font-medium text-gray-300 mb-1">
                  Subject
                </label>
                <input
                  type="text"
                  id="subject"
                  name="subject"
                  value={formData.subject}
                  onChange={handleChange}
                  required
                  className="w-full p-2 rounded-lg bg-gray-900/70 border border-gray-700/50 text-white placeholder-gray-500 focus:outline-none focus:ring-1 focus:ring-purple-500/50 transition-colors text-sm"
                  placeholder="What's this about?"
                />
              </div>

              <div>
                <label htmlFor="message" className="block text-xs font-medium text-gray-300 mb-1">
                  Message
                </label>
                <textarea
                  id="message"
                  name="message"
                  value={formData.message}
                  onChange={handleChange}
                  required
                  rows={4}
                  className="w-full p-2 rounded-lg bg-gray-900/70 border border-gray-700/50 text-white placeholder-gray-500 focus:outline-none focus:ring-1 focus:ring-purple-500/50 transition-colors resize-none text-sm"
                  placeholder="Tell us how we can help you..."
                />
              </div>

              <button
                type="submit"
                className="w-full bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-500 hover:to-purple-600 text-white px-4 py-2 rounded-full font-semibold transition-all duration-300 shadow-lg hover:shadow-purple-500/25 flex items-center justify-center text-sm"
              >
                <Send className="w-4 h-4 mr-2" />
                Send Message
              </button>
            </form>
          </div>
        </div>
      </section>
    </div>
    </PublicLayout>
  )
}

export default ContactPage