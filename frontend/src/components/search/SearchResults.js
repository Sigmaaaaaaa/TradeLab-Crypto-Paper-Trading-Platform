export default function SearchResults({ results, loading, error, onSelect }) {
  if (loading) {
    return <div className="p-3 text-sm text-slate-500">Searching...</div>;
  }

  if (error) {
    return <div className="p-3 text-sm text-red-600">{error}</div>;
  }

  if (!results.length) {
    return <div className="p-3 text-sm text-slate-500">No matching pairs</div>;
  }

  return (
    <ul className="max-h-60 overflow-y-auto py-1">
      {results.map((symbol) => (
        <li key={symbol}>
          <button
            type="button"
            onClick={() => onSelect(symbol)}
            className="w-full px-3 py-2 text-left text-sm font-medium text-slate-700 hover:bg-blue-50 hover:text-blue-700"
          >
            {symbol}
          </button>
        </li>
      ))}
    </ul>
  );
}