import "./globals.css";
import Sidebar from "./components/ui/Sidebar";
import Navbar from "./components/ui/Navbar";

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="bg-gray-50">
        <div className="flex">
          
          <Sidebar/>

          <div className="flex-1 flex flex-col">
            <Navbar />
            <main className="p-6 flex-1">
              {children}
            </main>
          </div>

        </div>
      </body>
    </html>
  );
}
