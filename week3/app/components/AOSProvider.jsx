'use client';

import { useEffect } from 'react';
import AOS from 'aos';

export default function AOSProvider({ children }) {
  useEffect(() => {
    AOS.init({
      duration: 500,
      once: true,
      easing: 'ease-in-out',
    });
  }, []);

  return children;
}
