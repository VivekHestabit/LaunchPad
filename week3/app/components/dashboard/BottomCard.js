export default function BottomCard({ name, img, value }) {
  return (
    <>
      <div>
        <div className="h-[35.5] w-[101] l-[319.5px t-[871px] flex gap-2  items-center">
          <img src={img} alt="" className="h-[35] w-[35]" />
          <p className="text-sm text-gray-400 font-bold">{name}</p>
        </div>
        <div>
          <h1 className="font-extrabold">{value}</h1>
          <img src="/Progress.png" alt="" />
        </div>
      </div>
    </>
  );
}
