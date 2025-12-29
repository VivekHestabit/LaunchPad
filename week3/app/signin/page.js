'use client';
import SignNav from '../components/ui/SignNav';
import { useState } from 'react';

export default function SignIn() {
  const [rememberMe, setRememberMe] = useState(false);
  return (
    <>
      <SignNav />
      <div className="flex flex-col min-h-screen w-screen ">
        <div className="flex min-h-screen w-screen overflow-hidden">
          <div className="w-2/3 bg-white flex items-center justify-center">
            <form
              action=""
              className=" h-[445px] w-[353px] l-[282px] t-[466px]"
            >
              <h1 className="text-[#4FD1C5] text-2xl font-extrabold">
                Welcome Back
              </h1>
              <p className="text-sm text-[#A0AEC0] mt-3">
                Enter your email and password to sign in
              </p>
              <div className="flex flex-col mt-5">
                <p className="text-lg text-[#2D3748]">Email</p>
                <input
                  type="text"
                  placeholder="Your email address"
                  className="text-[#A0AEC0] border rounded-2xl border-gray-300 p-3 "
                />
                <p className="text-lg text-[#2D3748] mt-5">Password</p>
                <input
                  type="text"
                  placeholder="Your email address"
                  className="text-[#A0AEC0] border rounded-2xl border-gray-300 p-3 "
                />
              </div>
              <div></div>
              <div className="flex items-center gap-3 mt-4">
                <div
                  onClick={() => setRememberMe(!rememberMe)}
                  className={`w-12 h-6 flex items-center rounded-full p-1 cursor-pointer transition-colors duration-300
      ${rememberMe ? 'bg-[#4FD1C5]' : 'bg-gray-300'}`}
                >
                  <div
                    className={`bg-white w-4 h-4 rounded-full shadow-md transform transition-transform duration-300
        ${rememberMe ? 'translate-x-6' : 'translate-x-0'}`}
                  ></div>
                </div>

                <span className="text-[#2D3748]">Remember me</span>
              </div>
              <button className="text-white pt-4 pb-4 text-xs w-full bg-[#4FD1C5] border rounded-2xl mt-8">
                SIGN IN
              </button>
              <div className="flex items-center justify-center mt-5">
                <h3 className="text-[#A0AEC0]">
                  Don't have an account?{' '}
                  <a className="text-[#4FD1C5]" href="/signup">
                    Sign up
                  </a>
                </h3>
              </div>
            </form>
          </div>

          <div className="w-1/2 bg-white">
            <img
              src="/SS.svg"
              alt=""
              className="w-full h-[872px] border rounded-b-3xl object-cover"
            />
          </div>
        </div>
        <div className="bg-white flex justify-evenly pb-15 ">
          <p className="text-[#A0AEC0]">
            @ 2021, Made with ❤️ by{' '}
            <span className="text-green-400">Creative Tim</span> &{' '}
            <span className="text-green-400">Simmmple</span> for a better web
          </p>
          <div className=" justify-between">
            <ul className="text-[#A0AEC0] flex gap-15">
              <li>Creative Tim</li>
              <li>Simmmple</li>
              <li>Blog</li>
              <li>License</li>
            </ul>
          </div>
        </div>
      </div>
    </>
  );
}
