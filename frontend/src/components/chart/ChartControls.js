import { INTERVALS } from "../../lib/constants";

export default function ChartControls({ interval, onChange }) {
  return (
    <div className="flex gap-1">
      {INTERVALS.map((option) => (
        <button
          key={option.value}
          type="button"
          onClick={() => onChange(option.value)}
          className={`rounded px-2 py-1 text-xs font-medium ${
            interval === option.value
              ? "bg-blue-600 text-white"
              : "text-slate-500 hover:bg-slate-100"
          }`}
        >
          {option.label}
        </button>
      ))}
    </div>
  );
}