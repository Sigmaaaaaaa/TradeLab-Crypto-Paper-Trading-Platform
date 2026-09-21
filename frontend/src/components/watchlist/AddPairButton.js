export default function AddPairButton({ symbol, isSaved, onAdd }) {
  return (
    <button
      type="button"
      disabled={isSaved}
      onClick={() => onAdd(symbol)}
      className="rounded-md bg-blue-600 px-3 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-slate-300"
    >
      {isSaved ? "In watchlist" : "Add to watchlist"}
    </button>
  );
}