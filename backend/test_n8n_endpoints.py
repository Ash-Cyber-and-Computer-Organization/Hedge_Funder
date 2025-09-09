#!/usr/bin/env python3
"""
Test script to verify N8N API endpoints are working correctly
Run this before configuring N8N workflows
"""

import requests
import json
import time
from datetime import datetime

class N8NEndpointTester:
    def __init__(self, base_url="http://localhost:5001"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'N8N-Endpoint-Tester/1.0'
        })

    def test_health_check(self):
        """Test the health check endpoint"""
        print("🔍 Testing Health Check Endpoint...")
        try:
            response = self.session.get(f"{self.base_url}/api/health")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Health Check: {data['status']} (v{data['version']})")
                return True
            else:
                print(f"❌ Health Check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Health Check error: {e}")
            return False

    def test_news_analysis(self, symbol="AAPL", days_back=3):
        """Test news analysis endpoint"""
        print(f"📰 Testing News Analysis for {symbol}...")
        try:
            payload = {
                "symbol": symbol,
                "days_back": days_back
            }
            response = self.session.post(f"{self.base_url}/api/news/analyze", json=payload)

            if response.status_code == 200:
                data = response.json()
                if 'error' in data:
                    print(f"⚠️  News Analysis: {data['error']}")
                    return False
                else:
                    article_count = data.get('news_articles', [])
                    sentiment = data.get('sentiment_data', {}).get('overall_score', 0)
                    print(f"✅ News Analysis: {len(article_count)} articles, sentiment: {sentiment:.3f}")
                    return True
            else:
                print(f"❌ News Analysis failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ News Analysis error: {e}")
            return False

    def test_signal_generation(self, symbols=None, days_back=3):
        """Test signal generation endpoint"""
        if symbols is None:
            symbols = ["AAPL", "GOOGL", "MSFT"]

        print(f"📊 Testing Signal Generation for {symbols}...")
        try:
            payload = {
                "symbols": symbols,
                "days_back": days_back
            }
            response = self.session.post(f"{self.base_url}/api/signals/generate", json=payload)

            if response.status_code == 200:
                data = response.json()
                signals = data.get('signals', [])
                print(f"✅ Signal Generation: {len(signals)} signals generated")

                for signal in signals:
                    print(f"   📈 {signal['symbol']}: {signal['signal']} (confidence: {signal['confidence']:.3f})")
                return True
            else:
                print(f"❌ Signal Generation failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Signal Generation error: {e}")
            return False

    def test_monitoring_dashboard(self):
        """Test monitoring dashboard endpoint"""
        print("📊 Testing Monitoring Dashboard...")
        try:
            response = self.session.get(f"{self.base_url}/api/monitoring/dashboard")

            if response.status_code == 200:
                data = response.json()
                status = data.get('system_status', {})
                performance = data.get('performance', {})
                risk = data.get('risk_metrics', {})

                print("✅ Monitoring Dashboard:")
                print(f"   🔗 MT5 Connection: {'✅' if status.get('mt5_connection') else '❌'}")
                print(f"   📈 Daily P&L: ${performance.get('daily_pnl', 0)}")
                print(f"   🎯 Success Rate: {performance.get('success_rate', 0)*100:.1f}%")
                print(f"   ⚠️  Max Daily Loss: ${risk.get('max_daily_loss', 0)}")
                return True
            else:
                print(f"❌ Monitoring Dashboard failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Monitoring Dashboard error: {e}")
            return False

    def test_trade_execution(self, signal_data=None):
        """Test trade execution endpoint"""
        if signal_data is None:
            signal_data = {
                "symbol": "AAPL",
                "signal": "BUY",
                "confidence": 0.85
            }

        print(f"💰 Testing Trade Execution for {signal_data['symbol']}...")
        try:
            payload = {"signal": signal_data}
            response = self.session.post(f"{self.base_url}/api/trade/execute", json=payload)

            if response.status_code == 200:
                data = response.json()
                success = data.get('success', False)
                print(f"✅ Trade Execution: {'Success' if success else 'Failed'}")
                if success:
                    print(f"   📝 Signal: {data.get('formatted_signal', 'N/A')}")
                return success
            else:
                print(f"❌ Trade Execution failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Trade Execution error: {e}")
            return False

    def test_alert_sending(self, message="Test alert from N8N tester"):
        """Test alert sending endpoint"""
        print("📢 Testing Alert Sending...")
        try:
            payload = {
                "message": message,
                "type": "test"
            }
            response = self.session.post(f"{self.base_url}/api/alerts/send", json=payload)

            if response.status_code == 200:
                data = response.json()
                success = data.get('success', False)
                print(f"✅ Alert Sending: {'Success' if success else 'Failed'}")
                return success
            else:
                print(f"❌ Alert Sending failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Alert Sending error: {e}")
            return False

    def run_full_test_suite(self):
        """Run complete test suite"""
        print("🚀 Starting N8N API Endpoint Test Suite")
        print("=" * 50)

        tests = [
            ("Health Check", self.test_health_check),
            ("News Analysis", lambda: self.test_news_analysis()),
            ("Signal Generation", self.test_signal_generation),
            ("Monitoring Dashboard", self.test_monitoring_dashboard),
            ("Trade Execution", self.test_trade_execution),
            ("Alert Sending", self.test_alert_sending)
        ]

        results = []
        for test_name, test_func in tests:
            print(f"\n🔬 Running {test_name}...")
            try:
                result = test_func()
                results.append((test_name, result))
                time.sleep(1)  # Brief pause between tests
            except Exception as e:
                print(f"❌ {test_name} crashed: {e}")
                results.append((test_name, False))

        # Summary
        print("\n" + "=" * 50)
        print("📋 TEST RESULTS SUMMARY")
        print("=" * 50)

        passed = 0
        total = len(results)

        for test_name, result in results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test_name}")
            if result:
                passed += 1

        print(f"\n🎯 Overall: {passed}/{total} tests passed")

        if passed == total:
            print("🎉 All tests passed! Your N8N API is ready for production.")
            print("\n📝 Next steps:")
            print("1. Start N8N: n8n start")
            print("2. Open http://localhost:5678")
            print("3. Import workflows from n8n_workflow_examples.json")
            print("4. Configure Telegram credentials")
            print("5. Test workflows manually first")
        else:
            print("⚠️  Some tests failed. Check the Flask API logs for details.")
            print("🔧 Common fixes:")
            print("- Ensure all required API keys are set in .env")
            print("- Check MT5 connection if trade tests fail")
            print("- Verify news API endpoints are accessible")

        return passed == total

def main():
    """Main test function"""
    print("🤖 N8N API Endpoint Tester")
    print("This script tests all endpoints that N8N will use")
    print()

    # Test local API
    tester = N8NEndpointTester()

    success = tester.run_full_test_suite()

    if success:
        print("\n🌐 For production deployment:")
        print("1. Deploy Flask API to Vercel")
        print("2. Update n8n_workflow_config.json with production URLs")
        print("3. Test production endpoints")
        print("4. Update N8N workflows with production URLs")

    return success

if __name__ == "__main__":
    main()
