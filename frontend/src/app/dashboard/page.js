"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { useAuth } from "../../context/AuthContext";
import SearchBar from "../../components/search/SearchBar";
import CandleChart from "../../components/chart/CandleChart";
import useWebSocket from "../../hooks/useWebSocket";
import useWatchlist from "../../hooks/useWatchlist";
import WatchlistPanel from "../../components/watchlist/WatchlistPanel";
import AddPairButton from "../../components/watchlist/AddPairButton";
import { buy, getPortfolio, sell } from "../../lib/api";
import BalanceDisplay from "../../components/trade/BalanceDisplay";
import PositionCard from "../../components/trade/PositionCard";
import TradePanel from "../../components/trade/TradePanel";

export default function DashboardPage() {
  const router = useRouter();
  const { user, isAuthenticated, loading, logout } = useAuth();
  const [selectedSymbol, setSelectedSymbol] = useState("BTCUSDT");
  const { prices, connected } = useWebSocket();
  const [watchlistOpen, setWatchlistOpen] = useState(false);
  const { items, loading: watchlistLoading, error: watchlistError, add, remove } =
    useWatchlist(isAuthenticated);
  const [portfolio, setPortfolio] = useState({ balance: 0, positions: [], recent_orders: [] });
  const [tradeError, setTradeError] = useState("");
  const [tradeMessage, setTradeMessage] = useState("");
  const [tradeSubmitting, setTradeSubmitting] = useState(false);

  useEffect(() => {
    if (!loading && !isAuthenticated) router.replace("/login");
  }, [loading, isAuthenticated, router]);

  useEffect(() => {
    if (!isAuthenticated) return;
    getPortfolio()
      .then((response) => setPortfolio(response.data))
      .catch(() => setTradeError("Unable to load portfolio"));
  }, [isAuthenticated]);

  if (loading || !isAuthenticated) return null;
  const isSaved = items.some((item) => item.symbol === selectedSymbol);
  const realizedPnl = portfolio.recent_orders.reduce((total, order) => total + (order.pnl || 0), 0);
  const unrealizedPnl = portfolio.positions.reduce((total, position) => {
    const currentPrice = prices[position.symbol] || position.average_price;
    return total + (currentPrice - position.average_price) * position.quantity;
  }, 0);

  async function placeTrade(action) {
    setTradeSubmitting(true);
    setTradeError("");
    setTradeMessage("");
    try {
      const response = await action(selectedSymbol);
      setTradeMessage(`${response.data.side} order placed for ${response.data.quantity} ${response.data.symbol}`);
      const portfolioResponse = await getPortfolio();
      setPortfolio(portfolioResponse.data);
    } catch (error) {
      setTradeError(error?.response?.data?.detail || "Trade could not be completed");
    } finally {
      setTradeSubmitting(false);
    }
  }

  return (
    <main className="min-h-screen bg-[#f5f7fb] p-4 text-slate-900 sm:p-6">
      <WatchlistPanel
        open={watchlistOpen}
        onToggle={() => setWatchlistOpen(false)}
        items={items}
        prices={prices}
        loading={watchlistLoading}
        error={watchlistError}
        selectedSymbol={selectedSymbol}
        onSelect={setSelectedSymbol}
        onRemove={remove}
      />
      <div className="mx-auto max-w-[1440px]">
        <header className="mb-6 rounded-2xl border border-slate-200/80 bg-white/90 p-4 shadow-sm backdrop-blur sm:p-5">
          <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
            <div className="flex items-center gap-3">
              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-slate-950 text-lg font-bold text-white shadow-lg shadow-slate-300">
                ₿
              </div>
              <div>
                <h1 className="text-xl font-bold tracking-tight text-slate-950 sm:text-2xl">TradeLab</h1>
                <p className="text-xs text-slate-500">Paper trading terminal · {user.email}</p>
              </div>
            </div>
            <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
              <SearchBar value={selectedSymbol} onSelect={setSelectedSymbol} />
              <div className="flex gap-2">
                <button type="button" onClick={() => setWatchlistOpen(true)} className="rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm font-semibold text-slate-700 shadow-sm hover:border-blue-300 hover:text-blue-700">
                  Watchlist
                </button>
                <button type="button" onClick={logout} className="rounded-lg bg-slate-950 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-slate-800">
                  Log out
                </button>
              </div>
            </div>
          </div>
        </header>
        <div className="mb-3 flex items-center justify-between">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">Market overview</p>
            <p className="mt-1 text-sm text-slate-500">Monitor prices and practice risk-free.</p>
          </div>
          <p className={`rounded-full px-3 py-1 text-xs font-semibold ${connected ? "bg-emerald-50 text-emerald-700" : "bg-amber-50 text-amber-700"}`}>
            <span className="mr-1">●</span>{connected ? "Live feed connected" : "Connecting to feed"}
          </p>
        </div>
        <div>
          <CandleChart symbol={selectedSymbol} price={prices[selectedSymbol]} />
          <div className="mt-4 flex flex-col gap-4 rounded-2xl border border-slate-200/80 bg-white p-4 shadow-sm sm:flex-row sm:items-center sm:justify-between">
            <div className="flex items-center gap-3">
              <div className="h-2.5 w-2.5 rounded-full bg-blue-500 shadow-[0_0_0_4px_#dbeafe]" />
              <div>
              <p className="text-sm text-slate-500">Selected pair</p>
                <p className="font-bold text-slate-950">{selectedSymbol}</p>
              </div>
            </div>
            <AddPairButton symbol={selectedSymbol} isSaved={isSaved} onAdd={add} />
          </div>
          <div className="mt-4">
            <BalanceDisplay balance={portfolio.balance} realizedPnl={realizedPnl} unrealizedPnl={unrealizedPnl} />
          </div>
          <div className="mt-4 grid gap-4 lg:grid-cols-[minmax(0,1fr)_360px]">
              <section className="rounded-2xl border border-slate-200/80 bg-white p-5 shadow-sm">
                <h2 className="text-lg font-semibold text-slate-900">Open positions</h2>
                {!portfolio.positions.length && <p className="mt-3 text-sm text-slate-500">No open positions.</p>}
                <ul className="mt-3 space-y-3">
                  {portfolio.positions.map((position) => (
                    <PositionCard key={position.id} position={position} price={prices[position.symbol]} />
                  ))}
                </ul>
              </section>
              <TradePanel
                symbol={selectedSymbol}
                price={prices[selectedSymbol]}
                submitting={tradeSubmitting}
                error={tradeError}
                message={tradeMessage}
                onBuy={(quantity) => placeTrade((symbol) => buy(symbol, quantity))}
                onSell={(quantity) => placeTrade((symbol) => sell(symbol, quantity))}
              />
          </div>
        </div>
      </div>
    </main>
  );
}