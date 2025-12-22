import Card from "../ui/Card";
import Button from "../ui/Button";
import Badge from "../ui/Badge";
import Input from "../ui/Input";

export default function StatCard() {
  return (
    
    <>
      <Card>
        <p className="text-gray-400 text-sm">Today's Money</p>
        <div className="flex items-center gap-2 justify-between">
          <h2 className="text-xl font-bold text-gray-500">$53,000</h2>
          <Badge variant="success">+55%</Badge>
          <img src="/wallet.svg" alt="" className="ml-25"/>
        </div>
      </Card>

      <Card>
        <p className="text-gray-400 text-sm">New Clients</p>
        <div className="flex items-center gap-2 justify-between ">
          <h2 className="text-xl font-bold text-gray-500">+3,052</h2>
          <Badge variant="success">-14%</Badge>
          <img src="/wallet.svg" alt="" className="ml-25"/>
        </div>
      </Card>

      <Card>
        <p className="text-gray-400 text-sm">New Clients</p>
        <div className="flex items-center gap-2 justify-between">
          <h2 className="text-xl font-bold text-gray-500">+3,052</h2>
          <Badge variant="danger">-14%</Badge>
          <img src="/wallet.svg" alt="" className="ml-25" />
        </div>
      </Card>


      <Card>
        <p className="text-gray-400 text-sm">New Clients</p>
        <div className="flex items-center gap-2 justify-between">
          <h2 className="text-xl font-bold text-gray-500">+3,052</h2>
          <Badge variant="success">-14%</Badge>
          <img src="/wallet.svg" alt="" className="ml-25"/>
        </div>
      </Card>
      </>
  );
}
