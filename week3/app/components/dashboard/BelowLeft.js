export default function BelowLeft() {
  return (
    <div className="h-[519px] w-[1057px] t-[991px] l-[298px] rounded-2xl flex flex-col shadow-lg transition-transform duration-200 hover:-translate-y-2">
      <div className="mt-5 ml-5">
        <h1 className="text-black font-extrabold">Projects</h1>
        <p className="flex gap-2">
          <img src="/circle.svg" alt="" />{' '}
          <span className="text-md font-bold text-gray-600">
            30 done <span className="text-gray-500 font-light">this month</span>
          </span>
        </p>
      </div>
      <img
        src="/List.png"
        alt=""
        className="h-[380.5px] w-[1012px] l-[320.5px] t-[1098px] ml-5 mt-8"
      />
    </div>
  );
}
