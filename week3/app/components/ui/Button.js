export default function Button({
  variant = 'primary',
  size = 'md',
  disabled = false,
  children,
}) {
  const base = 'rounded-lg font-semibold transition focus:outline-none';

  const variants = {
    primary: 'bg-teal-400 text-white hover:bg-teal-500',
    outline: 'border border-gray-300 text-gray-600 hover:bg-gray-100',
    white: 'bg-white text-teal-500',
  };

  const sizes = {
    sm: 'px-3 py-1 text-sm',
    md: 'px-4 py-2 text-sm',
    lg: 'px-6 py-3 text-base',
  };

  return (
    <button
      disabled={disabled}
      className={`
        ${base}
        ${variants[variant]}
        ${sizes[size]}
        ${disabled ? 'opacity-50 cursor-not-allowed' : ''}
      `}
    >
      {children}
    </button>
  );
}
