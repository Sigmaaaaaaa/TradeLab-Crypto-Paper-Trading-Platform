"use client";

import { useEffect, useRef, useState } from "react";

import { searchSymbols } from "../../lib/api";
import SearchResults from "./SearchResults";

export default function SearchBar({ value, onSelect }) {
  const [query, setQuery] = useState(value || "");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [open, setOpen] = useState(false);
  const containerRef = useRef(null);

  useEffect(() => {
    setQuery(value || "");
  }, [value]);

  useEffect(() => {
    function closeOnOutsideClick(event) {
      if (!containerRef.current?.contains(event.target)) setOpen(false);
    }
    document.addEventListener("mousedown", closeOnOutsideClick);
    return () => document.removeEventListener("mousedown", closeOnOutsideClick);
  }, []);

  useEffect(() => {
    let active = true;
    const timer = setTimeout(async () => {
      setLoading(true);
      setError("");
      try {
        const response = await searchSymbols(query.trim());
        if (active) setResults(response.data);
      } catch {
        if (active) {
          setResults([]);
          setError("Unable to search symbols");
        }
      } finally {
        if (active) setLoading(false);
      }
    }, 250);

    return () => {
      active = false;
      clearTimeout(timer);
    };
  }, [query]);

  function selectSymbol(symbol) {
    setQuery(symbol);
    setOpen(false);
    onSelect(symbol);
  }

  return (
    <div ref={containerRef} className="relative w-full max-w-md">
      <label htmlFor="symbol-search" className="sr-only">
        Search trading pairs
      </label>
      <input
        id="symbol-search"
        type="search"
        value={query}
        placeholder="Search pairs, e.g. BTCUSDT"
        onFocus={() => setOpen(true)}
        onChange={(event) => {
          setQuery(event.target.value.toUpperCase());
          setOpen(true);
        }}
        className="w-full rounded-lg border border-slate-300 bg-white px-4 py-3 text-sm outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
      />
      {open && (
        <div className="absolute z-10 mt-2 w-full overflow-hidden rounded-lg border border-slate-200 bg-white shadow-lg">
          <SearchResults
            results={results}
            loading={loading}
            error={error}
            onSelect={selectSymbol}
          />
        </div>
      )}
    </div>
  );
}