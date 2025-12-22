export default function Badge({
  variant = "success",
  children
}) {
  const variants = {
    success: "text-green-500",
    danger: "text-red-500",
    info: "text-teal-400",
    neutral: "text-gray-400"
  };

  return (
    <span className={`text-sm font-semibold ${variants[variant]}`}>
      {children}
    </span>
  );
}
