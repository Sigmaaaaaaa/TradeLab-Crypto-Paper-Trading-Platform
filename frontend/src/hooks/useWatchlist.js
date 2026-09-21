"use client";

import { useCallback, useEffect, useState } from "react";

import {
  addToWatchlist,
  getWatchlist,
  removeFromWatchlist,
} from "../lib/api";

export default function useWatchlist(enabled = true) {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(enabled);
  const [error, setError] = useState("");

  const refresh = useCallback(async () => {
    if (!enabled) return;
    setLoading(true);
    try {
      const response = await getWatchlist();
      setItems(response.data.items || []);
      setError("");
    } catch (requestError) {
      setError(requestError?.response?.data?.detail || "Unable to load watchlist");
    } finally {
      setLoading(false);
    }
  }, [enabled]);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const add = useCallback(async (symbol) => {
    try {
      const response = await addToWatchlist(symbol);
      setItems((current) => [...current, response.data]);
      setError("");
    } catch (requestError) {
      setError(requestError?.response?.data?.detail || "Unable to add pair");
      throw requestError;
    }
  }, []);

  const remove = useCallback(async (symbol) => {
    try {
      await removeFromWatchlist(symbol);
      setItems((current) => current.filter((item) => item.symbol !== symbol));
      setError("");
    } catch (requestError) {
      setError(requestError?.response?.data?.detail || "Unable to remove pair");
      throw requestError;
    }
  }, []);

  return { items, loading, error, refresh, add, remove };
}