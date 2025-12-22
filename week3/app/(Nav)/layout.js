import Sidebar from '@/app/components/ui/Sidebar';
import Navbar from '@/app/components/ui/Navbar';

export default function DashoardLayout({ children }) {
  return (
    <>
      <div className="flex">
        <Sidebar />

        <div className="flex-1 flex flex-col">
          <Navbar />
          <main className="p-6 ">{children}</main>
        </div>
      </div>
    </>
  );
}
