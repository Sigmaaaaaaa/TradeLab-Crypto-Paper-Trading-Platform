"use client";

import { useEffect, useRef, useState } from "react";
import { createChart, CandlestickSeries } from "lightweight-charts";

import { getHistory } from "../../lib/api";
import ChartControls from "./ChartControls";

export default function CandleChart({ symbol, price }) {
  const containerRef = useRef(null);
  const seriesRef = useRef(null);
  const lastCandleRef = useRef(null);
  const [interval, setInterval] = useState("1h");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!containerRef.current) return undefined;

    const chart = createChart(containerRef.current, {
      layout: { background: { color: "#ffffff" }, textColor: "#475569" },
      grid: { vertLines: { color: "#e2e8f0" }, horzLines: { color: "#e2e8f0" } },
      rightPriceScale: { borderColor: "#cbd5e1" },
      timeScale: { borderColor: "#cbd5e1" },
      width: containerRef.current.clientWidth,
      height: 420,
    });
    const series = chart.addSeries(CandlestickSeries, {
      upColor: "#16a34a",
      downColor: "#dc2626",
      borderVisible: false,
      wickUpColor: "#16a34a",
      wickDownColor: "#dc2626",
    });
    seriesRef.current = series;

    const resizeObserver = new ResizeObserver(() => {
      chart.applyOptions({ width: containerRef.current.clientWidth });
    });
    resizeObserver.observe(containerRef.current);

    return () => {
      resizeObserver.disconnect();
      chart.remove();
      seriesRef.current = null;
    };
  }, []);

  useEffect(() => {
    let active = true;
    setLoading(true);
    setError("");
    lastCandleRef.current = null;

    getHistory(symbol, interval)
      .then((response) => {
        if (!active || !seriesRef.current) return;
        const candles = response.data || [];
        seriesRef.current.setData(candles);
        lastCandleRef.current = candles[candles.length - 1] || null;
      })
      .catch(() => {
        if (active) setError("Unable to load chart data");
      })
      .finally(() => {
        if (active) setLoading(false);
      });

    return () => {
      active = false;
    };
  }, [symbol, interval]);

  useEffect(() => {
    if (!price || !seriesRef.current || !lastCandleRef.current) return;
    const candle = lastCandleRef.current;
    const updated = {
      time: candle.time,
      open: candle.open,
      high: Math.max(candle.high, price),
      low: Math.min(candle.low, price),
      close: price,
    };
    seriesRef.current.update(updated);
    lastCandleRef.current = updated;
  }, [price]);

  return (
    <section className="rounded-xl bg-white p-4 shadow">
      <div className="mb-3 flex items-center justify-between">
        <div>
          <h2 className="font-semibold text-slate-900">{symbol}</h2>
          <p className="text-sm text-slate-500">
            {price ? `Live price: ${price}` : "Waiting for live price..."}
          </p>
        </div>
        <ChartControls interval={interval} onChange={setInterval} />
      </div>
      {loading && <p className="mb-2 text-sm text-slate-500">Loading candles...</p>}
      {error && <p className="mb-2 text-sm text-red-600">{error}</p>}
      <div ref={containerRef} className="min-h-[420px] w-full" />
    </section>
  );
}