"use client";

import { useState, useEffect, useCallback } from "react";
import { useRouter } from "next/navigation";
import { toast } from "@/lib/utils/toast";
import { authAPI } from "@/lib/api/auth";
import type { User, LoginCredentials, SignupCredentials } from "@/types/auth";

interface UseAuthReturn {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (credentials: LoginCredentials) => Promise<void>;
  signup: (credentials: SignupCredentials) => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
}

export function useAuth(): UseAuthReturn {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  const isAuthenticated = !!user;

  // Initialize auth state
  useEffect(() => {
    const initAuth = async () => {
      try {
        const token = localStorage.getItem("auth_token");
        if (token) {
          const userData = await authAPI.getCurrentUser();
          setUser(userData);
        }
      } catch (err) {
      console.error("Logout error:", err);
        console.error("Auth initialization failed:", err);
        localStorage.removeItem("auth_token");
        localStorage.removeItem("user_data");
      } finally {
        setIsLoading(false);
      }
    };

    initAuth();
  }, []);

  const login = useCallback(
    async (credentials: LoginCredentials) => {
      setIsLoading(true);
      try {
        const response = await authAPI.login(credentials);

        // Store auth data
        localStorage.setItem("auth_token", response.token);
        localStorage.setItem("user_data", JSON.stringify(response.user));

        setUser(response.user);
        toast.success("Welcome back! 🎉", {
          description: "Redirecting to your dashboard...",
        });

        setTimeout(() => {
          router.push("/dashboard");
        }, 1000);
      } catch (err) {
      console.error("Logout error:", err);
        toast.error("Login failed", {
          description:
            err instanceof Error
              ? err.message
              : "Please check your credentials and try again",
        });
        throw err;
      } finally {
        setIsLoading(false);
      }
    },
    [router]
  );

  const signup = useCallback(
    async (credentials: SignupCredentials) => {
      setIsLoading(true);
      try {
        const response = await authAPI.signup(credentials);

        // Store auth data
        localStorage.setItem("auth_token", response.token);
        localStorage.setItem("user_data", JSON.stringify(response.user));

        setUser(response.user);
        toast.success("Account created successfully! 🚀", {
          description:
            "Welcome to SmartReadmeGen! Let's create amazing documentation.",
        });

        setTimeout(() => {
          router.push("/dashboard");
        }, 1000);
      } catch (err) {
      console.error("Logout error:", err);
        toast.error("Signup failed", {
          description:
            err instanceof Error
              ? err.message
              : "Please try again or contact support",
        });
        throw err;
      } finally {
        setIsLoading(false);
      }
    },
    [router]
  );

  const logout = useCallback(async () => {
    setIsLoading(true);
    try {
      await authAPI.logout();
      setUser(null);
      toast.success("Logged out successfully! 👋", {
        description: "Thanks for using SmartReadmeGen",
      });
      router.push("/");
    } catch (err) {
      console.error("Logout error:", err);
      toast.error("Logout failed", {
        description: "Something went wrong. Please try again.",
      });
    } finally {
      setIsLoading(false);
    }
  }, [router]);

  const refreshUser = useCallback(async () => {
    try {
      const userData = await authAPI.getCurrentUser();
      setUser(userData);
    } catch (err) {
      console.error("Logout error:", err);
      console.error("Error:", err);
      setUser(null);
    }
  }, []);

  return {
    user,
    isLoading,
    isAuthenticated,
    login,
    signup,
    logout,
    refreshUser,
  };
}
