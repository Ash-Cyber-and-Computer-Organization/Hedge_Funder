#!/usr/bin/env python3
"""
Setup script for Hedge Funder Backend with MongoDB integration
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        logger.error("❌ Python 3.8 or higher is required")
        return False
    logger.info(f"✅ Python version {sys.version.split()[0]} is compatible")
    return True

def install_dependencies():
    """Install Python dependencies"""
    try:
        logger.info("📦 Installing Python dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        logger.info("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed to install dependencies: {e}")
        return False

def check_mongodb():
    """Check if MongoDB is installed and running"""
    try:
        # Try to import pymongo to check if it's available
        import pymongo
        logger.info("✅ PyMongo is available")

        # Try to connect to MongoDB
        from pymongo import MongoClient
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)

        # Test connection
        client.admin.command('ping')
        logger.info("✅ MongoDB is running and accessible")
        return True

    except ImportError:
        logger.warning("⚠️ PyMongo not found. Please install MongoDB Python driver.")
        return False
    except Exception as e:
        logger.warning(f"⚠️ MongoDB connection failed: {e}")
        logger.info("💡 Please ensure MongoDB is installed and running:")
        logger.info("   - Download: https://www.mongodb.com/try/download/community")
        logger.info("   - Or use Docker: docker run -d -p 27017:27017 --name mongodb mongo:latest")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path('.env')
    if not env_file.exists():
        logger.info("📝 Creating .env file template...")
        env_content = """# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017/
MONGODB_DATABASE=hedge_funder

# API Keys (use your actual keys)
FINNHUB_API_KEY=your_finnhub_api_key_here
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key_here
TWELVE_DATA_API_KEY=your_twelve_data_api_key_here

# Data Configuration
DEFAULT_TICKERS=AAPL,GOOGL,MSFT,TSLA
CACHE_DAYS=30
CACHE_HOURS=24
CACHE_MINUTES=60
"""
        env_file.write_text(env_content)
        logger.info("✅ .env file created. Please update with your API keys.")
        return True
    else:
        logger.info("✅ .env file already exists")
        return True

def run_tests():
    """Run the integration tests"""
    try:
        logger.info("🧪 Running MongoDB integration tests...")
        result = subprocess.run([sys.executable, "test_mongodb_integration.py"],
                              capture_output=True, text=True)

        if result.returncode == 0:
            logger.info("✅ All tests passed!")
            logger.info(result.stdout)
            return True
        else:
            logger.error("❌ Some tests failed:")
            logger.error(result.stderr)
            return False

    except FileNotFoundError:
        logger.warning("⚠️ Test file not found. Skipping tests.")
        return True
    except Exception as e:
        logger.error(f"❌ Error running tests: {e}")
        return False

def main():
    """Main setup function"""
    logger.info("🚀 Starting Hedge Funder Backend Setup...")

    steps = [
        ("Check Python Version", check_python_version),
        ("Install Dependencies", install_dependencies),
        ("Check MongoDB", check_mongodb),
        ("Create Environment File", create_env_file),
        ("Run Tests", run_tests)
    ]

    passed = 0
    total = len(steps)

    for step_name, step_func in steps:
        logger.info(f"\n🔍 {step_name}...")
        if step_func():
            passed += 1
        else:
            logger.error(f"❌ {step_name} failed")

    logger.info(f"\n📋 Setup Results: {passed}/{total} steps completed")

    if passed == total:
        logger.info("🎉 Setup completed successfully!")
        logger.info("\n📖 Next Steps:")
        logger.info("1. Update .env file with your API keys")
        logger.info("2. Start MongoDB if not already running")
        logger.info("3. Run: python -c 'from market_analysis_algorithm.market_analysis import run_market_analysis; print(run_market_analysis())'")
        return 0
    else:
        logger.error("❌ Setup incomplete. Please resolve the issues above.")
        logger.info("\n🔧 Troubleshooting:")
        logger.info("- Ensure MongoDB is installed and running")
        logger.info("- Check your internet connection for pip installs")
        logger.info("- Verify API keys in .env file")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
