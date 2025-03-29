import { Button } from "@/components/ui/button";
import { Heart, Activity, BarChart, Shield, Database, Brain } from "lucide-react";
import { Link } from "react-router-dom";
import { useEffect } from "react";

export function ServicesSection() {
  // Redirect to the prediction page with loading animation
  const redirectToPrediction = () => {
    // Create and show loading overlay
    const overlay = document.createElement('div');
    overlay.className = 'loading-overlay';
    
    // Create pulsing medical logo
    const logo = document.createElement('div');
    logo.className = 'medical-logo';
    
    // Create animated text
    const text = document.createElement('div');
    text.className = 'loading-text';
    text.innerText = 'Initializing Health Assessment...';
    
    // Create progress bar
    const progressContainer = document.createElement('div');
    progressContainer.className = 'progress-container';
    
    const progressBar = document.createElement('div');
    progressBar.className = 'progress-bar';
    progressContainer.appendChild(progressBar);
    
    // Add all elements to the overlay
    overlay.appendChild(logo);
    overlay.appendChild(text);
    overlay.appendChild(progressContainer);
    document.body.appendChild(overlay);
    
    // Animate progress bar
    let width = 0;
    const interval = setInterval(() => {
      if (width >= 100) {
        clearInterval(interval);
        // Open prediction page after animation completes
        window.open('http://127.0.0.1:5000/heart', '_blank');
        // Remove overlay with fade-out
        overlay.classList.add('fade-out');
        setTimeout(() => document.body.removeChild(overlay), 500);
      } else {
        width += 2;
        progressBar.style.width = width + '%';
        
        // Update text based on progress
        if (width > 25 && width <= 50) {
          text.innerText = 'Loading AI Models...';
        } else if (width > 50 && width <= 75) {
          text.innerText = 'Preparing Health Interface...';
        } else if (width > 75) {
          text.innerText = 'Almost Ready...';
        }
      }
    }, 30);
  };

  // Staggered animation entry for service items
  useEffect(() => {
    // Stagger the animation of items with the benefit-item class
    const staggerItems = () => {
      const items = document.querySelectorAll('.stagger-item:not(.visible)');
      items.forEach((item, index) => {
        setTimeout(() => {
          const position = item.getBoundingClientRect();
          if (position.top < window.innerHeight - 50) {
            item.classList.add('visible');
          }
        }, index * 100); // 100ms stagger
      });
    };

    // Initial check
    setTimeout(staggerItems, 300);
    
    // Add scroll listener
    window.addEventListener('scroll', staggerItems);
    
    return () => {
      window.removeEventListener('scroll', staggerItems);
    };
  }, []);

  return (
    <section className="py-16 md:py-24 bg-muted/50" id="services">
      <div className="container px-4 md:px-6">
        <div className="flex flex-col items-center justify-center space-y-4 text-center mb-10 md:mb-16 scroll-reveal">
          <div className="inline-block rounded-lg bg-primary/10 px-3 py-1 text-sm text-primary">
            Our Platform
          </div>
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold tracking-tighter max-w-4xl">
            Comprehensive Health Risk Detection
          </h2>
          <p className="max-w-[900px] text-muted-foreground md:text-xl">
            Advanced AI-powered risk assessment across all major disease categories
          </p>
        </div>
        
        <div className="grid md:grid-cols-2 gap-8 lg:gap-12 items-center">
          <div className="space-y-6 scroll-reveal">
            <div className="space-y-3">
              <h3 className="text-2xl font-bold">Integrated Multi-Disease Analysis</h3>
              <p className="text-muted-foreground">
                Our platform analyzes your health data across multiple disease models including heart disease, diabetes, and kidney and liver conditions to provide a holistic view of your health risks.
              </p>
            </div>
            
            <div className="grid gap-4 sm:grid-cols-2">
              <div className="flex items-start gap-3 stagger-item scroll-reveal">
                <div className="shrink-0 p-1.5 rounded-md bg-primary/10">
                  <Heart className="h-5 w-5 text-primary" />
                </div>
                <div>
                  <h4 className="font-medium">Cardiovascular</h4>
                  <p className="text-sm text-muted-foreground">Comprehensive heart health risk analysis</p>
                </div>
              </div>
              
              <div className="flex items-start gap-3 stagger-item scroll-reveal">
                <div className="shrink-0 p-1.5 rounded-md bg-primary/10">
                  <Activity className="h-5 w-5 text-primary" />
                </div>
                <div>
                  <h4 className="font-medium">Diabetes</h4>
                  <p className="text-sm text-muted-foreground">Blood glucose and metabolic risk assessment</p>
                </div>
              </div>
              
              <div className="flex items-start gap-3 stagger-item scroll-reveal">
                <div className="shrink-0 p-1.5 rounded-md bg-primary/10">
                  <Brain className="h-5 w-5 text-primary" />
                </div>
                <div>
                  <h4 className="font-medium">Organ Health</h4>
                  <p className="text-sm text-muted-foreground">Kidney and liver function analysis</p>
                </div>
              </div>
            </div>
            
            <div className="space-y-3 pt-4 scroll-reveal">
              <h3 className="text-2xl font-bold">Personalized Insurance Benefits</h3>
              <p className="text-muted-foreground">
                Our risk assessment enables insurance companies to offer personalized premiums and discounts based on your unique health profile, leading to potential cost savings.
              </p>
              
              <div className="flex items-center gap-2 mt-6">
                <Button 
                  onClick={redirectToPrediction} 
                  className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 relative overflow-hidden group"
                >
                  <span className="relative z-10 flex items-center gap-1">
                    Start Your Assessment
                  </span>
                  <span className="absolute inset-0 bg-gradient-to-r from-indigo-600 to-blue-600 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></span>
                </Button>
              </div>
            </div>
          </div>
          
          <div className="relative scroll-reveal">
            <div className="absolute inset-0 bg-gradient-to-br from-blue-500 to-indigo-500 rounded-xl blur-3xl opacity-20" />
            <div className="relative z-10 bg-gradient-to-b from-white to-slate-50 p-8 rounded-xl shadow-lg border border-slate-100 hover:shadow-xl transition-shadow duration-300">
              <div className="flex items-center gap-3 mb-6">
                <div className="p-2 rounded-md bg-primary/10">
                  <Database className="h-6 w-6 text-primary" />
                </div>
                <h3 className="text-xl font-bold">Key Benefits</h3>
              </div>
              
              <ul className="space-y-4">
                <li className="flex items-start gap-3 stagger-item scroll-reveal">
                  <div className="h-5 w-5 rounded-full bg-green-100 flex items-center justify-center mt-0.5">
                    <svg viewBox="0 0 24 24" className="h-3 w-3 text-green-600" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M5 13l4 4L19 7" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                  </div>
                  <p className="text-slate-700">In-depth health risk evaluation across multiple disease categories</p>
                </li>
                <li className="flex items-start gap-3 stagger-item scroll-reveal">
                  <div className="h-5 w-5 rounded-full bg-green-100 flex items-center justify-center mt-0.5">
                    <svg viewBox="0 0 24 24" className="h-3 w-3 text-green-600" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M5 13l4 4L19 7" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                  </div>
                  <p className="text-slate-700">Personalized prevention strategies and lifestyle recommendations</p>
                </li>
                <li className="flex items-start gap-3 stagger-item scroll-reveal">
                  <div className="h-5 w-5 rounded-full bg-green-100 flex items-center justify-center mt-0.5">
                    <svg viewBox="0 0 24 24" className="h-3 w-3 text-green-600" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M5 13l4 4L19 7" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                  </div>
                  <p className="text-slate-700">Insurance premium adjustments based on your health profile</p>
                </li>
                <li className="flex items-start gap-3 stagger-item scroll-reveal">
                  <div className="h-5 w-5 rounded-full bg-green-100 flex items-center justify-center mt-0.5">
                    <svg viewBox="0 0 24 24" className="h-3 w-3 text-green-600" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M5 13l4 4L19 7" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                  </div>
                  <p className="text-slate-700">Secure data processing with federated learning technology</p>
                </li>
                <li className="flex items-start gap-3 stagger-item scroll-reveal">
                  <div className="h-5 w-5 rounded-full bg-green-100 flex items-center justify-center mt-0.5">
                    <svg viewBox="0 0 24 24" className="h-3 w-3 text-green-600" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M5 13l4 4L19 7" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                  </div>
                  <p className="text-slate-700">Continuous monitoring and real-time health insights</p>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
