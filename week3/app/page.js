import Link from 'next/link';
import { Layout, Zap, Shield, ArrowRight } from 'lucide-react';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-white text-gray-900 font-sans">
      {/* SIMPLE NAVBAR */}
      <nav className="border-b border-gray-200 py-3">
        <div className="max-w-5xl mx-auto px-4 flex items-center justify-between">
          <div className="flex items-center gap-2 font-bold text-lg">
            <Zap className="w-5 h-5 text-teal-600" />
            <span>Purity UI</span>
          </div>

          <div className="flex gap-6 text-sm">
            <Link href="/" className="hover:underline">
              Home
            </Link>
            <Link href="/pricing" className="hover:underline">
              Pricing
            </Link>
            <Link href="/About" className="hover:underline">
              About
            </Link>
            <Link href="/login" className="hover:underline">
              Login
            </Link>
          </div>
        </div>
      </nav>

      {/* SIMPLE HERO */}
      <header className="py-20 px-4 border-b border-gray-100">
        <div className="max-w-2xl mx-auto text-center">
          <h1 className="text-3xl font-bold mb-4">
            Build your Dashboard simply.
          </h1>
          <p className="text-gray-600 mb-8">
            A basic tool for managing projects. No complex settings or heavy
            designs.
          </p>
          <div className="flex justify-center gap-4">
            <Link
              href="/signup"
              className="px-5 py-2 bg-teal-600 text-white font-medium"
            >
              Get Started
            </Link>
            <Link
              href="/dashboard"
              className="px-5 py-2 border border-gray-300 hover:bg-gray-50"
            >
              Live Demo
            </Link>
          </div>
        </div>
      </header>

      {/* SIMPLE FEATURES */}
      <section className="py-16 px-4">
        <div className="max-w-5xl mx-auto">
          <div className="grid md:grid-cols-3 gap-12">
            <div>
              <h3 className="font-bold border-b border-teal-600 w-fit mb-3">
                Layouts
              </h3>
              <p className="text-sm text-gray-600">
                Standard CSS grids that are easy to edit and maintain.
              </p>
            </div>
            <div>
              <h3 className="font-bold border-b border-teal-600 w-fit mb-3">
                Speed
              </h3>
              <p className="text-sm text-gray-600">
                Fast loading times because the code is kept very basic.
              </p>
            </div>
            <div>
              <h3 className="font-bold border-b border-teal-600 w-fit mb-3">
                Security
              </h3>
              <p className="text-sm text-gray-600">
                Standard data protection for all your dashboard information.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="py-10 border-t border-gray-200 text-center text-xs text-gray-500">
        <p>&copy; 2025 Purity UI. Simple Dashboard Tool.</p>
      </footer>
    </div>
  );
}
