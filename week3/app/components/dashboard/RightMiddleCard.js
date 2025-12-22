import Card from "../ui/Card";

export default function RightMiddleCard() {
  return (
    <Card className="h-[290.5px] w-137.5 p-0 overflow-hidden">
      <div
        className="relative h-full p-6 bg-cover bg-center rounded-xl"
        style={{
          backgroundImage: "url('/SecCard.jpg')"
        }}
      >
        <div className="absolute top-6 left-6 text-left">
          <h2 className="text-white text-xl font-semibold">
            Work with the Rockets
          </h2>

          <p className="text-white/80 text-sm mt-2">
            Wealth creation is an evolutionarily recent positive-sum game.
          </p>
        </div>

        <button className="absolute bottom-6 left-6 text-white text-sm font-medium mt-4 cursor-pointer">
          Read more →
        </button>
      </div>
    </Card>
  );
}
