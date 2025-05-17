import { ReactNode } from "react";
import { Heart } from "lucide-react";
import { Link } from "react-router-dom";

interface AuthLayoutProps {
  children: ReactNode;
  title: string;
  description: string;
  footer: ReactNode;
}

export function AuthLayout({ children, title, description, footer }: AuthLayoutProps) {
  return (
    <div className="flex min-h-screen w-full flex-col bg-black overflow-hidden">
      {/* Red glow effects */}
      <div className="fixed top-1/4 left-1/4 w-96 h-96 bg-red-600 rounded-full filter blur-[128px] opacity-20"></div>
      <div className="fixed bottom-1/4 right-1/4 w-96 h-96 bg-red-700 rounded-full filter blur-[128px] opacity-20"></div>
      
      {/* Grid background effect */}
      <div className="fixed inset-0 bg-grid-white/[0.05] bg-[size:50px_50px]" />
      
      <div className="flex flex-1 flex-col items-center justify-center px-4 py-10 sm:px-6 lg:px-8 relative z-10">
        <Link to="/" className="mb-4 flex items-center gap-2 text-2xl font-bold text-red-500">
          <Heart className="h-6 w-6 fill-red-500 text-red-500" />
          <span>CardiaLink</span>
        </Link>
        <div className="w-full max-w-md space-y-6 overflow-hidden rounded-lg border border-gray-800 bg-gray-900/50 backdrop-blur-sm p-6 shadow-lg sm:p-8 md:max-w-xl">
          <div className="flex flex-col space-y-2 text-center">
            <h1 className="text-2xl font-semibold tracking-tight text-white">{title}</h1>
            <p className="text-sm text-gray-400">{description}</p>
          </div>
          {children}
          {footer}
        </div>
      </div>
    </div>
  );
}
