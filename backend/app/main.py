# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

from app.database import engine, Base
from app.services.ws_manager import manager

# Import all routers
from app.routers import auth, symbols, watchlist, trades, history, ws


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables + start Coinbase listener
    Base.metadata.create_all(bind=engine)
    manager.start_market_data_listener()
    print("[main] Database tables created / verified")
    print("[main] Coinbase WebSocket listener started")
    
    yield
    
    # Shutdown
    manager.stop_market_data_listener()
    print("[main] Shutdown complete")


app = FastAPI(
    title="Trading App API",
    description="Paper trading backend with live Coinbase prices",
    version="1.0.0",
    lifespan=lifespan
)

# Allow local development and the configured production frontend to talk to us.
frontend_origins = [
    origin.strip().rstrip("/")
    for origin in os.getenv("FRONTEND_URL", "").split(",")
    if origin.strip()
]
allowed_origins = list(
    dict.fromkeys(
        [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "https://trade-lab-crypto-paper-trading-plat.vercel.app",
            "https://trade-lab-crypto-paper-trading-platform.vercel.app",
            *frontend_origins,
        ]
    )
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"^https:\/\/.*\.vercel\.app$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(auth.router)
app.include_router(symbols.router)
app.include_router(watchlist.router)
app.include_router(trades.router)
app.include_router(history.router)
app.include_router(ws.router)


@app.get("/")
def root():
    return {"message": "Trading App API is running", "docs": "/docs"}