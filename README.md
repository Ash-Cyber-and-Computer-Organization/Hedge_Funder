
# Hedge_Funder.

___

Hedge_Funder is an automated and autonomous trading and sentiment analysis platform, combining a Telegram signal listener, news sentiment scraper, and trade executor for the  MetaTrader 5 platform. The project includes both backend (Python) and frontend (Next.js/React) components, with supporting scripts and database storage.

## Project Structure

```
Hedge_Funder/
├── backend/
│   ├── telegram_bot.py       # Telegram signal listener
│   ├── web_scraper.py        # News scraper and sentiment analyzer
│   ├── trading_module.py     # MT5 trade executor
│   ├── api_server.py         # REST API server
│   ├── database.py           # SQLite database operations
│   ├── utils.py              # Helper functions
│   └── config.py             # Configuration settings
├── frontend/
│   ├── pages/                # Next.js pages
│   ├── components/           # React components
│   ├── package.json          # Frontend dependencies
│   └── ...                   # Other frontend files
├── scripts/
│   ├── install_mt5.sh        # Script to install MT5 via Wine
│   ├── setup_services.sh     # Script to configure systemd services
│   └── ...                   # Additional setup scripts
├── data/
│   ├── database.sqlite       # SQLite database file
│   └── ...                   # Other data files
└── README.md                 # Project documentation
```
<!-- Need to change directory's index
- we added new features like package.json
- vercel.json
-->
## Features

- **Telegram Signal Listener**: Connects to Telegram channels and parses trading signals.
- **News Scraper & Sentiment Analyzer**: Scrapes financial news and analyzes sentiment for trading decisions.
- **MT5 Trade Executor**: Executes trades via MetaTrader 5 with automated strategies.
- **REST API Server**: Provides API endpoints for frontend integration.
- **Web Dashboard**: Next.js/React frontend for monitoring trades, viewing signals, and analytics.

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/Ash-Cyber-and-Computer-Organization/Hedge_Funder.git
cd Hedge_Funder
```

### 2. Backend Setup
- Install Python dependencies:
  ```bash
  cd backend
  pip install -r requirements.txt
  ```
- Configure settings in `config.py`.
- Start backend services:
  ```bash
  python api_server.py
  ```

### 3. Frontend Setup
- Install Node dependencies:
  ```bash
  cd frontend
  npm install
  ```
- Run the development server:
  ```bash
  npm run dev
  ```

### 4. Scripts
- Use the scripts in `/scripts` to set up MT5 and system services as needed.

## Database

- Uses SQLite (`data/database.sqlite`) for storing signals, trades, and analytics.

## Contributing

Contributions are welcome! Please open issues or pull requests for improvements.

## License

MIT License 

## Contact

For questions, contact the maintainers via GitHub issues.
@ ContractorX
@ Moh dakai.


---
