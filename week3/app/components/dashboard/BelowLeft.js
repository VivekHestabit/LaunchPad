import Content from '../Tables/Content';
import Coloumn from '../Tables/Coloumn';
export default function BelowLeft() {
  const columns = ['COMPANIES', 'MEMBERS', 'BUDGET', 'COMPLETION'];
  const Data = [
    {
      one: 'XD.svg',
      two: 'Chakra Soft UI version',
      third: '1.png',
      fourth: '$14,000',
    },
    {
      one: 'A.svg',
      two: 'Add Progress Track',
      third: '2.png',
      fourth: '$3,000',
    },
    {
      one: 'Slack.svg',
      two: 'Fixed Platform Errors',
      third: '3.png',
      fourth: 'Not Set',
    },
    {
      one: 'spotify.svg',
      two: 'Launch our Mobile App',
      third: '4.png',
      fourth: '$32,000',
    },
    {
      one: 'JIRA.svg',
      two: 'Add the New Pricing Page',
      third: '5.png',
      fourth: '$400',
    },
  ];
  return (
    <div className="h-[519px] w-[1057px] t-[991px] l-[298px] rounded-2xl flex flex-col shadow-lg transition-transform duration-200 hover:-translate-y-2">
      <div className="mt-5 ml-5">
        <h1 className="text-black font-extrabold">Projects</h1>
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
          <Content key={index} d={data} />
        ))}
      </div>
    </div>
  );
}
