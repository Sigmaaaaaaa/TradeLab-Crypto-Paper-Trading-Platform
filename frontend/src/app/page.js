"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

import { useAuth } from "../context/AuthContext";

export default function HomePage() {
  const router = useRouter();
  const { isAuthenticated, loading } = useAuth();

  useEffect(() => {
    if (!loading) router.replace(isAuthenticated ? "/dashboard" : "/login");
  }, [loading, isAuthenticated, router]);

  return <main className="min-h-screen bg-slate-100" />;
}