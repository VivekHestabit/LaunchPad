import SignupNav from '../components/ui/SignupNav';
export default function signup() {
  return (
    <>
      <div className=" relative w-full min-h-screen items-center justify-center bg-white p-4">
        <SignupNav />
        <div className="relative h-[520.5px] w-full rounded-2xl overflow-hidden">
          <img src="/Ban.svg" alt="" className="w-full h-full object-cover" />

          <div className="absolute inset-0 mb-40 flex flex-col items-center justify-center text-center px-6">
            <h1 className="text-white text-3xl font-extrabold">Welcome!</h1>
            <p className="text-white mt-4 max-w-xl">
              Use these awesome forms to login or create new <br />
              account in your project for free.
            </p>
          </div>
        </div>

        <div className=" absolute ml-165 -mt-[260px] flex items-center justify-center px-10 items-center ">
          <div className="h-[713.5px] w-[452.5px] flex flex-col  justify-center border rounded-3xl bg-white shadow-xl p-10">
            <div className="mt-100  mb-100  flex flex-col items-center justify-center  ">
              <h1 className="font-extrabold text-[#2D3748] text-xl">
                Register with
              </h1>
              <div className="flex gap-4 mt-4">
                <img src="/Facebook.svg" alt="" />
                <img src="/Apple.svg" alt="" />
                <img src="/Google.svg" alt="" />
              </div>
              <p className="text-2xl  mt-8 text-[#A0AEC0]">or</p>
              <form action="" className="w-full">
                <p className="text-black text-lg ">Name</p>
                <input
                  type="text"
                  placeholder="Your full name"
                  className="text-[#A0AEC0] mt-3 mb-3 border w-full rounded-2xl p-4 border-[#E2E8F0]"
                />
                <p className="text-black text-lg ">Email</p>
                <input
                  type="text"
                  placeholder="Your email address"
                  className="text-[#A0AEC0] mb-3  mt-3 border w-full rounded-2xl p-4 border-[#E2E8F0]"
                />
                <p className="text-black text-lg ">Password</p>
                <input
                  type="text"
                  placeholder="Your Password"
                  className="text-[#A0AEC0] mb-3  mt-3 border w-full rounded-2xl p-4 border-[#E2E8F0]"
                />
                <div className="flex gap-3 mt-4">
                  <img src="/Base.svg" alt="" />
                  <span className="text-[#2D3748]">Remeber me </span>
                </div>
                <button className="text-white pt-4 pb-4 text-xs w-full bg-[#4FD1C5] border rounded-2xl mt-8">
                  SIGN IN
                </button>
                <p className="ml-25 mt-5 ">
                  Already have an account?{' '}
                  <span className="text-[#4FD1C5] font-bold">Sign in</span>
                </p>
              </form>
            </div>
          </div>
        </div>
      </div>
      <footer className="mt-[100px] mb-[100px] flex justify-evenly pb-[15px]">
        <p className="text-[#A0AEC0]">
          @ 2021, Made with ❤️ by{' '}
          <span className="text-green-400">Creative Tim</span> &{' '}
          <span className="text-green-400">Simmmple</span> for a better web
        </p>

        <ul className="text-[#A0AEC0] flex gap-15">
          <li>Creative Tim</li>
          <li>Simmmple</li>
          <li>Blog</li>
          <li>License</li>
        </ul>
      </footer>
    </>
  );
}
