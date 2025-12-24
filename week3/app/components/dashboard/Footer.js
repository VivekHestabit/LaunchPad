export default function Footer() {
  return (
    <div className="flex justify-between items-center mt-10 w-full">
      <div>
        <p className="text-[#A0AEC0]">
          @ 2021, Made with ❤️ by{' '}
          <span className="font-extrabold text-green-400">Creative Tim</span> &{' '}
          <span className="font-extrabold text-green-400">Simmmple </span>for a
          better web
        </p>
      </div>

      <div className="text-[#A0AEC0] ">
        <ul className="flex gap-15">
          <li>Creative Tim</li>
          <li>Simmmple</li>
          <li>Blog</li>
          <li>License</li>
        </ul>
      </div>
    </div>
  );
}
