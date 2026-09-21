export default function BalanceDisplay({ balance, realizedPnl, unrealizedPnl }) {
  const format = (value) =>
    value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });

  return (
    <section className="grid gap-4 rounded-2xl border border-slate-200/80 bg-white p-5 shadow-sm sm:grid-cols-3">
      <div>
        <p className="text-sm text-slate-500">Available balance</p>
        <p className="mt-1 text-xl font-semibold text-slate-900">{format(balance)}</p>
      </div>
      <div>
        <p className="text-sm text-slate-500">Realized P&amp;L</p>
        <p className={`mt-1 text-xl font-semibold ${realizedPnl >= 0 ? "text-green-600" : "text-red-600"}`}>
          {format(realizedPnl)}
        </p>
      </div>
      <div>
        <p className="text-sm text-slate-500">Unrealized P&amp;L</p>
        <p className={`mt-1 text-xl font-semibold ${unrealizedPnl >= 0 ? "text-green-600" : "text-red-600"}`}>
          {format(unrealizedPnl)}
        </p>
      </div>
    </section>
  );
}