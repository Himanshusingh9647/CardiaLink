import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import {
  NavigationMenu,
  NavigationMenuContent,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuTrigger,
} from "@/components/ui/navigation-menu";
import { cn } from "@/lib/utils";
import { Heart, ArrowRight } from "lucide-react";

export function Header() {
  const [scrolled, setScrolled] = useState(false);
  const [titleText, setTitleText] = useState("");
  const fullTitle = "CardiaLink";
  
  // Animated title effect - fixed to display the full text
  useEffect(() => {
    let timeoutId: NodeJS.Timeout;
    let intervalId: NodeJS.Timeout;
    
    const animateTitle = () => {
      // Use a recursive timeout approach to ensure all letters are typed
      let currentIndex = 0;
      
      const typeNextChar = () => {
        if (currentIndex <= fullTitle.length) {
          setTitleText(fullTitle.substring(0, currentIndex));
          currentIndex++;
          timeoutId = setTimeout(typeNextChar, 150);
        }
      };
      
      typeNextChar();
    };
    
    // Start the animation after a brief delay
    timeoutId = setTimeout(animateTitle, 500);
    
    // Clean up
    return () => {
      clearTimeout(timeoutId);
      clearInterval(intervalId);
    };
  }, []); // Only run on mount
  
  // Add cursor animation CSS
  useEffect(() => {
    const style = document.createElement('style');
    style.innerHTML = `
      @keyframes cursor-blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0; }
      }
      .animate-cursor {
        animation: cursor-blink 1s step-end infinite;
      }
    `;
    document.head.appendChild(style);
    
    return () => {
      document.head.removeChild(style);
    };
  }, []);
  
  // Handle scroll event to change header appearance
  useEffect(() => {
    const handleScroll = () => {
      const isScrolled = window.scrollY > 20;
      if (isScrolled !== scrolled) {
        setScrolled(isScrolled);
      }
    };
    
    window.addEventListener('scroll', handleScroll);
    
    // Check initial scroll position
    handleScroll();
    
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, [scrolled]);
  
  // Smooth scroll to sections
  const scrollToSection = (sectionId: string) => (e: React.MouseEvent) => {
    e.preventDefault();
    const section = document.getElementById(sectionId);
    if (section) {
      window.scrollTo({
        top: section.offsetTop - 80, // Offset for header
        behavior: 'smooth'
      });
    }
  };

  return (
    <header 
      className={cn(
        "sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 transition-all duration-300",
        scrolled ? "shadow-md h-14" : "h-16"
      )}
    >
      <div className={cn(
        "container flex items-center h-full transition-all duration-300",
        scrolled ? "py-1" : "py-2"
      )}>
        <Link to="/" className="flex items-center gap-2 font-bold text-2xl text-primary mr-4 group">
          <div className="relative">
            <Heart className={cn(
              "fill-blue-500 text-blue-500 transition-all duration-300 group-hover:scale-110",
              scrolled ? "h-5 w-5" : "h-6 w-6"
            )} />
            <span className="absolute -top-1 -right-1 w-2 h-2 bg-blue-500 rounded-full animate-ping opacity-75"></span>
          </div>
          <div className="overflow-hidden whitespace-nowrap">
            <span className={cn(
              "transition-all duration-300 text-blue-600 font-bold relative inline-block min-w-24",
              scrolled ? "text-xl" : "text-2xl"
            )}>
              {titleText || "C"}
              {titleText.length < fullTitle.length && (
                <span className="absolute right-0 top-0 h-full w-1 bg-blue-600 animate-cursor"></span>
              )}
            </span>
          </div>
        </Link>
        
        <NavigationMenu className="ml-auto">
          <NavigationMenuList>
            <NavigationMenuItem>
              <Link to="/">
                <NavigationMenuLink className={cn(
                  "group inline-flex h-10 w-max items-center justify-center rounded-md bg-background px-4 py-2 text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground focus:outline-none disabled:pointer-events-none disabled:opacity-50 data-[active]:bg-accent/50 data-[state=open]:bg-accent/50"
                )}>
                  Home
                </NavigationMenuLink>
              </Link>
            </NavigationMenuItem>
            <NavigationMenuItem>
              <a href="#services" onClick={scrollToSection('services')}>
                <NavigationMenuLink className={cn(
                  "group inline-flex h-10 w-max items-center justify-center rounded-md bg-background px-4 py-2 text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground focus:outline-none disabled:pointer-events-none disabled:opacity-50 data-[active]:bg-accent/50 data-[state=open]:bg-accent/50"
                )}>
                  Services
                </NavigationMenuLink>
              </a>
            </NavigationMenuItem>
            <NavigationMenuItem>
              <Link to="/about">
                <NavigationMenuLink className={cn(
                  "group inline-flex h-10 w-max items-center justify-center rounded-md bg-background px-4 py-2 text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground focus:outline-none disabled:pointer-events-none disabled:opacity-50 data-[active]:bg-accent/50 data-[state=open]:bg-accent/50"
                )}>
                  About Us
                </NavigationMenuLink>
              </Link>
            </NavigationMenuItem>
          </NavigationMenuList>
        </NavigationMenu>
        <div className="ml-4">
          <Link to="/login">
            <Button size="sm" className="ml-auto flex items-center gap-1 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700">
              Login/Signup
            </Button>
          </Link>
        </div>
      </div>
    </header>
  );
}

const services = [
  {
    title: "Cancer Risk Assessment",
    href: "/services/cancer",
    description: "Evaluate your risk for various types of cancer based on personal health data."
  },
  {
    title: "Diabetes Risk Analysis",
    href: "/services/diabetes",
    description: "Assess your risk of developing diabetes and receive personalized prevention strategies."
  },
  {
    title: "Heart Disease Evaluation",
    href: "/services/heart",
    description: "Comprehensive analysis of cardiovascular health and risk factors."
  },
  {
    title: "Kidney Health Assessment",
    href: "/services/kidney",
    description: "Evaluate kidney function and identify potential risk factors for kidney disease."
  },
  {
    title: "Liver Health Check",
    href: "/services/liver",
    description: "Assess liver health and identify potential risk factors for liver disease."
  },
  {
    title: "Insurance Premium Calculator",
    href: "/services/insurance",
    description: "Calculate potential insurance savings based on your health profile."
  },
];

const ListItem = React.forwardRef<
  React.ElementRef<"a">,
  React.ComponentPropsWithoutRef<"a">
>(({ className, title, children, ...props }, ref) => {
  return (
    <li>
      <NavigationMenuLink asChild>
        <a
          ref={ref}
          className={cn(
            "block select-none space-y-1 rounded-md p-3 leading-none no-underline outline-none transition-colors hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground",
            className
          )}
          {...props}
        >
          <div className="text-sm font-medium leading-none">{title}</div>
          <p className="line-clamp-2 text-sm leading-snug text-muted-foreground">
            {children}
          </p>
        </a>
      </NavigationMenuLink>
    </li>
  );
});
ListItem.displayName = "ListItem";
