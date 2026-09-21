# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import engine, Base
from app.services.ws_manager import manager

# Import all routers
from app.routers import auth, symbols, watchlist, trades, history, ws


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables + start Binance listener
    Base.metadata.create_all(bind=engine)
    manager.start_binance_listener()
    print("[main] Database tables created / verified")
    print("[main] Binance WebSocket listener started")
    
    yield
    
    # Shutdown
    manager.stop_binance_listener()
    print("[main] Shutdown complete")


app = FastAPI(
    title="Trading App API",
    description="Paper trading backend with live Binance prices",
    version="1.0.0",
    lifespan=lifespan
)

# Allow frontend (Next.js) to talk to us
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
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