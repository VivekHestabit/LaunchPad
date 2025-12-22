'use client';
import { usePathname } from "next/navigation";

export default function Navbar() {
    const pathname = usePathname();
    const pageName = pathname.split("/")[1] || "Dashboard";
    return (
        <header className="h-16 border-b flex items-center justify-between px-6">

            <div>
                <p className="text-lg text-gray-400 font-semibold h-18px w-45px">Pages / <span className="text-gray1000 border-shadow">{pageName}</span></p>
                <h3 className="text-gray-500 font-bold">{pageName}</h3>
            </div>

            <div className="flex items-center gap-6 justify-between">
                <div className="relative">
                    <img
                        src="/Search.svg"
                        alt="search"
                        className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4"
                    />
                    <input
                        type="text"
                        placeholder="Type here..."
                        className="bg-white pl-10 pr-3 py-1 rounded-md shadow-sm focus:outline-none text-gray-500 focus:ring-2 focus:ring-gray-400"
                    />
                </div>
                <div className="flex gap-2">
                    <img src="/Person2.svg" className="absoute top-1/2" alt="" />
                    <button className="text-gray-500 cursor-pointer">sign in</button>
                </div>
                <img height="15px" width="15px" src="/Settings.svg" alt="" />
                <img height="15px" width="15px" src="/Bell.svg" alt="" />
            </div>
        </header>
    );
}

function IconBox({ children }) {
    return (
        <div className="w-9 h-9 flex items-center justify-center rounded-lg hover:bg-gray-100 cursor-pointer">
            {children}
        </div>
    );
}
