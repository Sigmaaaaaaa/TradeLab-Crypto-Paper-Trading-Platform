export default function WatchlistItem({ item, price, selected, onSelect, onRemove }) {
  return (
    <li className={`flex items-center justify-between gap-3 rounded-lg p-3 ${
      selected ? "bg-blue-50" : "hover:bg-slate-50"
    }`}>
      <button type="button" onClick={() => onSelect(item.symbol)} className="min-w-0 flex-1 text-left">
        <span className="block font-medium text-slate-800">{item.symbol}</span>
        <span className="block text-xs text-slate-500">
          {price ? price.toLocaleString(undefined, { maximumFractionDigits: 8 }) : "No price"}
        </span>
      </button>
      <button
        type="button"
        onClick={() => onRemove(item.symbol)}
        aria-label={`Remove ${item.symbol}`}
        className="text-lg leading-none text-slate-400 hover:text-red-600"
      >
        ×
      </button>
    </li>
  );
}