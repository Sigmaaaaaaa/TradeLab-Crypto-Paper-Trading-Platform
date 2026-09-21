"use client";

import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import Cookies from "js-cookie";

import { getMe, login as loginRequest, register as registerRequest } from "../lib/api";

const TOKEN_COOKIE = "token";

export const AuthContext = createContext(null);

function getErrorMessage(error) {
  return error?.response?.data?.detail || error?.message || "Something went wrong";
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const clearSession = useCallback(() => {
    Cookies.remove(TOKEN_COOKIE);
    setUser(null);
  }, []);

  useEffect(() => {
    let active = true;

    async function restoreSession() {
      const token = Cookies.get(TOKEN_COOKIE);
      if (!token) {
        if (active) setLoading(false);
        return;
      }

      try {
        const response = await getMe();
        if (active) setUser(response.data);
      } catch (error) {
        if (error?.response?.status === 401) clearSession();
      } finally {
        if (active) setLoading(false);
      }
    }

    restoreSession();
    return () => {
      active = false;
    };
  }, [clearSession]);

  const authenticate = useCallback(async (request) => {
    try {
      const response = await request();
      const { access_token: token, user: authenticatedUser } = response.data;
      Cookies.set(TOKEN_COOKIE, token, { sameSite: "lax" });
      setUser(authenticatedUser);
      return authenticatedUser;
    } catch (error) {
      throw new Error(getErrorMessage(error));
    }
  }, []);

  const login = useCallback(
    (email, password) => authenticate(() => loginRequest(email, password)),
    [authenticate]
  );

  const register = useCallback(
    async (email, password) => {
      try {
        await registerRequest(email, password);
        clearSession();
      } catch (error) {
        throw new Error(getErrorMessage(error));
      }
    },
    [clearSession]
  );

  const logout = useCallback(() => clearSession(), [clearSession]);

  const value = useMemo(
    () => ({ user, loading, isAuthenticated: Boolean(user), login, register, logout }),
    [user, loading, login, register, logout]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used inside an AuthProvider");
  }
  return context;
}