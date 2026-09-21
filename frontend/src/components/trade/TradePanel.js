"use client";

import { useState } from "react";

export default function TradePanel({ symbol, price, onBuy, onSell, submitting, error, message }) {
  const [quantity, setQuantity] = useState("");

  async function submit(side) {
    if (!quantity || Number(quantity) <= 0) return;
    await (side === "BUY" ? onBuy : onSell)(Number(quantity));
    setQuantity("");
  }

  return (
    <section className="rounded-2xl border border-slate-200/80 bg-white p-5 shadow-sm">
      <h2 className="text-lg font-semibold text-slate-900">Paper trade {symbol}</h2>
      <p className="mt-1 text-sm text-slate-500">
        Market price: {price ? price.toLocaleString() : "Waiting for price..."}
      </p>
      <label className="mt-4 block text-sm font-medium text-slate-700">
        Quantity
        <input
          type="number"
          min="0.00000001"
          step="any"
          value={quantity}
          onChange={(event) => setQuantity(event.target.value)}
          className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 outline-none focus:border-blue-500"
          placeholder="Enter quantity"
        />
      </label>
      {error && <p className="mt-3 text-sm text-red-600">{error}</p>}
      {message && <p className="mt-3 text-sm text-green-600">{message}</p>}
      <div className="mt-4 grid grid-cols-2 gap-3">
        <button type="button" disabled={submitting} onClick={() => submit("BUY")} className="rounded-md bg-green-600 px-4 py-2 font-medium text-white hover:bg-green-700 disabled:opacity-50">
          Buy
        </button>
        <button type="button" disabled={submitting} onClick={() => submit("SELL")} className="rounded-md bg-red-600 px-4 py-2 font-medium text-white hover:bg-red-700 disabled:opacity-50">
          Sell
        </button>
      </div>
    </section>
  );
}