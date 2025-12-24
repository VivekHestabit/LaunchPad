import Link from 'next/link';
export default function SignupNav() {
  return (
    <div
      className="fixed top-4 left-1/2 -translate-x-1/2 z-50
                   rounded-xl 
                 px-8 py-5 w-[50%] mt-10"
    >
      <div className="flex items-center justify-between">
        {/* LEFT: LOGO */}
        <div className="flex items-center gap-3">
          <img src="/W.svg" alt="Logo" className="w-6 h-6" />
          <span className="font-semibold text-sm tracking-wide ">
            PURITY UI DASHBOARD
          </span>
        </div>

        {/* CENTER: NAV LINKS */}
        <nav className="flex items-center gap-8 text-xs font-semibold text-white">
          <Link
            href="/dashboard"
            className="flex items-center gap-2 hover:text-black transition"
          >
            <img src="/C.svg" alt="" />
            <span>DASHBOARD</span>
          </Link>
          <Link
            href="/dashboard/profile"
            className="flex items-center gap-2 hover:text-black transition"
          >
            <img src="/I.svg" alt="" />
            <span>PROFILE</span>
          </Link>
          <Link
            href="/signup"
            className=" flex items-center gap-2 hover:text-black transition"
          >
            <img src="/T.svg" alt="" />
            <span>SIGN UP</span>
          </Link>
          <Link
            href="/signin"
            className=" flex items-center gap-2 hover:text-black transition"
          >
            <img src="/O.svg" alt="" />
            <span>SIGN IN</span>
          </Link>
        </nav>

        {/* RIGHT: BUTTON */}
        <button
          className="bg-white text-black text-xs font-bold
                     text-sm px-4 py-2 rounded-full"
        >
          Free Download
        </button>
      </div>
    </div>
  );
}
