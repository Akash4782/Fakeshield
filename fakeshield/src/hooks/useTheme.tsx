import React, { createContext, useContext, useState, useEffect, type ReactNode } from 'react';

type Theme = 'dark' | 'light';

interface ThemeContextType {
  theme: Theme;
  toggleTheme: (event?: React.MouseEvent | MouseEvent) => void;
}

const ThemeContext = createContext<ThemeContextType>({
  theme: 'dark',
  toggleTheme: () => {},
});

export const useTheme = () => useContext(ThemeContext);

export const ThemeProvider = ({ children }: { children: ReactNode }) => {
  const [theme, setTheme] = useState<Theme>(() => {
    const saved = localStorage.getItem('fakeshield-theme');
    return (saved === 'light' || saved === 'dark') ? saved : 'dark';
  });

  useEffect(() => {
    localStorage.setItem('fakeshield-theme', theme);
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  const toggleTheme = (event?: React.MouseEvent | MouseEvent) => {
    // @ts-expect-error - startViewTransition is a new API
    const isAppearanceTransition = document.startViewTransition && 
      !window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (!isAppearanceTransition) {
      setTheme(prev => (prev === 'dark' ? 'light' : 'dark'));
      return;
    }

    const x = event ? (event instanceof MouseEvent ? event.clientX : (event as React.MouseEvent).nativeEvent.clientX) : window.innerWidth / 2;
    const y = event ? (event instanceof MouseEvent ? event.clientY : (event as React.MouseEvent).nativeEvent.clientY) : window.innerHeight / 2;
    const endRadius = Math.hypot(
      Math.max(x, window.innerWidth - x),
      Math.max(y, window.innerHeight - y)
    );

    document.documentElement.setAttribute('data-theme-transition', 'true');
    document.documentElement.style.setProperty('--x', x + 'px');
    document.documentElement.style.setProperty('--y', y + 'px');
    document.documentElement.style.setProperty('--r', endRadius + 'px');

    // @ts-expect-error - startViewTransition is a new API
    const transition = document.startViewTransition(async () => {
      setTheme(prev => (prev === 'dark' ? 'light' : 'dark'));
    });

    transition.finished.finally(() => {
      document.documentElement.removeAttribute('data-theme-transition');
    });
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};
