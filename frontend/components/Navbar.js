// frontend/components/Navbar.js
import Link from 'next/link';
import { useState } from 'react';

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="bg-bamboo-green p-4">
      <div className="container mx-auto flex justify-between items-center">
        <h1 className="text-xl font-bold text-gold">Elite Trading</h1>
        <div className="md:hidden">
          <button onClick={() => setIsOpen(!isOpen)} className="text-gold">
            ☰
          </button>
        </div>
        <div className={`md:flex ${isOpen ? 'block' : 'hidden'} md:block`}>
          <Link href="/">
            <a className="block md:inline-block text-gold hover:bg-gold hover:text-gray-900 px-3 py-2 rounded">Dashboard</a>
          </Link>
          <Link href="/trades">
            <a className="block md:inline-block text-gold hover:bg-gold hover:text-gray-900 px-3 py-2 rounded">Trades</a>
          </Link>
          <Link href="/history">
            <a className="block md:inline-block text-gold hover:bg-gold hover:text-gray-900 px-3 py-2 rounded">History</a>
          </Link>
          <Link href="/balance">
            <a className="block md:inline-block text-gold hover:bg-gold hover:text-gray-900 px-3 py-2 rounded">Balance</a>
          </Link>
        </div>
      </div>
    </nav>
  );
}