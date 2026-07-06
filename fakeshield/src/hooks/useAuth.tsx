import React, { createContext, useContext, useState, useEffect, type ReactNode } from 'react';
import { API_BASE_URL } from '../config';

interface User {
  name: string;
  fullName?: string;
  email: string;
  subscription_tier: 'free' | 'paid';
  subscription_expires_at?: string | null;
  profile_pic?: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (token: string, user: User, rememberMe?: boolean) => void;
  logout: () => void;
  updateUser: (newUser: Partial<User>) => void;
  isLoading: boolean;
  isAuthenticated: boolean;
}

const TOKEN_KEY = 'fakeshield_token';
const USER_KEY  = 'fakeshield_user';

/** Detect which storage currently holds our session. */
function getStorage(): Storage | null {
  if (localStorage.getItem(TOKEN_KEY))  return localStorage;
  if (sessionStorage.getItem(TOKEN_KEY)) return sessionStorage;
  return null;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user,      setUser]      = useState<User | null>(null);
  const [token,     setToken]     = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const verifyToken = async () => {
      const storage    = getStorage();
      const savedToken = storage?.getItem(TOKEN_KEY) ?? null;
      const savedUser  = storage?.getItem(USER_KEY)  ?? null;

      if (savedToken && savedUser) {
        try {
          const response = await fetch(`${API_BASE_URL}/auth/me`, {
            headers: { Authorization: `Bearer ${savedToken}` }
          });

          if (response.ok) {
            const userData = await response.json();
            setToken(savedToken);
            setUser(userData);
          } else {
            // Token invalid / expired
            storage?.removeItem(TOKEN_KEY);
            storage?.removeItem(USER_KEY);
          }
        } catch {
          // Network error — keep cached session
          try {
            const cachedUser = JSON.parse(savedUser);
            setToken(savedToken);
            setUser({ ...cachedUser, subscription_tier: 'free' });
          } catch {
            storage?.removeItem(TOKEN_KEY);
            storage?.removeItem(USER_KEY);
          }
        }
      }
      setIsLoading(false);
    };

    verifyToken();
  }, []);

  /**
   * Call after a successful login.
   * @param rememberMe  true  → persist in localStorage  (survives tab/browser close)
   *                   false → use sessionStorage only   (clears when browser is closed)
   */
  const login = (newToken: string, newUser: User, rememberMe = false) => {
    // Clear both storages first to avoid stale data
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    sessionStorage.removeItem(TOKEN_KEY);
    sessionStorage.removeItem(USER_KEY);

    const storage = rememberMe ? localStorage : sessionStorage;
    storage.setItem(TOKEN_KEY, newToken);
    storage.setItem(USER_KEY,  JSON.stringify(newUser));

    setToken(newToken);
    setUser(newUser);
  };

  const logout = () => {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    sessionStorage.removeItem(TOKEN_KEY);
    sessionStorage.removeItem(USER_KEY);
    setToken(null);
    setUser(null);
  };

  const updateUser = (newData: Partial<User>) => {
    if (!user) return;
    const updated = { ...user, ...newData };
    setUser(updated);
    // Persist to whichever storage holds the current session
    const storage = getStorage();
    storage?.setItem(USER_KEY, JSON.stringify(updated));
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout, updateUser, isLoading, isAuthenticated: !!token }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within an AuthProvider');
  return ctx;
};
