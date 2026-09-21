"use client";

import WatchlistItem from "./WatchlistItem";

export default function WatchlistPanel({
  open,
  onToggle,
  items,
  prices,
  loading,
  error,
  selectedSymbol,
  onSelect,
  onRemove,
}) {
  return (
    <aside className={`fixed inset-y-0 left-0 z-20 w-72 transform bg-white p-4 shadow-xl transition-transform ${
      open ? "translate-x-0" : "-translate-x-full"
    }`}>
      <div className="flex items-center justify-between border-b border-slate-200 pb-4">
        <h2 className="text-lg font-semibold text-slate-900">Watchlist</h2>
        <button type="button" onClick={onToggle} className="text-2xl text-slate-500 hover:text-slate-900" aria-label="Close watchlist">
          ×
        </button>
      </div>
      {loading && <p className="py-4 text-sm text-slate-500">Loading...</p>}
      {error && <p className="py-4 text-sm text-red-600">{error}</p>}
      {!loading && !items.length && <p className="py-4 text-sm text-slate-500">No saved pairs yet.</p>}
      <ul className="space-y-1 pt-3">
        {items.map((item) => (
          <WatchlistItem
            key={item.id}
            item={item}
            price={prices[item.symbol]}
            selected={selectedSymbol === item.symbol}
            onSelect={onSelect}
            onRemove={onRemove}
          />
        ))}
      </ul>
    </aside>
  );
}