import Coloumn from './Coloumn';
import Content from './Content';
export default function LowerCard() {
  const columns = ['COMPANIES', 'BUDGET', 'STATUS', 'COMPLETION'];
  const Lower = 'lower';
  const Data = [
    {
      one: 'XD.svg',
      two: 'Chakra Soft UI version',
      third: '$14,000',
      fourth: 'working',
    },
    {
      one: 'A.svg',
      two: 'Add Progress Track',
      third: '$3,000',
      fourth: 'Canceled',
    },
    {
      one: 'Slack.svg',
      two: 'Fixed Platform Errors',
      third: 'Not Set',
      fourth: 'Done',
    },
    {
      one: 'spotify.svg',
      two: 'Launch our Mobile App',
      third: '$32,000',
      fourth: 'Done',
    },
    {
      one: 'JIRA.svg',
      two: 'Add the New Pricing Page',
      third: '$400',
      fourth: 'working',
    },
  ];
  return (
    <div
      className="h-[435.5px] w-[1500px] t-[101px] l-[15px]  mt-5 rounded-xl shadow-xl "
      data-aos="fade-right"
    >
      <div className="mt-5 ml-5 ">
        <h1 className="two-black font-extrabold text-black">Projects</h1>
        <p className="flex gap-2">
          <img src="/circle.svg" alt="" />{' '}
          <span className="text-md font-bold text-gray-600">
            30 done <span className="text-gray-500 font-light">this month</span>
          </span>
        </p>
      </div>
      <div className="mt-10">
        <Coloumn coloumns={columns} />
        {Data.map((data, index) => (
          <Content key={index} d={data} Flag={Lower} />
        ))}
      </div>
    </div>
  );
}
