
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
    <div className="flex min-h-screen flex-col bg-muted/40">
      <div className="flex flex-col items-center justify-center px-4 py-10 sm:px-6 md:min-h-screen md:py-12 lg:px-8">
        <Link to="/" className="mb-4 flex items-center gap-2 text-2xl font-bold text-primary">
          <Heart className="h-6 w-6 fill-primary text-primary" />
          <span>CardiaLink</span>
        </Link>
        <div className="w-full max-w-md space-y-6 overflow-hidden rounded-lg border bg-background p-6 shadow-md sm:p-8 md:max-w-xl">
          <div className="flex flex-col space-y-2 text-center">
            <h1 className="text-2xl font-semibold tracking-tight">{title}</h1>
            <p className="text-sm text-muted-foreground">{description}</p>
          </div>
          {children}
          {footer}
        </div>
      </div>
    </div>
  );
}
