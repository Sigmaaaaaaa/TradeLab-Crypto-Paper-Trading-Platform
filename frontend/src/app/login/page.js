"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

import LoginForm from "../../components/auth/LoginForm";
import { useAuth } from "../../context/AuthContext";

export default function LoginPage() {
  const router = useRouter();
  const { isAuthenticated, loading } = useAuth();

  useEffect(() => {
    if (!loading && isAuthenticated) router.replace("/dashboard");
  }, [loading, isAuthenticated, router]);

  if (loading || isAuthenticated) return null;

  return (
    <main className="relative flex min-h-screen items-center justify-center overflow-hidden bg-slate-950 px-4 py-10">
      <div className="absolute -left-32 -top-32 h-80 w-80 rounded-full bg-blue-600/30 blur-3xl" />
      <div className="absolute -bottom-40 -right-20 h-96 w-96 rounded-full bg-cyan-400/20 blur-3xl" />
      <div className="relative w-full max-w-md">
        <p className="mb-5 text-center text-sm font-semibold tracking-[0.2em] text-blue-300">TRADELAB</p>
        <LoginForm />
      </div>
    </main>
  );
}