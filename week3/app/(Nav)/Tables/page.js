import UpperCard from '@/app/components/Tables/UpperCard';
import LowerCard from '@/app/components/Tables/LowerCard';
import Footer from '@/app/components/dashboard/Footer';

export default function page() {
  return (
    <>
      <div className="h-[966px] w-[1500px] t-[101px] l-[298px] ">
        <UpperCard />
        <LowerCard />
      </div>
      <Footer />
    </>
  );
}
