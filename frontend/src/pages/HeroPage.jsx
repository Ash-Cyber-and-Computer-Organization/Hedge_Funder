import { useState, useEffect } from "react"
import { motion } from "framer-motion"
import { Facebook, Twitter, Instagram, Youtube, TrendingUp, Shield, Bot } from "lucide-react"
import { SignedIn, SignedOut, SignInButton, UserButton } from "@clerk/clerk-react"

export default function TradingPlatformLandingPage() {
  const [cryptoData, setCryptoData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCryptoData = async () => {
      try {
        setLoading(true);
        setError(null);
        // Using CoinGecko API to get the top 8 cryptocurrencies
        const response = await fetch('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=8&page=1&sparkline=false&price_change_percentage=24h');
        
        if (!response.ok) {
          throw new Error('Failed to fetch crypto data. Please try again later.');
        }

        const data = await response.json();
        
        // Format the received data to match your component's needs
        const formattedData = data.map(crypto => ({
          id: crypto.id,
          name: crypto.name,
          symbol: crypto.symbol.toUpperCase(),
          price: crypto.current_price,
          change: crypto.price_change_percentage_24h,
          volume: crypto.total_volume,
        }));

        setCryptoData(formattedData);
        setLoading(false);

      } catch (err) {
        console.error("Error fetching crypto data:", err);
        setError(err.message);
        setLoading(false);
      }
    };

    fetchCryptoData();
  }, []); 

  const services = [
    {
      icon: Bot,
      title: "Automated Trading",
      description: "Advanced AI-powered algorithms execute trades 24/7, analyzing market patterns and capitalizing on opportunities while you sleep. Our bots adapt to market conditions in real-time.",
    },
    {
      icon: TrendingUp,
      title: "Live Trading",
      description: "Access real-time market data, advanced charting tools, and lightning-fast execution. Trade with professional-grade features including stop-loss, take-profit, and margin trading.",
    },
    {
      icon: Shield,
      title: "Safety And Protection Of Your Assets",
      description: "Bank-level security with multi-factor authentication, cold storage wallets, and insurance coverage. Your funds are protected by industry-leading security protocols and compliance standards.",
    },
  ];

  const stats = [
    { number: "94,000+", label: "Active Traders" },
    { number: "115,000+", label: "Transactions Made" },
    { number: "1,500+", label: "Assets to trade in" },
  ];
  
  return (
    <div className="min-h-screen bg-gray-950 text-gray-300">
      {/* Header */}
      <header className="fixed top-0 left-0 w-full bg-gray-950/40 backdrop-blur-lg border-b border-gray-800 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="text-2xl font-bold text-purple-500">Elite Trader</div>
            <nav className="hidden md:flex space-x-8">
              <a href="#join-us" className="text-gray-300 hover:text-purple-400 transition-colors">
                Live Trading
              </a>
              <a href="#crypto" className="text-gray-300 hover:text-purple-400 transition-colors">
                Demo account
              </a>
              <a href="#offer" className="text-gray-300 hover:text-purple-400 transition-colors">
                Market Analysis
              </a>
              <a href="#choose" className="text-gray-300 hover:text-purple-400 transition-colors">
                Trading Tools
              </a>
              <a href="#reviews" className="text-gray-300 hover:text-purple-400 transition-colors">
                Mobile App
              </a>
            </nav>
            <SignedOut>
              <SignInButton mode="modal" className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-2 rounded-full font-semibold transition-colors">
                Sign Up
              </SignInButton>
            </SignedOut>
          </div>
        </div>
      </header>
        
      
      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <motion.div initial={{ opacity: 0, x: -50 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.6 }}>
              <h1 className="text-4xl lg:text-6xl font-bold text-white leading-tight">
                Your Gateway to <span className="text-purple-500">Superior, Seamless & Elite Trading</span>
              </h1>
              <p className="text-lg text-gray-400 mt-6 mb-8">
                Join the ranks of elite traders using cutting-edge AI technology and advanced market analytics. Our platform delivers institutional-grade trading tools designed for both beginners and professionals seeking superior returns in the cryptocurrency markets.
              </p>
              <div className="flex flex-col sm:flex-row gap-4">
                <SignedOut>
                  <SignInButton mode="modal" className="bg-purple-600 hover:bg-purple-700 text-white px-8 py-3 rounded-full text-lg font-semibold transition-colors">
                    Start Trading Now
                  </SignInButton>
                </SignedOut>
                <SignedIn>
                  <button className="bg-purple-600 hover:bg-purple-700 text-white px-8 py-3 rounded-full text-lg font-semibold transition-colors">
                    Go to Dashboard
                  </button>
                </SignedIn>
                <button
                  variant="outline"
                  className="border border-purple-500 text-purple-500 hover:bg-purple-900/20 px-8 py-3 rounded-full text-lg bg-transparent font-semibold transition-colors"
                >
                  Meet The Team
                </button>
              </div>
            </motion.div>
            <motion.div
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="relative"
            >
              <img
                src="/undraw_crypto-portfolio_cat6.svg"
                alt="Crypto trading dashboard visualization"
                className="w-full h-auto rounded-lg"
              />
            </motion.div>
          </div>
        </div>
      </section>

      {/* Experience Section */}
      <section id="join-us" className="py-20 px-4 sm:px-6 lg:px-8 bg-gray-900">
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
            >
              <img
                src="https://images.unsplash.com/photo-1551288049-bebda4e38f71"
                alt="Advanced trading analytics dashboard"
                className="w-full h-auto rounded-lg"
              />
            </motion.div>
            <motion.div
              initial={{ opacity: 0, x: 50 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              viewport={{ once: true }}
            >
              <div className="inline-block bg-purple-900/50 text-purple-400 px-4 py-2 rounded-full text-sm font-semibold mb-4">
                Limited Time Offer!
              </div>
              <h2 className="text-3xl lg:text-4xl font-bold text-white mb-6">
                Join The Elite <span className="text-purple-500">Today</span>
              </h2>
              <p className="text-lg text-gray-400 mb-8">
                Transform your financial future with our exclusive trading platform. Get access to professional-grade tools, AI-powered strategies, and a community of successful traders. Start with our risk-free demo account and experience the difference that elite-level trading makes. Our proven algorithms have helped traders achieve an average of 23% monthly returns.
              </p>
              <div className="mb-6">
                <div className="flex items-center mb-2">
                  <div className="w-4 h-4 bg-green-500 rounded-full mr-3 flex-shrink-0"></div>
                  <span className="text-gray-300">✓ No trading experience required</span>
                </div>
                <div className="flex items-center mb-2">
                  <div className="w-4 h-4 bg-green-500 rounded-full mr-3 flex-shrink-0"></div>
                  <span className="text-gray-300">✓ 24/7 automated trading</span>
                </div>
                <div className="flex items-center">
                  <div className="w-4 h-4 bg-green-500 rounded-full mr-3 flex-shrink-0"></div>
                  <span className="text-gray-300">✓ Free $100,000 demo account</span>
                </div>
              </div>
              <SignedOut>
                <SignInButton mode="modal" className="bg-purple-600 hover:bg-purple-700 text-white px-8 py-3 rounded-full font-semibold transition-colors">
                  Sign Up
                </SignInButton>
              </SignedOut>
              <SignedIn>
                <button className="bg-purple-600 hover:bg-purple-700 text-white px-8 py-3 rounded-full font-semibold transition-colors">
                  Go to Dashboard
                </button>
              </SignedIn>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Crypto Section */}
      <section id="crypto" className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl lg:text-4xl font-bold text-white mb-4">
              Top Cryptocurrencies <span className="text-purple-500">Available for Trading</span>
            </h2>
            <p className="text-lg text-gray-400 max-w-2xl mx-auto">
              Access the most popular cryptocurrencies with real-time pricing, advanced analytics, and instant execution. Our platform supports over 150+ digital assets.
            </p>
          </motion.div>
          {loading ? (
            <div className="text-center text-gray-400">Loading crypto data...</div>
          ) : error ? (
            <div className="text-center text-red-500">Error: {error}</div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
              {cryptoData.map((item, index) => (
                <motion.div
                  key={item.id}
                  initial={{ opacity: 0, y: 30 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  viewport={{ once: true }}
                  className="bg-gray-800 rounded-lg shadow-xl overflow-hidden hover:shadow-2xl transition-shadow border-l-4 border-purple-500"
                >
                  <div className="p-4">
                    <div className="flex items-center justify-between mb-3">
                      <h3 className="font-semibold text-white text-lg">{item.name}</h3>
                      <span className={`text-xs px-2 py-1 rounded-full ${item.change >= 0 ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                        {item.change >= 0 ? '+' : ''}{item.change?.toFixed(2)}%
                      </span>
                    </div>
                    <div className="text-sm text-gray-400 mb-2">{item.symbol}/USD</div>
                    <div className="text-purple-500 font-bold text-xl mb-2">${item.price.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 4 })}</div>
                    <div className="grid grid-cols-2 gap-2 text-xs text-gray-500">
                      <div>Volume (24h):</div>
                      <div>${(item.volume / 1000000000).toFixed(2)}B</div>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* Services Section */}
      <section id="offer" className="py-20 px-4 sm:px-6 lg:px-8 bg-gray-900">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl lg:text-4xl font-bold text-white mb-4">
              What We <span className="text-purple-500">Offer</span>
            </h2>
            <p className="text-lg text-gray-400 max-w-2xl mx-auto">
              Elite Trader provides comprehensive trading solutions designed to maximize your investment potential. From beginner-friendly automation to advanced professional tools, we have everything you need to succeed in the cryptocurrency markets.
            </p>
          </motion.div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {services.map((service, index) => (
              <motion.div
                key={service.title}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.2 }}
                viewport={{ once: true }}
                className="text-center bg-gray-800 p-8 rounded-xl shadow-lg hover:shadow-xl transition-shadow"
              >
                <div className="bg-purple-900/50 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
                  <service.icon className="w-8 h-8 text-purple-400" />
                </div>
                <h3 className="text-xl font-semibold text-white mb-4">{service.title}</h3>
                <p className="text-gray-400 leading-relaxed">{service.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Why Choose Us Section */}
      <section id="choose" className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
            >
              <h2 className="text-3xl lg:text-4xl font-bold text-white mb-8">
                Why <span className="text-purple-500">Choose Elite Trader</span>
              </h2>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-8 mb-8">
                {stats.map((stat, index) => (
                  <motion.div
                    key={stat.label}
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: index * 0.1 }}
                    viewport={{ once: true }}
                    className="text-center"
                  >
                    <div className="text-3xl font-bold text-purple-500 mb-2">{stat.number}</div>
                    <div className="text-gray-400">{stat.label}</div>
                  </motion.div>
                ))}
              </div>
              <p className="text-lg text-gray-400 mb-8">
                Join thousands of successful traders who trust Elite Trader for their cryptocurrency investments. Our proven track record, cutting-edge technology, and commitment to security make us the preferred choice for both novice and experienced traders looking to maximize their returns in the digital asset space.
              </p>
              <SignedOut>
                <SignInButton mode="modal" className="bg-purple-600 hover:bg-purple-700 text-white px-8 py-3 rounded-full font-semibold transition-colors">
                  Sign Up
                </SignInButton>
              </SignedOut>
              <SignedIn>
                <button className="bg-purple-600 hover:bg-purple-700 text-white px-8 py-3 rounded-full font-semibold transition-colors">
                  Go to Dashboard
                </button>
              </SignedIn>
            </motion.div>
            <motion.div
              initial={{ opacity: 0, x: 50 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              viewport={{ once: true }}
            >
              <img
                src="https://images.unsplash.com/photo-1559526324-4b87b5e36e44?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80"
                alt="Professional cryptocurrency trading workspace"
                className="w-full h-auto rounded-lg shadow-2xl"
              />
            </motion.div>
          </div>
        </div>
      </section>

      {/* Sign Up Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-gray-950 via-gray-900 to-black relative overflow-hidden">
        <div className="absolute inset-0">
          <div className="absolute top-20 left-10 w-32 h-32 bg-purple-600 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse"></div>
          <div className="absolute bottom-40 right-20 w-40 h-40 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse delay-1000"></div>
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-60 h-60 bg-purple-700 rounded-full mix-blend-multiply filter blur-2xl opacity-10"></div>
          <div className="absolute inset-0 opacity-5">
            <svg className="w-full h-full text-white" viewBox="0 0 1000 400">
              <polyline
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                points="0,200 100,150 200,180 300,120 400,140 500,80 600,100 700,60 800,90 900,40 1000,70"
              />
            </svg>
          </div>
        </div>
        <div className="max-w-7xl mx-auto relative z-10">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl lg:text-6xl font-bold text-white mb-6">
              Ready to Join the
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-blue-400"> Elite Traders?</span>
            </h2>
            <p className="text-xl text-gray-400 max-w-3xl mx-auto mb-8">
              Transform your financial future with professional-grade trading tools and AI-powered strategies.
              Join the exclusive community of elite traders achieving consistent profits in cryptocurrency markets.
            </p>
          </motion.div>
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 1.0 }}
            viewport={{ once: true }}
            className="text-center"
          >
            <div className="flex flex-col sm:flex-row justify-center gap-4 mb-4">
              <button className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-bold py-3 px-8 rounded-full text-lg transition-all duration-300 transform hover:scale-105 shadow-2xl">
                Start Elite Trading
              </button>
              <button className="bg-white/10 backdrop-blur-sm border-2 border-white/30 text-white font-bold py-3 px-8 rounded-full text-lg hover:bg-white/20 transition-all duration-300">
                View Demo Account
              </button>
            </div>
            <div className="inline-flex items-center gap-2 bg-green-500/20 border border-green-400/30 rounded-full px-4 py-2 my-4">
              <svg className="w-4 h-4 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              <span className="text-green-400 font-medium text-sm">Risk-Free Demo Account Available</span>
            </div>
            <p className="text-gray-400 text-sm max-w-xl mx-auto">
              Join the elite with a free demo account including $100,000 virtual funds. No commitment required - experience professional trading today.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-950 text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="col-span-1 md:col-span-2">
              <div className="text-2xl font-bold text-purple-500 mb-4">Elite Trader</div>
              <p className="text-gray-400 mb-6 max-w-md">
                The premier cryptocurrency trading platform for professionals and beginners alike. Join thousands of successful traders using our advanced AI-powered tools and institutional-grade security to maximize their investment returns.
              </p>
              <div className="flex space-x-4">
                <a href="#" className="bg-gray-800 hover:bg-purple-600 p-3 rounded-full transition-colors">
                  <Facebook className="w-5 h-5" />
                </a>
                <a href="#" className="bg-gray-800 hover:bg-purple-600 p-3 rounded-full transition-colors">
                  <Twitter className="w-5 h-5" />
                </a>
                <a href="#" className="bg-gray-800 hover:bg-purple-600 p-3 rounded-full transition-colors">
                  <Instagram className="w-5 h-5" />
                </a>
                <a href="#" className="bg-gray-800 hover:bg-purple-600 p-3 rounded-full transition-colors">
                  <Youtube className="w-5 h-5" />
                </a>
              </div>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-4 text-white">Trading Platform</h3>
              <ul className="space-y-2">
                <li><a href="#" className="text-gray-400 hover:text-purple-400 transition-colors">Live Trading</a></li>
                <li><a href="#" className="text-gray-400 hover:text-purple-400 transition-colors">Demo Account</a></li>
                <li><a href="#" className="text-gray-400 hover:text-purple-400 transition-colors">Market Analysis</a></li>
                <li><a href="#" className="text-gray-400 hover:text-purple-400 transition-colors">Trading Tools</a></li>
                <li><a href="#" className="text-gray-400 hover:text-purple-400 transition-colors">Mobile App</a></li>
              </ul>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-4 text-white">Support & Legal</h3>
              <ul className="space-y-2">
                <li><a href="#" className="text-gray-400 hover:text-purple-400 transition-colors">Help Center</a></li>
                <li><a href="#" className="text-gray-400 hover:text-purple-400 transition-colors">Contact Support</a></li>
                <li><a href="#" className="text-gray-400 hover:text-purple-400 transition-colors">Security Info</a></li>
                <li><a href="#" className="text-gray-400 hover:text-purple-400 transition-colors">Privacy Policy</a></li>
                <li><a href="#" className="text-gray-400 hover:text-purple-400 transition-colors">Terms of Service</a></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-12 pt-8 flex flex-col md:flex-row justify-between items-center">
            <p className="text-gray-400 text-sm">© 2025 Elite Trader Inc. All rights reserved. Licensed and regulated financial services.</p>
            <div className="flex space-x-6 mt-4 md:mt-0">
              <a href="#" className="text-gray-400 hover:text-purple-400 text-sm transition-colors">Risk Disclosure</a>
              <a href="#" className="text-gray-400 hover:text-purple-400 text-sm transition-colors">Compliance</a>
              <a href="#" className="text-gray-400 hover:text-purple-400 text-sm transition-colors">Investor Protection</a>
            </div>
          </div>
          <div className="mt-8 p-4 bg-yellow-900/20 border border-yellow-600/30 rounded-lg">
            <p className="text-yellow-300 text-xs text-center">
              <strong>Risk Warning:</strong> Trading cryptocurrencies involves substantial risk of loss and is not suitable for all investors. Past performance does not guarantee future results. Please ensure you fully understand the risks involved and seek independent advice if necessary.
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}
