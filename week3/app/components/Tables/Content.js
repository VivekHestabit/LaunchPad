export default function Content({ d, Flag }) {
  return (
    <div className=" grid grid-cols-[2fr_1fr_1fr_1fr_1fr] gap-x-10 text-[#2D3748] ml-5 mt-3 border-b border-[#E2E8F0] pb-3 font-bold">
      <div className="flex gap-5 items-center ">
        <img
          src={d.one}
          alt=""
          className="h-[40px] w-[40px] t-[216px] -[320.5px]"
        />
        <p>{d.two}</p>
      </div>
      <span>
        {d.third.includes('png') ? (
          <>
            <img src={`/${d.third}`} alt="" />
          </>
        ) : (
          <>{d.third}</>
        )}
      </span>
      <span>
        {Flag == 'Upper' ? (
          <>
            <img src={d.fifth} alt="" />
          </>
        ) : (
          <>{d.fourth}</>
        )}
      </span>
      <div>
        {Flag == 'Upper' ? (
          <>
            <p>14/06/21</p>
          </>
        ) : (
          <>
            <span className="text-green-400 font-bold">60%</span>
            <img src="Progress.png" alt="" />
          </>
        )}
      </div>

      <div>
        {Flag == 'Upper' ? (
          <>
            <p>Edit</p>
          </>
        ) : (
          <>
            <p>:</p>
          </>
        )}
      </div>
    </div>
  );
}
