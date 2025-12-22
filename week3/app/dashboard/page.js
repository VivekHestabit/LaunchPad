import Card from "../components/ui/Card";
import Button from "../components/ui/Button";
import Badge from "../components/ui/Badge";
import Input from "../components/ui/Input";
import StatCard from "../components/dashboard/StatCard";
import LeftMiddleCard from "../components/dashboard/LeftMiddleCard";
import RightMiddleCard from "../components/dashboard/RightMiddleCard";

export default function Dashboard() {
  return (
    <>
    <div className="grid grid-cols-4 gap-6">
      <StatCard />
    </div>
     <div className="grid grid-cols-[auto_1fr] gap-6 mt-6 ">
        <LeftMiddleCard />
        <RightMiddleCard/>
      </div>
      </>
  );
}
