// frontend/src/lib/api.js

import axios from "axios";
import Cookies from "js-cookie";
import { API_URL } from "./constants";

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Attach JWT token to every request (if available)
api.interceptors.request.use((config) => {
  const token = Cookies.get("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ========== Auth ==========
export const register = (email, password) =>
  api.post("/api/auth/register", { email, password });

export const login = (email, password) =>
  api.post("/api/auth/login", { email, password });

export const getMe = () => api.get("/api/auth/me");

// ========== Symbols ==========
export const searchSymbols = (q) =>
  api.get("/api/symbols", { params: { q } });

// ========== Watchlist ==========
export const getWatchlist = () => api.get("/api/watchlist");

export const addToWatchlist = (symbol) =>
  api.post("/api/watchlist", { symbol });

export const removeFromWatchlist = (symbol) =>
  api.delete(`/api/watchlist/${symbol}`);

// ========== History (candles) ==========
export const getHistory = (symbol, interval = "1h", limit = 200) =>
  api.get(`/api/history/${symbol}`, { params: { interval, limit } });

// ========== Trades ==========
export const buy = (symbol, quantity) =>
  api.post("/api/trades/buy", { symbol, quantity });

export const sell = (symbol, quantity) =>
  api.post("/api/trades/sell", { symbol, quantity });

export const getPortfolio = () => api.get("/api/trades/portfolio");

export default api;