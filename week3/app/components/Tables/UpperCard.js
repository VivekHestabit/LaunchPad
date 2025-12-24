import Coloumn from './Coloumn';
import Content from './Content';
export default function UpperCard() {
  const U = 'Upper';
  const columns = ['AUTHOR', 'FUNCTION', 'STATUS', 'EMPLOYED'];
  const Data = [
    {
      one: 'P1.svg',
      two: 'Esthera Jackson',
      third: 'Manager',
      fourth: 'working',
      fifth: '/Online.svg',
    },
    {
      one: 'P2.svg',
      two: 'Alexa liras',
      third: 'Programmer',
      fourth: 'Canceled',
      fifth: '/offline.svg',
    },
    {
      one: 'P3.svg',
      two: 'Laurent Michael',
      third: 'Executive',
      fourth: 'Done',
      fifth: 'Online.svg',
    },
    {
      one: 'P4.svg',
      two: 'Freduardo Hill',
      third: 'Manager',
      fourth: 'Done',
      fifth: 'Online.svg',
    },
    {
      one: 'P5.svg',
      two: 'Daniel thomas',
      third: 'Programmer',
      fourth: 'working',
      fifth: '/offline.svg',
    },
    {
      one: 'P6.svg',
      two: 'Mark wilson',
      third: 'Designer',
      fourth: 'working',
      fifth: '/offline.svg',
    },
  ];
  return (
    <div
      className="h-[488.5px] w-[1500px] t-[101px] l-[15px]  rounded-xl shadow-lg "
      data-aos="fade-right"
    >
      <div className="mt-5 ml-5 ">
        <h1 className="font-extrabold two-lg two-black text-black">
          Authors Table
        </h1>
      </div>
      <Coloumn coloumns={columns} />
      {Data.map((data, index) => (
        <Content key={index} d={data} Flag={U} />
      ))}
    </div>
  );
}
