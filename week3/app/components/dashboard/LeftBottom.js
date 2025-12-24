import Image from 'next/image';
import BottomCard from './BottomCard';
export default function LeftBottom() {
  return (
    <div className="h-[444px] w-[652px] l-[298px] t-[522px]  rounded-xl flex flex-col justify-start  text-black shadow-lg p-4 transition-transform duration-200 hover:-translate-y-2">
      <Image src="/Graph.png" height={222} width={620} alt="Graph img" />
      <div className="mt-4  w-[160px] h-[50.5px] l-[319px] t-[784px] flex flex-col">
        <p className="font-extrabold">Acitve Users</p>
        <p className="text-green-500 font-extrabold">
          (+23) <span className="text-gray-400">then last week</span>
        </p>
      </div>
      <div className="mt-10 h-[80.5] w-[569] l-[319.5px] t-[871px] flex items-center justify-start gap-15 ">
        <BottomCard name="Users" img="/Folder.svg" value="32,984" />
        <BottomCard name="Clicks" img="/JET.svg" value="2,42m" />
        <BottomCard name="Sales" img="/Cart.svg" value="2,400$" />
        <BottomCard name="Items" img="/TOOL.svg" value="320" />
      </div>
    </div>
  );
}
