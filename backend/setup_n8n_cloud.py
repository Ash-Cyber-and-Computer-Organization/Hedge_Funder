#!/usr/bin/env python3
"""
N8N Cloud Setup Script
Automates the setup process for linking local backend with N8N cloud
"""

import json
import os
import subprocess
import requests
import time
from pathlib import Path

class N8NCloudSetup:
    def __init__(self):
        self.config_file = 'n8n_workflow_config.json'
        self.env_file = '.env'
        self.ngrok_url = None

    def check_ngrok_installation(self):
        """Check if ngrok is installed"""
        try:
            result = subprocess.run(['ngrok', 'version'], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Ngrok is installed")
                return True
            else:
                print("❌ Ngrok not found. Please install ngrok first:")
                print("   npm install -g ngrok")
                return False
        except FileNotFoundError:
            print("❌ Ngrok not found. Please install ngrok first:")
            print("   npm install -g ngrok")
            return False

    def start_ngrok_tunnel(self, port=5001):
        """Start ngrok tunnel"""
        print(f"🚀 Starting ngrok tunnel on port {port}...")
        try:
            # Start ngrok in background
            process = subprocess.Popen(['ngrok', 'http', str(port)],
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)

            # Wait for ngrok to start
            time.sleep(3)

            # Get ngrok URL from API
            response = requests.get('http://localhost:4040/api/tunnels')
            if response.status_code == 200:
                tunnels = response.json()['tunnels']
                https_tunnel = next((t for t in tunnels if t['proto'] == 'https'), None)
                if https_tunnel:
                    self.ngrok_url = https_tunnel['public_url']
                    print(f"✅ Ngrok tunnel established: {self.ngrok_url}")
                    return True

            print("❌ Failed to get ngrok URL")
            return False

        except Exception as e:
            print(f"❌ Error starting ngrok: {e}")
            return False

    def update_config_files(self):
        """Update configuration files with ngrok URL"""
        if not self.ngrok_url:
            print("❌ No ngrok URL available")
            return False

        print("📝 Updating configuration files...")

        # Update n8n_workflow_config.json
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)

            # Update cloud environment URLs
            config['environments']['cloud']['base_url'] = self.ngrok_url

            # Update workflow endpoints
            for workflow_name, workflow in config['workflows'].items():
                if 'endpoints' in workflow:
                    workflow['endpoints']['cloud'] = self.ngrok_url + '/api' + workflow['webhook_path'].replace('/webhook', '')

            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)

            print(f"✅ Updated {self.config_file}")

        except Exception as e:
            print(f"❌ Error updating {self.config_file}: {e}")
            return False

        # Update .env file
        try:
            env_content = f"""# N8N Cloud Configuration
N8N_CLOUD_URL=https://ash1industries.app.n8n.cloud
N8N_WEBHOOK_BASE=https://ash1industries.app.n8n.cloud/webhook
N8N_API_KEY=your_n8n_api_key_here

# Local Backend Configuration
LOCAL_BACKEND_URL=http://localhost:5001
BACKEND_PORT=5001

# Ngrok Configuration
NGROK_URL={self.ngrok_url}

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here

# Risk Management
MAX_DAILY_LOSS=100.0
MAX_POSITION_SIZE=0.1
MAX_OPEN_POSITIONS=3

# Environment
ENVIRONMENT=development
"""

            with open(self.env_file, 'w') as f:
                f.write(env_content)

            print(f"✅ Updated {self.env_file}")

        except Exception as e:
            print(f"❌ Error updating {self.env_file}: {e}")
            return False

        return True

    def test_backend_connection(self):
        """Test connection to local backend"""
        print("🔍 Testing local backend connection...")
        try:
            response = requests.get('http://localhost:5001/api/health', timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Backend is running: {data['status']} (v{data['version']})")
                return True
            else:
                print(f"❌ Backend returned status {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Cannot connect to backend: {e}")
            print("   Make sure your backend is running: python n8n_api.py")
            return False

    def test_ngrok_connection(self):
        """Test connection through ngrok"""
        if not self.ngrok_url:
            return False

        print("🌐 Testing ngrok connection...")
        try:
            response = requests.get(f"{self.ngrok_url}/api/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Ngrok tunnel working: {data['status']} (v{data['version']})")
                return True
            else:
                print(f"❌ Ngrok returned status {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Cannot connect through ngrok: {e}")
            return False

    def generate_n8n_workflow_json(self):
        """Generate N8N workflow JSON for import"""
        print("📋 Generating N8N workflow templates...")

        workflow_template = {
            "name": "Hedge Funder - News Analysis & Signals",
            "nodes": [
                {
                    "parameters": {
                        "httpMethod": "POST",
                        "path": "trading-signals",
                        "options": {}
                    },
                    "name": "Webhook",
                    "type": "n8n-nodes-base.webhook",
                    "typeVersion": 1,
                    "position": [240, 300]
                },
                {
                    "parameters": {
                        "url": f"{self.ngrok_url}/api/signals/generate",
                        "method": "POST",
                        "sendBody": True,
                        "bodyContentType": "json",
                        "specifyBody": "json",
                        "jsonBody": {
                            "symbols": ["AAPL", "GOOGL", "MSFT", "TSLA", "NVDA"],
                            "days_back": 3
                        },
                        "headerParameters": {
                            "parameter": [
                                {
                                    "name": "Content-Type",
                                    "value": "application/json"
                                }
                            ]
                        }
                    },
                    "name": "HTTP Request",
                    "type": "n8n-nodes-base.httpRequest",
                    "typeVersion": 3,
                    "position": [460, 300]
                },
                {
                    "parameters": {
                        "functionCode": "const signals = $node[\"HTTP Request\"].json.signals;\n\n// Filter high-confidence signals\nlet validSignals = signals.filter(signal => signal.confidence > 0.6 && signal.risk_validated);\n\nlet message = '🚀 **Trading Signals Generated**\\n\\n';\n\nif (validSignals.length > 0) {\n  validSignals.forEach(signal => {\n    message += `📊 **${signal.symbol}**: ${signal.signal}\\n`;\n    message += `🎯 Confidence: ${(signal.confidence * 100).toFixed(1)}%\\n`;\n    message += `📝 Reason: ${signal.reason}\\n\\n`;\n  });\n} else {\n  message += '⚠️ No high-confidence signals found\\n';\n}\n\nreturn [{ json: { message, signals: validSignals } }];"
                    },
                    "name": "Function",
                    "type": "n8n-nodes-base.function",
                    "typeVersion": 1,
                    "position": [680, 300]
                }
            ],
            "connections": {
                "Webhook": {
                    "main": [
                        [
                            {
                                "node": "HTTP Request",
                                "type": "main",
                                "index": 0
                            }
                        ]
                    ]
                },
                "HTTP Request": {
                    "main": [
                        [
                            {
                                "node": "Function",
                                "type": "main",
                                "index": 0
                            }
                        ]
                    ]
                }
            },
            "settings": {},
            "staticData": None
        }

        with open('n8n_workflow_template.json', 'w') as f:
            json.dump(workflow_template, f, indent=2)

        print("✅ Generated n8n_workflow_template.json")
        print("   Import this file into your N8N cloud instance")

    def run_setup(self):
        """Run the complete setup process"""
        print("🚀 Starting N8N Cloud Setup")
        print("=" * 50)

        # Check prerequisites
        if not self.check_ngrok_installation():
            return False

        if not self.test_backend_connection():
            return False

        # Start ngrok
        if not self.start_ngrok_tunnel():
            return False

        # Update configurations
        if not self.update_config_files():
            return False

        # Test connections
        if not self.test_ngrok_connection():
            print("⚠️  Warning: Ngrok connection test failed")
            print("   This might be due to ngrok startup time")

        # Generate workflow template
        self.generate_n8n_workflow_json()

        print("\n" + "=" * 50)
        print("🎉 Setup Complete!")
        print("=" * 50)
        print(f"🌐 Ngrok URL: {self.ngrok_url}")
        print("📁 Updated files:")
        print(f"   - {self.config_file}")
        print(f"   - {self.env_file}")
        print("   - n8n_workflow_template.json")
        print("\n📋 Next Steps:")
        print("1. Import n8n_workflow_template.json into N8N cloud")
        print("2. Test the workflow manually")
        print("3. Configure Telegram notifications (optional)")
        print("4. Enable automatic scheduling")
        print("\n🔗 N8N Cloud Dashboard:")
        print("   https://ash1industries.app.n8n.cloud")

        return True

def main():
    """Main setup function"""
    setup = N8NCloudSetup()
    success = setup.run_setup()

    if not success:
        print("\n❌ Setup failed. Please check the errors above.")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
