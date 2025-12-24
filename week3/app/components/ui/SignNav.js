import Link from 'next/link';
export default function SignNav() {
  return (
    <div
      className="fixed top-4 left-1/2 -translate-x-1/2 z-50
                 bg-white shadow-md rounded-xl
                 px-8 py-5 w-[50%] opacity-90"
    >
      <div className="flex items-center justify-between">
        {/* LEFT: LOGO */}
        <div className="flex items-center gap-3">
          <img src="/icon.svg" alt="Logo" className="w-6 h-6" />
          <span className="font-semibold text-sm tracking-wide text-gray-800">
            PURITY UI DASHBOARD
          </span>
        </div>

        {/* CENTER: NAV LINKS */}
        <nav className="flex items-center gap-8 text-xs font-semibold text-gray-700">
          <Link
            href="/dashboard"
            className="flex items-center gap-2 hover:text-black transition"
          >
            <img src="/cube.svg" alt="" />
            <span>Dashboard</span>
          </Link>
          <Link
            href="/dashboard/profile"
            className="flex items-center gap-2 hover:text-black transition"
          >
            <img src="/Man.svg" alt="" />
            <span>Profile</span>
          </Link>
          <Link
            href="/signup"
            className=" flex items-center gap-2 hover:text-black transition"
          >
            <img src="/pic.svg" alt="" />
            <span>Sign Up</span>
          </Link>
          <Link
            href="/signin"
            className=" flex items-center gap-2 hover:text-black transition"
          >
            <img src="/Key.svg" alt="" />
            <span>Sign In</span>
          </Link>
        </nav>

        {/* RIGHT: BUTTON */}
        <button
          className="bg-gray-900 text-white
                     text-xs px-4 py-2 rounded-full"
        >
          Free Download
        </button>
      </div>
    </div>
  );
}
