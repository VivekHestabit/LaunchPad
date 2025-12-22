export default function Input({
  placeholder,
  error,
  icon
}) {
  return (
    <div className="w-full">
      <div className="relative">
        {icon && (
          <span className="absolute left-3 top-1/2 -translate-y-1/2">
            {icon}
          </span>
        )}
        <input
          placeholder={placeholder}
          className={`
            w-full bg-white py-2 rounded-lg shadow-sm
            focus:outline-none focus:ring-2
            ${icon ? "pl-10" : "pl-4"}
            ${error
              ? "border border-red-400 focus:ring-red-300"
              : "focus:ring-teal-300"
            }
          `}
        />
      </div>
      {error && (
        <p className="text-red-500 text-sm mt-1">{error}</p>
      )}
    </div>
  );
}
