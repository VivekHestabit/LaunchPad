import Card from '../ui/Card';
export default function LeftMIddleCard() {
  return (
    <Card className="h-[290.5px] w-230.5 flex items-center justify-between transition-transform duration-200 hover:-translate-y-2">
      <div className="flex">
        <div className="max-w-sm">
          <p className="text-sm text-[#A0AEC0]">Built by developers</p>

          <h2 className="text-xl font-semibold mt-1 text-[#2D3748]">
            Purity UI Dashboard
          </h2>

          <p className="text-sm text-[#A0AEC0] mt-2">
            From colors, cards, typography to complex elements, you will find
            the full documentation.
          </p>

          <button className="text-black font-medium mt-30 cursor-pointer">
            Read more →
          </button>
        </div>

        <img
          src="/Chakra.svg"
          alt=""
          height="255.5px"
          width="360px"
          className="ml-55"
        />
      </div>
    </Card>
  );
}
