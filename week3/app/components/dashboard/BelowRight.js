export default function BelowRight() {
  return (
    <div className="border-2  rounded-xl shadow-xl h-[519px] t-[991px] l-[298px] transition-transform duration-200 hover:-translate-y-2 ">
      <div className="mt-8 ml-5">
        <h1 className="text-black font-extrabold">Order Overview</h1>
        <p className="flex gap-2">
          {' '}
          <span className="text-md font-bold text-green-500">
            +30% <span className="text-gray-500 font-light">this month</span>
          </span>
        </p>
      </div>
      <img src="/BelowList.svg" alt="" className="mt-10 ml-5" />
    </div>
  );
}
