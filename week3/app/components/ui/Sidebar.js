'use client';

import Link from "next/link";
import { usePathname } from "next/navigation";
import { HelpCircle } from "lucide-react";

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 h-screen flex flex-col p-4">
      
      {/* TOP */}
      <div>
        {/* Logo */}
        <div className="flex items-center gap-2 mb-10 font-bold text-[#2D3748]">
          <img src="/icon.svg" alt="logo" />
          <span className="text-sm font-semibold">
            PURITY UI DASHBOARD
          </span>
        </div>

        {/* MAIN MENU */}
        <MenuItem
          href="/dashboard"
          icon={<img src="/Home.svg" width="15" height="15" />}
          text="Dashboard"
          active={pathname === "/dashboard"}
        />

        <MenuItem
          href="/tables"
          icon={<img src="/chart.svg" width="15" height="15" />}
          text="Tables"
          active={pathname === "/tables"}
        />

        <MenuItem
          href="/billing"
          icon={<img src="/default.svg" width="15" height="15" />}
          text="Billing"
          active={pathname === "/billing"}
        />

        <MenuItem
          href="/rtl"
          icon={<img src="/default1.png" width="15" height="15" />}
          text="RTL"
          active={pathname === "/rtl"}
        />

        {/* ACCOUNT PAGES */}
        <p className="text-xs text-[#2D3748] font-semibold mt-8 mb-2">
          ACCOUNT PAGES
        </p>

        <MenuItem
          href="/profile"
          icon={<img src="/Person.svg" width="15" height="15" />}
          text="Profile"
          active={pathname === "/profile"}
        />

        <MenuItem
          href="/signin"
          icon={<img src="/Page.svg" width="15" height="15" />}
          text="Sign In"
          active={pathname === "/signin"}
        />

        <MenuItem
          href="/signup"
          icon={<img src="/sharp.svg" width="15" height="15" />}
          text="Sign Up"
          active={pathname === "/signup"}
        />
      </div>

      {/* HELP CARD */}
      <div className="bg-teal-400 rounded-xl p-4 text-white mt-6">
        <HelpCircle size={20} />
        <p className="mt-2 font-semibold">Need help?</p>
        <p className="text-sm opacity-90">
          Please check our docs
        </p>
        <button className="mt-4 bg-white text-teal-500 w-full py-2 rounded-lg text-sm font-semibold">
          DOCUMENTATION
        </button>
      </div>

    </aside>
  );
}

function MenuItem({ href, icon, text, active }) {
  return (
    <Link href={href}>
      <div
        className={`flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer mb-1
        ${active
          ? "bg-teal-100 text-teal-600"
          : "text-gray-600 hover:bg-gray-100"
        }`}
      >
        {icon}
        <span className="text-sm">{text}</span>
      </div>
    </Link>
  );
}
