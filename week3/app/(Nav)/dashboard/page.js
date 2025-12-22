import Card from '@/app/components/ui/Badge';
import Button from '@/app/components/ui/Badge';
import Badge from '@/app/components/ui/Badge';
import Input from '@/app/components/ui/Badge';
import StatCard from '@/app/components/dashboard/StatCard';
import LeftMiddleCard from '@/app/components/dashboard/LeftMiddleCard';
import RightMiddleCard from '@/app/components/dashboard/RightMiddleCard';
import LeftBottom from '@/app/components/dashboard/LeftBottom';
import RIghtBottom from '@/app/components/dashboard/RIghtBottom';
import BelowLeft from '@/app/components/dashboard/BelowLeft';
import BelowRight from '@/app/components/dashboard/BelowRight';

export default function Dashboard() {
  return (
    <>
      <div className="grid grid-cols-4 gap-6">
        <StatCard />
      </div>
      <div className="grid grid-cols-[auto_1fr] gap-6 mt-6 ">
        <LeftMiddleCard />
        <RightMiddleCard />
      </div>
      <div
        style={{
          height: '445px',
          width: '1510px',
          top: '522px',
          left: '298px',
        }}
        className="grid grid-cols-[auto_1fr] mt-13 gap-5 "
      >
        <LeftBottom />
        <RIghtBottom />
      </div>
      <div className="grid grid-cols-[auto_1fr]  mt-6 gap-5">
        <BelowLeft />
        <BelowRight />
      </div>
    </>
  );
}
