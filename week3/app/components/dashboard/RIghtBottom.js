export default function RIghtBottom() {
  return (
    <div className="h-[444px] w-[834px] l-[974px] t-[522px] rounded-xl flex flex-col shadow-lg transition-transform duration-200 hover:-translate-y-2">
      <div className="ml-5 mt-5">
        <h1 className="text-black font-extrabold">Sales Overview</h1>
        <p className="text-gray-500">
          <span className="text-green-500 font-bold">(+5) more</span> in 2021
        </p>
      </div>
      <img
        src="/Graph2.svg"
        alt=""
        className="h-[296.5px] w-[800.5px] l-[995.5px] t-[641.5px] mt-15 ml-5 mt-5"
      />
    </div>
  );
}
