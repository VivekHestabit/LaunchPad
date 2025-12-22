import Link from 'next/link';
import { Zap } from 'lucide-react';

export default function AboutPage() {
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
            <Link href="/about" className="font-bold underline text-teal-Li600">
              About
            </Link>
          </div>
        </div>
      </nav>

      {/* CONTENT */}
      <main className="max-w-2xl mx-auto py-20 px-4">
        <h1 className="text-2xl font-bold mb-6">About Purity</h1>

        <div className="space-y-6 text-gray-700 leading-normal">
          <p>
            Purity is a small project built to make web development easier. We
            focus on using standard HTML and CSS practices.
          </p>

          <h2 className="text-lg font-bold text-black pt-4">Our Goal</h2>
          <p>
            The goal is to provide a clean starting point for developers who
            don't want the bloat of modern frameworks and heavy animations.
          </p>

          <h2 className="text-lg font-bold text-black pt-4">The Team</h2>
          <p>
            We are a small team of developers who prefer simple tools over
            complex ones.
          </p>
        </div>

        <div className="mt-12 pt-8 border-t border-gray-100">
          <Link href="/" className="text-teal-600 hover:underline">
            &larr; Back to Home
          </Link>
        </div>
      </main>

      {/* FOOTER */}
      <footer className="py-10 border-t border-gray-200 text-center text-xs text-gray-500">
        <p>&copy; 2025 Purity UI. Simple Dashboard Tool.</p>
      </footer>
    </div>
  );
}
