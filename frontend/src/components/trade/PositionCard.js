export default function PositionCard({ position, price }) {
  const marketPrice = price || position.average_price;
  const unrealizedPnl = (marketPrice - position.average_price) * position.quantity;

  return (
    <li className="rounded-lg border border-slate-200 p-4">
      <div className="flex items-center justify-between">
        <span className="font-semibold text-slate-900">{position.symbol}</span>
        <span className="text-sm text-slate-500">{position.quantity} units</span>
      </div>
      <div className="mt-2 grid grid-cols-3 gap-2 text-sm">
        <div>
          <p className="text-slate-500">Avg. entry</p>
          <p className="font-medium text-slate-800">{position.average_price.toFixed(2)}</p>
        </div>
        <div>
          <p className="text-slate-500">Market</p>
          <p className="font-medium text-slate-800">{marketPrice.toFixed(2)}</p>
        </div>
        <div>
          <p className="text-slate-500">P&amp;L</p>
          <p className={`font-medium ${unrealizedPnl >= 0 ? "text-green-600" : "text-red-600"}`}>
            {unrealizedPnl.toFixed(2)}
          </p>
        </div>
      </div>
    </li>
  );
}