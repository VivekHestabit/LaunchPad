import Sidebar from '@/app/components/ui/Sidebar';
import Navbar from '@/app/components/ui/Navbar';

export default function DashoardLayout({ children }) {
  return (
    <>
      <div className="flex m-5 p-5">
        <Sidebar />

        <div className="flex-1 flex flex-col">
          <Navbar />
          <main className="p-6 " data-aos="fade-right">
            {children}
          </main>
        </div>
      </div>
    </>
  );
}
