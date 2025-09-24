"use client"

import { useState, useEffect } from "react"
import { Link } from "react-router-dom"
import { motion } from "framer-motion"
import { TrendingUp, Shield, Bot, TrendingDown } from "lucide-react" // Added TrendingDown
import PublicLayout from "../layout/PublicLayout"

const fadeInUp = {
  initial: { opacity: 0, y: 60 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.8, ease: "easeOut" }
}

const staggerContainer = {
  animate: {
    transition: {
      staggerChildren: 0.1
    }
  }
}

export default function TradingPlatformLandingPage() {
  const [cryptoData, setCryptoData] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  useEffect(() => {
    const fetchCryptoData = async () => {
      try {
        setLoading(true)
        setError(null)
        const response = await fetch(
          "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=8&page=1&sparkline=false&price_change_percentage=24h",
        )

        if (!response.ok) {
          throw new Error("Failed to fetch crypto data. Please try again later.")
        }

        const data = await response.json()

        const formattedData = data.map((crypto) => ({
          id: crypto.id,
          name: crypto.name,
          symbol: crypto.symbol.toUpperCase(),
          price: crypto.current_price,
          change: crypto.price_change_percentage_24h,
          volume: crypto.total_volume,
        }))

        setCryptoData(formattedData)
        setLoading(false)
      } catch (err) {
        console.error("Error fetching crypto data:", err)
        setError(err.message)
        setLoading(false)
      }
    }

    fetchCryptoData()
  }, [])

  const services = [
    {
      icon: Bot,
      title: "Automated Trading",
      description:
        "Advanced AI-powered algorithms execute trades 24/7, analyzing market patterns and capitalizing on opportunities while you sleep. Our bots adapt to market conditions in real-time.",
    },
    {
      icon: TrendingUp,
      title: "Live Trading",
      description:
        "Access real-time market data, advanced charting tools, and lightning-fast execution. Trade with professional-grade features including stop-loss, take-profit, and margin trading.",
    },
    {
      icon: Shield,
      title: "Safety And Protection Of Your Assets",
      description:
        "Bank-level security with multi-factor authentication, cold storage wallets, and insurance coverage. Your funds are protected by industry-leading security protocols and compliance standards.",
    },
  ]

  const stats = [
    { number: "94,000+", label: "Active Traders" },
    { number: "115,000+", label: "Transactions Made" },
    { number: "1,500+", label: "Assets to trade in" },
  ]

  return (
    <PublicLayout>
      <div className="min-h-screen bg-black text-gray-300">
        
        
         <section className="pt-8 pb-20 px-4 bg-gradient-to-t from-gray-800 via-gray-900 to-black sm:px-6 lg:px-8">
           
          <div className="max-w-7xl mx-auto">
            <div className="grid lg:grid-cols-2 gap-12 items-center">
              <motion.div
                initial={{ opacity: 0, x: -50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6 }}
              >
                <h1 className="text-4xl lg:text-6xl font-bold text-white leading-tight">
                  Your Gateway to <span className="text-purple-500">Superior, Seamless & Elite Trading</span>
                </h1>
                <p className="text-lg text-gray-400 mt-6 mb-8">
                  Join the ranks of elite traders using cutting-edge AI technology and advanced market analytics. Our
                  platform delivers institutional-grade trading tools designed for both beginners and professionals
                  seeking superior returns in the cryptocurrency markets.
                </p>
                <div className="flex flex-col sm:flex-row gap-4">
                  <Link
                                    to="/signin">
                  <button  className="bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-500 hover:to-purple-600 text-white font-medium py-4 px-12 rounded-full text-lg transition-all duration-300 shadow-lg hover:shadow-purple-500/25">
                    Start Trading Now
                  </button>
                  </Link>
                  <Link
                                    to="/about">
                  <button
                    variant="outline"
                    className="border border-purple-500 text-purple-500 hover:bg-purple-900/20 px-8 py-3 rounded-full text-lg bg-transparent font-semibold transition-colors"
                  >
                    Meet The Team
                  </button>
                  </Link>
                </div>
              </motion.div>
              <motion.div
                initial={{ opacity: 0, x: 50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.2 }}
                className="relative"
              >
                <img
                  src="/Bitcoin-amico.svg"
                  alt="Crypto trading dashboard visualization"
                  className="w-full h-auto rounded-lg"
                />
              </motion.div>
            </div>
          </div>
        </section>

        {/* Experience Section */}
        <section id="join-us" className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-gray-800 via-gray-900 to-black relative overflow-hidden">
          {/* Background effects */}
          <div className="absolute inset-0 opacity-5">
            <div className="absolute top-40 left-20 w-72 h-72 bg-purple-500 rounded-full blur-3xl"></div>
            <div className="absolute bottom-40 right-20 w-96 h-96 bg-purple-400 rounded-full blur-3xl"></div>
          </div>
          
          <div className="max-w-7xl mx-auto relative z-10">
            <div className="grid lg:grid-cols-2 gap-12 items-center">
              <motion.div
                {...fadeInUp}
                whileInView={{ opacity: 1, y: 0 }}
                initial={{ opacity: 0, y: 60 }}
                transition={{ duration: 0.8, ease: "easeOut" }}
                viewport={{ once: true, margin: "-100px" }}
              >
                <img
                  src="/Bitcoin P2P-amico.svg"
                  alt="Advanced trading analytics dashboard"
                  className="w-full h-auto rounded-lg"
                />
              </motion.div>
              <motion.div
                initial={{ opacity: 0, y: 60 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.2, ease: "easeOut" }}
                viewport={{ once: true, margin: "-100px" }}
              >
                <div className="inline-block bg-purple-900/50 text-purple-400 px-4 py-2 rounded-full text-sm font-semibold mb-4">
                  Limited Time Offer!
                </div>
                <h2 className="text-3xl lg:text-4xl font-bold text-white mb-6">
                  Join The Elite <span className="text-purple-400">Today</span>
                </h2>
                <p className="text-lg text-gray-300 mb-8">
                  Transform your financial future with our exclusive trading platform. Get access to professional-grade
                  tools, AI-powered strategies, and a community of successful traders. Start with our risk-free demo
                  account and experience the difference that elite-level trading makes.
                </p>
                <div className="mb-6">
                  <div className="flex items-center mb-2">
                    <div className="w-4 h-4 bg-green-400 rounded-full mr-3 flex-shrink-0"></div>
                    <span className="text-gray-300">✓ No trading experience required</span>
                  </div>
                  <div className="flex items-center mb-2">
                    <div className="w-4 h-4 bg-green-400 rounded-full mr-3 flex-shrink-0"></div>
                    <span className="text-gray-300">✓ 24/7 automated trading</span>
                  </div>
                  <div className="flex items-center">
                    <div className="w-4 h-4 bg-green-400 rounded-full mr-3 flex-shrink-0"></div>
                    <span className="text-gray-300">✓ Free $100,000 demo account</span>
                  </div>
                </div>
                <Link
                                    to="/signin">
                <button className="bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-500 hover:to-purple-600 text-white font-medium py-4 px-12 rounded-full text-lg transition-all duration-300 shadow-lg hover:shadow-purple-500/25">
                  Get Started Free
                </button>
                </Link>
              </motion.div>
            </div>
          </div>
        </section>

        {/* Crypto Section */}
        <section id="crypto" className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-black via-gray-900 to-gray-800 relative overflow-hidden">
          {/* Background effects */}
          <div className="absolute inset-0 opacity-5">
            <div className="absolute top-40 left-20 w-72 h-72 bg-purple-500 rounded-full blur-3xl"></div>
            <div className="absolute bottom-40 right-20 w-96 h-96 bg-purple-400 rounded-full blur-3xl"></div>
          </div>
          
          <div className="max-w-7xl mx-auto relative z-10">
            <motion.div
              initial={{ opacity: 0, y: 60 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, ease: "easeOut" }}
              viewport={{ once: true, margin: "-100px" }}
              className="text-center mb-16"
            >
              <h2 className="text-3xl lg:text-4xl font-bold text-white mb-4">
                Top Cryptocurrencies <span className="text-purple-400">Available for Trading</span>
              </h2>
              <p className="text-lg text-gray-300 max-w-2xl mx-auto">
                Access the most popular cryptocurrencies with real-time pricing, advanced analytics, and instant
                execution. Our platform supports over 150+ digital assets.
              </p>
            </motion.div>
            
            {loading ? (
              <div className="text-center text-gray-300 py-20">
                <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-purple-500"></div>
                <p className="mt-4">Loading crypto data...</p>
              </div>
            ) : error ? (
              <div className="text-center text-red-400 py-20">Error: {error}</div>
            ) : (
              <motion.div
      variants={staggerContainer}
      initial="initial"
      whileInView="animate"
      viewport={{ once: true, amount: 0.2 }}
      className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8"
    >
      {cryptoData.map((item) => (
        <motion.div
          key={item.id}
          variants={fadeInUp}
          className="group relative"
        >
          {/* Card container */}
          <div className="relative bg-gradient-to-br from-gray-800/80 via-gray-900/90 to-black/80 backdrop-blur-xl rounded-2xl overflow-hidden border border-gray-700/50 hover:border-purple-500/50 transition-colors duration-300">
            {/* Hover effect overlay */}
            <div className="absolute -inset-0.5 bg-gradient-to-r from-purple-500 to-purple-700 rounded-2xl blur-xl opacity-0 group-hover:opacity-20 transition-opacity duration-300"></div>

            {/* Inner content */}
            <div className="relative p-6">
              {/* Header section */}
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 rounded-full bg-purple-600/30 flex items-center justify-center text-white font-bold text-sm">
                    <img 
                      src={`https://s2.coinmarketcap.com/static/img/coins/64x64/${item.id}.png`} 
                      alt={`${item.symbol} logo`} 
                      className="w-full h-full object-cover rounded-full p-1"
                      onError={(e) => {
                        e.currentTarget.style.display = 'none';
                        e.currentTarget.parentElement.innerHTML = item.symbol.substring(0, 2).toUpperCase();
                      }}
                    />
                  </div>
                  <div>
                    <h3 className="font-bold text-white text-lg">{item.name}</h3>
                    <p className="text-gray-400 text-sm">{item.symbol}</p>
                  </div>
                </div>
                
                {/* Price change badge */}
                <div className={`flex items-center space-x-1 px-3 py-1 rounded-full text-xs font-medium ${
                  item.change >= 0 
                    ? "bg-green-500/10 text-green-400 border border-green-500/20" 
                    : "bg-red-500/10 text-red-400 border border-red-500/20"
                }`}>
                  {item.change >= 0 
                    ? <TrendingUp className="w-3 h-3" /> 
                    : <TrendingDown className="w-3 h-3" />
                  }
                  <span>{item.change >= 0 ? "+" : ""}{item.change?.toFixed(2)}%</span>
                </div>
              </div>
              
              {/* Price section */}
              <div className="mb-6">
                <div className="text-3xl font-bold text-white mb-1">
                  ${item.price.toLocaleString(undefined, { 
                    minimumFractionDigits: 2, 
                    maximumFractionDigits: item.price > 1000 ? 2 : 4 
                  })}
                </div>
                <div className="text-gray-500 text-sm">USD</div>
              </div>
              
              {/* Stats section */}
              <div className="space-y-3 pt-4 border-t border-gray-700/50">
                <div className="flex justify-between items-center text-sm">
                  <span className="text-gray-500">24h Volume</span>
                  <span className="text-white font-medium">
                    ${(item.volume / 1000000000).toFixed(2)}B
                  </span>
                </div>
              </div>
              
              {/* Action button */}
              <div className="mt-6">
                <button className="w-full bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-500 hover:to-purple-600 text-white font-medium py-2 rounded-full text-sm transition-all duration-300 shadow-lg hover:shadow-purple-500/25 flex items-center justify-center">
                  Trade {item.symbol}
                </button>
              </div>
            </div>
          </div>
        </motion.div>
      ))}
    </motion.div>
            )}
          </div>
        </section>

        {/* Services Section */}
        <section id="offer" className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-gray-800 via-gray-900 to-black relative overflow-hidden">
          {/* Background effects */}
          <div className="absolute inset-0 opacity-5">
            <div className="absolute top-40 left-20 w-72 h-72 bg-purple-500 rounded-full blur-3xl"></div>
            <div className="absolute bottom-40 right-20 w-96 h-96 bg-purple-400 rounded-full blur-3xl"></div>
          </div>
          
          <div className="max-w-7xl mx-auto relative z-10">
            <motion.div
              initial={{ opacity: 0, y: 60 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, ease: "easeOut" }}
              viewport={{ once: true, margin: "-100px" }}
              className="text-center mb-16"
            >
              <h2 className="text-3xl lg:text-4xl font-bold text-white mb-4">
                What We <span className="text-purple-400">Offer</span>
              </h2>
              <p className="text-lg text-gray-300 max-w-2xl mx-auto">
                Elite Trader provides comprehensive trading solutions designed to maximize your investment potential.
                From beginner-friendly automation to advanced professional tools, we have everything you need to succeed
                in the cryptocurrency markets.
              </p>
            </motion.div>
            <motion.div 
              variants={staggerContainer}
              initial="initial"
              whileInView="animate"
              viewport={{ once: true, margin: "-100px" }}
              className="grid grid-cols-1 md:grid-cols-3 gap-8"
            >
              {services.map((service, index) => (
                <motion.div
                  key={service.title}
                  variants={fadeInUp}
                  className="text-center bg-gradient-to-br from-gray-800/80 via-gray-900/90 to-black/80 backdrop-blur-xl p-8 rounded-2xl border border-gray-700/50 hover:border-purple-500/50 transition-colors duration-300"
                >
                  <div className="bg-gradient-to-br from-purple-600/20 to-purple-800/20 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6 border border-purple-500/30">
                    <service.icon className="w-8 h-8 text-purple-400" />
                  </div>
                  <h3 className="text-xl font-semibold text-white mb-4">{service.title}</h3>
                  <p className="text-gray-300 leading-relaxed">{service.description}</p>
                </motion.div>
              ))}
            </motion.div>
          </div>
        </section>

        {/* Why Choose Us Section */}
        <section id="choose" className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-black via-gray-900 to-gray-800 relative overflow-hidden">
          {/* Background effects */}
          <div className="absolute inset-0 opacity-5">
            <div className="absolute top-40 left-20 w-72 h-72 bg-purple-500 rounded-full blur-3xl"></div>
            <div className="absolute bottom-40 right-20 w-96 h-96 bg-purple-400 rounded-full blur-3xl"></div>
          </div>
          
          {/* Abstract artistic elements */}
          <div className="absolute top-16 right-8 w-3 h-20 bg-purple-400/15 -rotate-12 blur-sm"></div>
          <svg className="absolute bottom-28 left-12 w-14 h-14 text-purple-500/20" viewBox="0 0 100 100">
            <rect x="20" y="20" width="60" height="60" fill="none" stroke="currentColor" strokeWidth="1" transform="rotate(45 50 50)"/>
          </svg>
          
          <div className="max-w-7xl mx-auto relative z-10">
            <div className="grid lg:grid-cols-2 gap-12 items-center">
              <motion.div
                initial={{ opacity: 0, y: 60 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, ease: "easeOut" }}
                viewport={{ once: true, margin: "-100px" }}
              >
                <h2 className="text-3xl lg:text-4xl font-bold text-white mb-8">
                  Why <span className="text-purple-400">Choose Elite Trader</span>
                </h2>
                <motion.div 
                  variants={staggerContainer}
                  initial="initial"
                  whileInView="animate"
                  viewport={{ once: true, margin: "-100px" }}
                  className="grid grid-cols-1 sm:grid-cols-3 gap-8 mb-8"
                >
                  {stats.map((stat, index) => (
                    <motion.div
                      key={stat.label}
                      variants={fadeInUp}
                      className="text-center"
                    >
                      <div className="text-3xl font-bold text-purple-400 mb-2">{stat.number}</div>
                      <div className="text-gray-300">{stat.label}</div>
                    </motion.div>
                  ))}
                </motion.div>
                <p className="text-lg text-gray-300 mb-8">
                  Join thousands of successful traders who trust Elite Trader for their cryptocurrency investments. Our
                  proven track record, cutting-edge technology, and commitment to security make us the preferred choice
                  for both novice and experienced traders looking to maximize their returns in the digital asset space.
                </p>
                <Link
                                    to="/signin">
                <button className="bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-500 hover:to-purple-600 text-white font-medium py-4 px-12 rounded-full text-lg transition-all duration-300 shadow-lg hover:shadow-purple-500/25">
                  Create Account
                </button>
                </Link>
              </motion.div>
              <motion.div
                initial={{ opacity: 0, y: 60 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.2, ease: "easeOut" }}
                viewport={{ once: true, margin: "-100px" }}
              >
                <img
                  src="/Crypto portfolio-amico.svg"
                  alt="Professional cryptocurrency trading workspace"
                  className="w-full h-auto rounded-lg shadow-2xl"
                />
              </motion.div>
            </div>
          </div>
        </section>

        {/* Sign Up Section */}
<section className="py-32 px-4 sm:px-6 lg:px-8 bg-gradient-to-t from-black to-gray-800 relative overflow-hidden">
  {/* Minimal background effects */}
  <div className="absolute inset-0 opacity-3">
    <div className="absolute top-1/3 left-1/4 w-96 h-96 bg-purple-600 rounded-full blur-3xl"></div>
    <div className="absolute bottom-1/3 right-1/4 w-80 h-80 bg-purple-500 rounded-full blur-3xl"></div>
  </div>
  
  {/* Single subtle abstract element */}
  <div className="absolute top-20 right-20 w-1 h-40 bg-purple-400/10 rotate-12 blur-sm"></div>
  
  <div className="max-w-4xl mx-auto relative z-10 text-center">
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8, ease: "easeOut" }}
      viewport={{ once: true, margin: "-100px" }}
      className="space-y-8"
    >
      <h2 className="text-5xl lg:text-7xl font-light text-white leading-tight">
        Ready to Join the
        <span className="block text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-purple-600 font-normal">
          Elite?
        </span>
      </h2>
      
      <p className="text-xl text-gray-400 max-w-2xl mx-auto font-light">
        Transform your trading with professional-grade tools and AI-powered strategies.
      </p>
      
      <div className="pt-8">
        <Link
          to="/signin">
        <button className="bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-500 hover:to-purple-600 text-white font-medium py-4 px-12 rounded-full text-lg transition-all duration-300 shadow-lg hover:shadow-purple-500/25">
          Start Trading
        </button>
        </Link>
      </div>
      
      <div className="pt-4 flex items-center justify-center gap-2 text-gray-500 text-sm">
        <div className="w-1.5 h-1.5 bg-green-400 rounded-full"></div>
        <span>Risk-free demo available</span>
      </div>
    </motion.div>
  </div>
</section>
      </div>
    </PublicLayout>
  )
}