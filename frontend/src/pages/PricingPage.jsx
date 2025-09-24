"use client"

import { motion } from "framer-motion"
import { Link } from "react-router-dom"
import { Check, Star, Zap, Crown, Shield, Users, TrendingUp, Award, Target } from "lucide-react"
import PublicLayout from "../layout/PublicLayout"


// Framer Motion variants
const fadeInUp = {
  initial: { opacity: 0, y: 30 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.8, ease: "easeOut" }
}

const staggerContainer = {
  animate: {
    transition: {
      staggerChildren: 0.15
    }
  }
}

const planCardHover = {
  hover: {
    y: -10,
    scale: 1.05,
    boxShadow: "0 10px 20px rgba(128, 90, 213, 0.3)",
    transition: {
      duration: 0.3,
      ease: "easeOut"
    }
  }
}

const PricingPage = () => {
  const plans = [
    {
      name: "Demo",
      price: "Free",
      period: "Forever",
      description: "Perfect for learning and testing strategies",
      icon: Star,
      features: [
        "$100,000 virtual trading balance",
        "Real-time market data",
        "Basic charting tools",
        "Educational resources",
        "Community access",
        "Mobile app access",
      ],
      cta: "Start Demo",
      popular: false,
      color: "gray",
    },
    {
      name: "Trader",
      price: "$29",
      period: "per month",
      description: "For serious traders ready to go live",
      icon: Zap,
      features: [
        "Live trading with real funds",
        "Advanced charting & analytics",
        "Real-time market alerts",
        "Portfolio management tools",
        "Priority customer support",
        "API access for automation",
        "Risk management tools",
        "Tax reporting features",
      ],
      cta: "Start Trading",
      popular: true,
      color: "purple",
    },
    {
      name: "Elite Pro",
      price: "$99",
      period: "per month",
      description: "Ultimate package with AI-powered EliteBot",
      icon: Crown,
      features: [
        "Everything in Trader plan",
        "EliteBot AI trading assistant",
        "Advanced AI strategies",
        "Automated portfolio rebalancing",
        "Custom trading algorithms",
        "Dedicated account manager",
        "Institutional-grade analytics",
        "White-glove onboarding",
        "Priority trade execution",
      ],
      cta: "Go Elite",
      popular: false,
      color: "gradient",
    },
  ]

  const faqs = [
    {
      question: "What is EliteBot?",
      answer:
        "EliteBot is our proprietary AI trading assistant that uses advanced machine learning algorithms to analyze market patterns, execute trades automatically, and optimize your portfolio for maximum returns while managing risk.",
    },
    {
      question: "Can I switch between plans?",
      answer:
        "Yes, you can upgrade or downgrade your plan at any time. Changes take effect immediately, and we'll prorate any billing adjustments.",
    },
    {
      question: "Is there a free trial for paid plans?",
      answer:
        "We offer a 14-day free trial for both Trader and Elite Pro plans. You can cancel anytime during the trial period without being charged.",
    },
    {
      question: "How secure are my funds?",
      answer:
        "We use bank-level security with multi-factor authentication, cold storage wallets, and insurance coverage. Your funds are protected by industry-leading security protocols.",
    },
    {
      question: "What cryptocurrencies can I trade?",
      answer:
        "We support over 150+ cryptocurrencies including Bitcoin, Ethereum, and all major altcoins. Our platform connects to multiple exchanges for the best liquidity and pricing.",
    },
  ]

  return (
    <PublicLayout>
     <div className="min-h-screen bg-black text-gray-300 overflow-hidden font-inter">
      {/* Background for a simple aesthetic */}
      <div className="absolute inset-0 z-0 bg-black opacity-60"></div>

      {/* Hero Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 relative z-10 text-center">
        
          <h1 className="text-3xl lg:text-5xl font-bold text-white leading-tight">
            Elevate Your <span className="text-purple-500">Trading Game</span>
          </h1>
          <p className="text-lg text-gray-400 max-w-2xl mx-auto leading-relaxed">
            Unleash the power of professional-grade tools and AI-driven insights with a plan that fits your ambition.
          </p>
      </section>

      {/* Pricing Cards */}
      <section className="py-12 px-4 sm:px-6 lg:px-8 relative z-20">
        <div className="max-w-6xl mx-auto">
          <motion.div
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true, amount: 0.2 }}
            className="grid grid-cols-1 md:grid-cols-3 gap-6"
          >
            {plans.map((plan, index) => (
              <motion.div
                key={plan.name}
                variants={fadeInUp}
                whileHover="hover"
                className={`relative p-1 rounded-xl transition-all duration-300 ${
                  plan.popular ? "bg-gradient-to-r from-purple-500 to-cyan-500" : "bg-gray-800/50"
                } hover:shadow-lg hover:shadow-purple-500/20`}
              >
                <div
                  className="relative bg-gray-900/90 backdrop-blur-sm rounded-xl overflow-hidden border border-gray-700/50 p-6 h-full flex flex-col justify-between"
                >
                  {plan.popular && (
                    <div className="absolute top-0 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
                      
                    </div>
                  )}

                  <div className="text-center mb-6">
                    <div
                      className={`inline-flex items-center justify-center w-12 h-12 rounded-full mb-3 ring-2 ring-offset-2 ring-offset-gray-900 ${
                        plan.color === "gradient"
                          ? "bg-gradient-to-r from-purple-600 to-purple-700 ring-purple-500"
                          : plan.color === "purple"
                            ? "bg-purple-600 ring-purple-500"
                            : "bg-gray-700 ring-gray-600"
                      }`}
                    >
                      <plan.icon className="w-6 h-6 text-white" />
                    </div>
                    <h3 className="text-xl font-bold text-white mb-1">{plan.name}</h3>
                    <p className="text-gray-400 text-sm mb-3">{plan.description}</p>
                    <div className="mb-3">
                      <span className="text-3xl font-bold text-white">{plan.price}</span>
                      {plan.period !== "Forever" && <span className="text-gray-400 ml-1">{plan.period}</span>}
                    </div>
                  </div>

                  <ul className="space-y-3 mb-6 flex-grow">
                    {plan.features.map((feature, featureIndex) => (
                      <li key={featureIndex} className="flex items-start text-sm">
                        <Check className="w-4 h-4 text-purple-500 mr-2 mt-0.5 flex-shrink-0" />
                        <span className="text-gray-300">{feature}</span>
                      </li>
                    ))}
                  </ul>

                  <a
                    href="#"
                    className={`block w-full text-center py-2 px-4 rounded-full font-semibold transition-all duration-300 shadow-md ${
                      plan.color === "gradient"
                        ? "bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-500 hover:to-purple-600 text-white"
                        : plan.color === "purple"
                          ? "bg-purple-600 hover:bg-purple-700 text-white"
                          : "bg-gray-700 hover:bg-gray-600 text-white"
                    }`}
                  >
                    {plan.cta}
                  </a>
                </div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="py-12 px-4 sm:px-6 lg:px-8 bg-black/50 relative z-10">
        <div className="max-w-4xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <h2 className="text-2xl lg:text-3xl font-bold text-white mb-2">
              Frequently Asked <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-500">Questions</span>
            </h2>
          </motion.div>

          <motion.div
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true, amount: 0.2 }}
            className="space-y-4"
          >
            {faqs.map((faq, index) => (
              <motion.div
                key={index}
                variants={fadeInUp}
                className="bg-gray-800/80 backdrop-blur-sm rounded-lg p-5 border border-gray-700/50 hover:border-purple-500/50 transition-colors duration-300"
              >
                <h3 className="text-lg font-semibold text-white mb-2">{faq.question}</h3>
                <p className="text-gray-400 text-sm leading-relaxed">{faq.answer}</p>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-black/50 relative text-center z-10">
        <div className="max-w-3xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="space-y-6"
          >
            <h2 className="text-4xl lg:text-5xl font-light text-white leading-tight">
              Ready to Join the
              <span className="block text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-purple-600 font-normal">
                Elite?
              </span>
            </h2>
            <p className="text-lg text-gray-400 max-w-2xl mx-auto font-light">
              Transform your trading with professional-grade tools and AI-powered strategies.
            </p>
            <div className="pt-4">
              <Link
                to="/signin"
                className="inline-block bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-500 hover:to-purple-600 text-white font-medium py-3 px-8 rounded-full text-lg transition-all duration-300 shadow-lg hover:shadow-purple-500/25"
              >
                Start Trading
              </Link>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
    </PublicLayout>
  )
}

export default PricingPage