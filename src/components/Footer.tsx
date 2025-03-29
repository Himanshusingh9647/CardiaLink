import { Heart, ArrowRight, Github, Linkedin, Twitter } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { Input } from "@/components/ui/input";
import { Link } from "react-router-dom";

export function Footer() {
  return (
    <footer className="bg-gradient-to-br from-slate-900 to-slate-950 text-slate-50 pt-12 pb-6">
      <div className="container px-4 md:px-6">
        {/* Animated wave separator */}
        <div className="relative h-12 mb-8 overflow-hidden">
          <div className="absolute w-full">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320" className="text-blue-600 opacity-10">
              <path fill="currentColor" fillOpacity="1" d="M0,96L48,112C96,128,192,160,288,160C384,160,480,128,576,133.3C672,139,768,181,864,181.3C960,181,1056,139,1152,122.7C1248,107,1344,117,1392,122.7L1440,128L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path>
            </svg>
          </div>
        </div>
        
        <div className="grid gap-10 md:grid-cols-2 lg:grid-cols-3">
          {/* Brand Column */}
          <div className="space-y-4">
            <Link to="/" className="flex items-center gap-2 font-bold text-2xl group transition-all">
              <div className="relative transition-all">
                <Heart className="h-6 w-6 fill-blue-500 text-white group-hover:scale-110 transition-transform" />
                <span className="absolute -top-1 -right-1 w-2 h-2 bg-blue-500 rounded-full animate-ping opacity-75"></span>
              </div>
              <span className="text-blue-400 text-gradient bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-indigo-400">
                CardiaLink
              </span>
            </Link>
            <p className="text-sm text-slate-400">
              AI-powered health risk assessment and personalized insurance platform. Understand your health risks and get tailored insurance plans.
            </p>
            
            <div className="pt-4">
              <h4 className="text-sm font-semibold text-slate-200 mb-3">Connect With Us</h4>
              <div className="flex space-x-4">
                <Button size="icon" variant="ghost" className="rounded-full h-8 w-8 bg-slate-800/50 hover:bg-blue-900/50 hover:text-blue-400">
                  <Github className="h-4 w-4" />
                  <span className="sr-only">GitHub</span>
                </Button>
                <Button size="icon" variant="ghost" className="rounded-full h-8 w-8 bg-slate-800/50 hover:bg-blue-900/50 hover:text-blue-400">
                  <Twitter className="h-4 w-4" />
                  <span className="sr-only">Twitter</span>
                </Button>
                <Button size="icon" variant="ghost" className="rounded-full h-8 w-8 bg-slate-800/50 hover:bg-blue-900/50 hover:text-blue-400">
                  <Linkedin className="h-4 w-4" />
                  <span className="sr-only">LinkedIn</span>
                </Button>
              </div>
            </div>
          </div>
          
          {/* Quick Links Column */}
          <div className="space-y-4">
            <h3 className="text-lg font-medium text-blue-300">Quick Links</h3>
            <ul className="space-y-2 text-sm text-slate-400">
              <li>
                <a href="/" className="hover:text-blue-400 transition-colors flex items-center gap-1">
                  <ArrowRight className="h-3 w-3" /> Home
                </a>
              </li>
              <li>
                <a href="#services" className="hover:text-blue-400 transition-colors flex items-center gap-1">
                  <ArrowRight className="h-3 w-3" /> Services
                </a>
              </li>
              <li>
                <a href="/about" className="hover:text-blue-400 transition-colors flex items-center gap-1">
                  <ArrowRight className="h-3 w-3" /> About Us
                </a>
              </li>
              <li>
                <a href="/privacy" className="hover:text-blue-400 transition-colors flex items-center gap-1">
                  <ArrowRight className="h-3 w-3" /> Privacy Policy
                </a>
              </li>
              <li>
                <a href="/terms" className="hover:text-blue-400 transition-colors flex items-center gap-1">
                  <ArrowRight className="h-3 w-3" /> Terms of Service
                </a>
              </li>
            </ul>
          </div>
          
          {/* Newsletter Column */}
          <div className="space-y-4">
            <h3 className="text-lg font-medium text-blue-300">Stay Updated</h3>
            <p className="text-sm text-slate-400">Subscribe to our newsletter for the latest health insights and updates.</p>
            <div className="flex gap-2">
              <Input 
                type="email"
                placeholder="Enter your email"
                className="bg-slate-800/50 border-slate-700 placeholder:text-slate-500 focus-visible:ring-blue-400"
              />
              <Button size="sm" className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700">
                <ArrowRight className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>
        
        <Separator className="my-8 bg-slate-800" />
        
        <div className="flex flex-col md:flex-row items-center justify-between text-sm text-slate-500">
          <p>© {new Date().getFullYear()} CardiaLink. All rights reserved.</p>
          <div className="flex gap-6 mt-4 md:mt-0">
            <a href="/privacy" className="hover:text-blue-400 transition-colors">Privacy</a>
            <a href="/terms" className="hover:text-blue-400 transition-colors">Terms</a>
            <a href="/cookies" className="hover:text-blue-400 transition-colors">Cookies</a>
          </div>
        </div>
      </div>
    </footer>
  );
}
