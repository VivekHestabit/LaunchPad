import './globals.css';
import 'aos/dist/aos.css';
import AOSProvider from './components/AOSProvider';
export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="bg-gray-50 border-black">
        <AOSProvider>{children}</AOSProvider>
      </body>
    </html>
  );
}
