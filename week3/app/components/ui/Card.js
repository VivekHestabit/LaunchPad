export default function Card({ children, className = '' }) {
  return (
    <div
      className={`bg-white rounded-xl shadow-lg p-6 ${className} transition-transform transition-200 hover:-translate-y-2`}
    >
      {children}
    </div>
  );
}
