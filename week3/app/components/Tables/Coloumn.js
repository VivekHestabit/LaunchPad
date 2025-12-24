export default function Coloumn({ coloumns }) {
  return (
    <div>
      <div className="grid grid-cols-[2fr_1fr_1fr_1fr_1fr] gap-x-10 text-xs text-gray-400 font-semibold pb-3 border-b border-[#E2E8F0] ml-5 mt-3">
        {coloumns?.map((col, index) => (
          <span key={index}>{col}</span>
        ))}
      </div>
    </div>
  );
}
