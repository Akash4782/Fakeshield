import React, { createContext, useContext, useState, useEffect, type ReactNode } from 'react';
import { API_BASE_URL } from '../config';

interface User {
  name: string;
  fullName?: string;
  email: string;
  subscription_tier: 'free' | 'paid';
  profile_pic?: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (token: string, user: User) => void;
  logout: () => void;
  updateUser: (newUser: Partial<User>) => void;
  isLoading: boolean;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const verifyToken = async () => {
      const savedToken = localStorage.getItem('fakeshield_token');
      const savedUser = localStorage.getItem('fakeshield_user');

      if (savedToken && savedUser) {
        try {
          // Verify with backend
          const response = await fetch(`${API_BASE_URL}/auth/me`, {
            headers: { 'Authorization': `Bearer ${savedToken}` }
          });
          
          if (response.ok) {
            const userData = await response.json();
            setToken(savedToken);
            setUser(userData);
          } else {
            // Token invalid or expired
            localStorage.removeItem('fakeshield_token');
            localStorage.removeItem('fakeshield_user');
          }
        } catch (e) {
          console.error("Token verification failed", e);
          // Don't necessarily logout if it's just a network error, 
          // but for "strictly protected" we might.
          // For now, let's just use the cached data if offline, or handle it gracefully.
          try {
            setToken(savedToken);
            setUser(JSON.parse(savedUser));
          } catch(err) {
             localStorage.removeItem('fakeshield_token');
             localStorage.removeItem('fakeshield_user');
          }
        }
      }
      setIsLoading(false);
    };

    verifyToken();
  }, []);

  const login = (newToken: string, newUser: User) => {
    setToken(newToken);
    setUser(newUser);
    localStorage.setItem('fakeshield_token', newToken);
    localStorage.setItem('fakeshield_user', JSON.stringify(newUser));
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('fakeshield_token');
    localStorage.removeItem('fakeshield_user');
  };

  const updateUser = (newData: Partial<User>) => {
    if (!user) return;
    const updatedUser = { ...user, ...newData };
    setUser(updatedUser);
    localStorage.setItem('fakeshield_user', JSON.stringify(updatedUser));
  };

  const value = {
    user,
    token,
    login,
    logout,
    updateUser,
    isLoading,
    isAuthenticated: !!token,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
