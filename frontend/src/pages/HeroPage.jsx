const HeroPage = () => {
    return ( 
        <>
     <div className="min-h-screen bg-black text-white relative overflow-hidden">
      {/* Background decorative elements */}
      {/* <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-32 left-32 w-24 h-24 border border-gray-700">
          <div className="absolute top-1/2 left-1/2 w-2 h-2 bg-gray-600 rounded-full transform -translate-x-1/2 -translate-y-1/2"></div>
        </div>
        <div className="absolute top-96 right-32 w-32 h-32 border border-gray-700">
          <div className="absolute top-1/2 left-1/2 w-2 h-2 bg-gray-600 rounded-full transform -translate-x-1/2 -translate-y-1/2"></div>
        </div>
        <div className="absolute bottom-32 right-64 w-20 h-20 border border-gray-700">
          <div className="absolute top-1/2 left-1/2 w-2 h-2 bg-gray-600 rounded-full transform -translate-x-1/2 -translate-y-1/2"></div>
        </div>
        <div className="absolute bottom-96 left-64 w-16 h-16 border border-gray-700">
          <div className="absolute top-1/2 left-1/2 w-2 h-2 bg-gray-600 rounded-full transform -translate-x-1/2 -translate-y-1/2"></div>
        </div>
      </div> */}

      {/* Header */}
      <header className="relative z-10 px-6 py-4">
        <nav className="flex items-center justify-between max-w-7xl mx-auto">
          {/* Logo */}
          <div className="flex items-center space-x-2">
            <div className="text-xl font-bold">Elite Trader</div>
          </div>

          {/* Navigation Menu */}
          <div className="hidden md:flex items-center space-x-8">
            <a href="#" className="text-white hover:text-gray-300 transition-colors">
              Home
            </a>
            <a href="#" className="text-gray-400 hover:text-white transition-colors">
              About Us
            </a>
            <a href="#" className="text-gray-400 hover:text-white transition-colors">
              Crypto Prices And Live Data
            </a>
            <a href="#" className="text-gray-400 hover:text-white transition-colors">
              Makers
            </a>
            <a href="#" className="text-gray-400 hover:text-white transition-colors">
              Pricing
            </a>
          </div>

          {/* Auth buttons */}
          <div className="flex items-center space-x-4">
            <button className="text-gray-400 hover:text-white transition-colors">Log in</button>
            <button variant="outline" className="border-gray-600 text-white hover:bg-gray-800 bg-transparent">
              Create account
            </button>
          </div>
        </nav>
      </header>

      {/* Hero Section */}
      <main className="relative z-10 px-6 py-20">
        <div className="max-w-4xl mx-auto text-center">
          {/* Trust Badge */}
          <div className="inline-flex items-center space-x-2 bg-gray-900 rounded-full px-4 py-2 mb-8">
            <span className="text-sm text-gray-300">Top Trading Experience</span>
          </div>

          {/* Main Headline */}
          <h1 className="text-5xl md:text-6xl font-bold mb-6 leading-tight">
            We Provide
            <br />
            Seamless Live Trading
            <br />
             On The Go
          </h1>

          {/* Subheading */}
          <p className="text-xl text-gray-400 mb-12 max-w-2xl mx-auto">
            Track, Grow, Save, and Trade CryptoCurrency easily and fast
            <br />
            With Real Transaction History 
            <br />
            And A Seamless User Experience
          </p>

          {/* CTA buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-4">
            <button size="lg" className="bg-white text-black hover:bg-gray-200 px-8 py-3 text-lg">
              Sign Up
            </button>
            <button
              variant="outline"
              size="lg"
              className="border-gray-600 text-white hover:bg-gray-800 px-8 py-3 text-lg bg-transparent"
            >
              Login
            </button>
          </div>
        </div>
      </main>

      {/* Trusted By Section */}
      <section className="relative z-10 px-6 py-16">
        <div className="max-w-6xl mx-auto text-center">
          <p className="text-gray-400 mb-12 text-lg">Trade in</p>

          <div className="flex flex-wrap items-center justify-center space-x-8 space-y-4">
            <div className="flex items-center space-x-2 bg-gray-900 rounded-lg px-6 py-4">
              {/* <div className="w-6 h-6 bg-gradient-to-r from-purple-400 to-pink-400 rounded"></div> */}
              <span className="text-white font-semibold text-lg">BitCoin</span>
            </div>

            <div className="flex items-center space-x-2 bg-gray-900 rounded-lg px-6 py-4">
              {/* <div className="w-6 h-6 bg-blue-500 rounded-full"></div> */}
              <span className="text-white font-semibold text-lg">Etherum</span>
            </div>

            <div className="flex items-center space-x-2 bg-gray-900 rounded-lg px-6 py-4">
              {/* <div className="w-6 h-6 bg-pink-500 rounded-full"></div> */}
              <span className="text-white font-semibold text-lg">BNB</span>
            </div>

            <div className="flex items-center space-x-2 bg-gray-900 rounded-lg px-6 py-4">
              {/* <div className="w-6 h-6 bg-purple-600 rounded"></div> */}
              <span className="text-white font-semibold text-lg">Sui</span>
            </div>

            <div className="flex items-center space-x-2 bg-gray-900 rounded-lg px-6 py-4">
              {/* <div className="w-6 h-6 bg-green-500 rounded"></div> */}
              <span className="text-white font-semibold text-lg">And Many More</span>
            </div>
          </div>
        </div>
      </section>
    </div> 
        </>
     );
}
 
export default HeroPage;