import InnerCard from '@/app/components/dashboard/Profile/InnerCard.js';
import Footer from '@/app/components/dashboard/Footer';
import ProfileCard from '@/app/components/dashboard/Profile/ProfileCard';

export default function Page() {
  return (
    <div>
      <div className="border-2 border-pink-500 h-[377.5px] w-[1510px] l-[298px] t-[397px] rounded-xl shadow-xl flex gap-5">
        <ProfileCard />
        <ProfileCard />
        <ProfileCard />
      </div>
      <div className=" h-[540px] w-[1520px] l-[298px] t-[798.5px] mt-5 rounded-xl shadow-xl ">
        <div className="flex flex-col mt-8 ml-5">
          <h1 className="font-extrabold text-black text-2xl">Projects</h1>
          <p className="text-gray-500 mt-3">Architects design houses</p>
        </div>
        <div className="flex  mt-5">
          <InnerCard
            name={'Modern'}
            Project={'Project #1'}
            img={'/Inner.png'}
          />
          <InnerCard
            name={'Scandinavian'}
            Project={'Project #2'}
            img={'/plant.png'}
          />
          <InnerCard
            name={'Minimalist'}
            Project={'Project #3'}
            img={'/back.png'}
          />
          <div className="text-black h-[390px] w-[365px] t-[902.5px] l-[319px] ml-3 mr-3 mt-5 border-2 border-[#E0E1E2] rounded-3xl flex flex-col justify-center transition-transform transition-200 hover:-translate-y-2">
            <div className="flex flex-col items-center">
              <img
                src="/outline.svg"
                alt=""
                className="h-[30px] w-[30px] l-[1674px] t-[1043px] font-extrabold"
              />
              <h1 className="font-extrabold text-2xl text-[#718096]">
                Create a New Project
              </h1>
            </div>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
}
