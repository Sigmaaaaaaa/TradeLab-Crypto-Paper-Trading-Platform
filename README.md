# TradeLab

TradeLab is a small crypto paper-trading web application built for learning and demonstrating full-stack fintech development. It lets users practice trading supported cryptocurrency pairs with virtual funds, live market prices, watchlists, charts, and portfolio tracking.

> **Important:** TradeLab is a paper-trading simulator. It does not place real orders, connect to a brokerage account, or handle real money.

## Features

- JWT-based user registration and login
- SQLite database with SQLAlchemy
- Virtual starting balance of INR 100,000
- Crypto pair search
- Per-user watchlist with add and remove support
- Live Coinbase Exchange WebSocket prices
- Historical candlestick data through yfinance
- Lightweight Charts candlestick chart
- Simulated buy and sell orders
- Weighted-average position pricing
- Open positions
- Realized and unrealized P&L
- Responsive Next.js dashboard

## Technology stack

### Frontend

- Next.js 14
- React 18
- Tailwind CSS
- Lightweight Charts
- Axios

### Backend

- Python
- FastAPI
- SQLAlchemy
- SQLite
- JWT with `python-jose`
- Passlib with bcrypt
- Coinbase Exchange public WebSocket
- yfinance

## Project structure

```text
trading-app/
├── backend/
│   ├── app/
│   │   ├── models/          # SQLAlchemy database models
│   │   ├── routers/         # REST and WebSocket routes
│   │   ├── schemas/         # Pydantic request/response schemas
│   │   ├── services/        # Authentication, market data, broker logic
│   │   └── utils/           # JWT and validation helpers
│   ├── data/                # SQLite database
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── app/             # Next.js pages
│   │   ├── components/      # UI components
│   │   ├── context/         # Authentication context
│   │   ├── hooks/           # WebSocket and watchlist hooks
│   │   └── lib/             # API client and constants
│   ├── package.json
│   └── tailwind.config.js
└── README.md
```

## Requirements

- Python 3.10 or newer
- Node.js 18 or newer
- npm
- Internet access for Coinbase prices and yfinance data

## Installation

### 1. Clone and enter the project

```bash
git clone <your-repository-url>
cd trading-app
```

### 2. Set up the backend

Create and activate a virtual environment if one does not already exist:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install Python dependencies:

```bash
cd backend
pip install -r requirements.txt
```

Create `backend/.env`:

```env
SECRET_KEY=replace-with-a-long-random-secret
DB_PATH=./data/app.db
```

For local development, the existing SQLite database is created automatically when the backend starts.

### 3. Set up the frontend

Open another terminal:

```bash
cd trading-app/frontend
npm install
```

Create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws/live
```

## Running the application

### Start the backend

```bash
cd trading-app/backend
../venv/bin/python run.py
```

The backend runs at:

```text
http://localhost:8000
```

Interactive API documentation is available at:

```text
http://localhost:8000/docs
```

### Start the frontend

In a second terminal:

```bash
cd trading-app/frontend
npm run dev
```

Open the application at:

```text
http://localhost:3000
```

Use only one frontend development server at a time. If port 3000 is busy, Next.js may use another port; open the exact URL printed in the terminal.

## Supported crypto pairs

The current live data feed supports:

```text
BTCUSDT  ETHUSDT  BNBUSDT  SOLUSDT  XRPUSDT
ADAUSDT  DOGEUSDT AVAXUSDT DOTUSDT  LINKUSDT
MATICUSDT LTCUSDT UNIUSDT ATOMUSDT NEARUSDT
```

## API overview

### Authentication

```text
POST /api/auth/register
POST /api/auth/login
GET  /api/auth/me
```

### Symbols and market data

```text
GET /api/symbols?q=BTC
GET /api/history/{symbol}?interval=1h&limit=200
WS  /ws/live
```

### Watchlist

```text
GET    /api/watchlist
POST   /api/watchlist
DELETE /api/watchlist/{symbol}
```

### Paper trading

```text
GET  /api/trades/portfolio
POST /api/trades/buy
POST /api/trades/sell
```

## Paper-trading behavior

- A new account starts with INR 100,000 in virtual funds.
- A buy order decreases the virtual balance by `quantity × price`.
- Multiple buys use a weighted-average entry price.
- A sell order increases the virtual balance by `quantity × price`.
- Selling calculates realized P&L using the average entry price.
- Open-position unrealized P&L is calculated from the latest live market price.
- - Orders are simulated and are not sent to Coinbase or any exchange.

## Production and security notes

For a deployed frontend, set the backend `FRONTEND_URL` environment variable to
the exact Vercel origin, for example:

```env
FRONTEND_URL=https://trade-lab-crypto-paper-trading-plat.vercel.app
```

Set these frontend variables in Vercel for the Production environment:

```env
NEXT_PUBLIC_API_URL=https://tradelab-crypto-paper-trading-platform.onrender.com
NEXT_PUBLIC_WS_URL=wss://tradelab-crypto-paper-trading-platform.onrender.com/ws/live
```

- Replace the development `SECRET_KEY` before deployment.
- Do not commit `.env` or `.env.local` files containing secrets.
- This project uses SQLite for simplicity and local development.
- Coinbase and yfinance data can be delayed, unavailable, or rate-limited.
- The application is not financial advice and should not be used with real money.

## Build the frontend

```bash
cd frontend
npm run build
```

## Resume description

> Built TradeLab, a full-stack crypto paper-trading platform using Next.js, React, FastAPI, SQLAlchemy, and SQLite. Implemented JWT authentication, per-user watchlists, Coinbase WebSocket live prices, historical candlestick charts, simulated buy/sell orders, portfolio balances, open positions, and realized/unrealized P&L.