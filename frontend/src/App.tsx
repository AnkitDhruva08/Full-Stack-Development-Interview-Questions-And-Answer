import { useState } from "react";
import { Toaster } from "../components/ui/sonner";
import HomePage from "../components/HomePage";


export default function App() {
  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-b from-slate-50 via-white to-slate-100">
      <HomePage />
      <Toaster />
    </div>
  );
}