import { Button } from "@/components/ui/button";
import { ArrowRight, Shield, Activity, BarChart } from "lucide-react";
import { useEffect } from "react";

export function HeroSection() {
  // Enhanced scrolling function with animation
  const scrollToServices = () => {
    const servicesSection = document.getElementById('services');
    if (servicesSection) {
      // Add a highlight animation class to the services section
      servicesSection.classList.add('scroll-highlight');
      
      // Smooth scroll with enhanced easing
      window.scrollTo({
        top: servicesSection.offsetTop - 80, // Offset for header
        behavior: 'smooth'
      });
      
      // Remove highlight class after animation completes
      setTimeout(() => {
        servicesSection.classList.remove('scroll-highlight');
      }, 2000);
    }
  };

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

  // Add scroll animation styles once on component mount
  useEffect(() => {
    // Add scroll highlight animation CSS
    const style = document.createElement('style');
    style.innerHTML = `
      @keyframes scrollHighlight {
        0% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0); }
        50% { box-shadow: 0 0 0 15px rgba(59, 130, 246, 0.3); }
        100% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0); }
      }
      .scroll-highlight {
        animation: scrollHighlight 2s ease-out;
      }
      
      .scroll-reveal {
        opacity: 0;
        transform: translateY(20px);
        transition: opacity 0.8s ease, transform 0.8s ease;
      }
      
      .scroll-reveal.visible {
        opacity: 1;
        transform: translateY(0);
      }
      
      /* Loading Screen Styles */
      .loading-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(255, 255, 255, 0.97);
        backdrop-filter: blur(10px);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        transition: opacity 0.5s ease;
      }
      
      .fade-out {
        opacity: 0;
      }
      
      .medical-logo {
        width: 120px;
        height: 120px;
        margin-bottom: 30px;
        border-radius: 50%;
        background: linear-gradient(135deg, #3b82f6, #4f46e5);
        position: relative;
        animation: pulse 2s infinite, spin 10s linear infinite;
        box-shadow: 0 0 30px rgba(79, 70, 229, 0.4);
      }
      
      .medical-logo:before, .medical-logo:after {
        content: '';
        position: absolute;
        background: white;
      }
      
      .medical-logo:before {
        width: 80%;
        height: 20%;
        top: 40%;
        left: 10%;
        border-radius: 10px;
      }
      
      .medical-logo:after {
        width: 20%;
        height: 80%;
        top: 10%;
        left: 40%;
        border-radius: 10px;
      }
      
      @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
      }
      
      @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
      }
      
      .loading-text {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 20px;
        background: linear-gradient(to right, #3b82f6, #4f46e5);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        animation: textPulse 3s infinite;
      }
      
      @keyframes textPulse {
        0% { opacity: 0.8; }
        50% { opacity: 1; }
        100% { opacity: 0.8; }
      }
      
      .progress-container {
        width: 300px;
        height: 8px;
        background-color: #e2e8f0;
        border-radius: 4px;
        overflow: hidden;
        box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
      }
      
      .progress-bar {
        height: 100%;
        width: 0%;
        background: linear-gradient(to right, #3b82f6, #4f46e5);
        border-radius: 4px;
        transition: width 0.2s ease;
        position: relative;
        overflow: hidden;
      }
      
      .progress-bar:after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(
          45deg,
          rgba(255, 255, 255, 0) 0%,
          rgba(255, 255, 255, 0.3) 50%,
          rgba(255, 255, 255, 0) 100%
        );
        animation: shine 2s infinite;
      }
      
      @keyframes shine {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
      }
    `;
    document.head.appendChild(style);
    
    // Implement scroll reveal for elements
    const handleScroll = () => {
      const elements = document.querySelectorAll('.scroll-reveal:not(.visible)');
      elements.forEach(element => {
        const position = element.getBoundingClientRect();
        // If element is in viewport
        if (position.top < window.innerHeight - 100) {
          element.classList.add('visible');
        }
      });
    };
    
    // Initial check for elements in viewport
    setTimeout(handleScroll, 100);
    
    // Add scroll listener
    window.addEventListener('scroll', handleScroll);
    
    // Clean up
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  return (
    <section className="relative py-24 md:py-32 overflow-hidden">
      {/* Vector Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-50 to-blue-100 -z-10">
        {/* Healthcare Vector Design */}
        <svg
          className="absolute inset-0 w-full h-full opacity-30"
          width="100%"
          height="100%"
          viewBox="0 0 1200 800"
          xmlns="http://www.w3.org/2000/svg"
        >
          <defs>
            <linearGradient id="gradient1" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#3B82F6" stopOpacity="0.1" />
              <stop offset="100%" stopColor="#4F46E5" stopOpacity="0.3" />
            </linearGradient>
            <linearGradient id="gradient2" x1="100%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#3B82F6" stopOpacity="0.2" />
              <stop offset="100%" stopColor="#4F46E5" stopOpacity="0.4" />
            </linearGradient>
          </defs>
          
          {/* EKG/Heartbeat Lines */}
          <path d="M-100,200 L50,200 L75,150 L100,250 L125,150 L150,250 L175,200 L300,200" stroke="url(#gradient1)" strokeWidth="3" fill="none" />
          <path d="M350,200 L450,200 L475,150 L500,250 L525,150 L550,250 L575,200 L700,200" stroke="url(#gradient1)" strokeWidth="3" fill="none" />
          <path d="M750,200 L850,200 L875,150 L900,250 L925,150 L950,250 L975,200 L1100,200" stroke="url(#gradient1)" strokeWidth="3" fill="none" />
          
          <path d="M-100,300 L50,300 L75,250 L100,350 L125,250 L150,350 L175,300 L300,300" stroke="url(#gradient2)" strokeWidth="3" fill="none" />
          <path d="M350,300 L450,300 L475,250 L500,350 L525,250 L550,350 L575,300 L700,300" stroke="url(#gradient2)" strokeWidth="3" fill="none" />
          <path d="M750,300 L850,300 L875,250 L900,350 L925,250 L950,350 L975,300 L1100,300" stroke="url(#gradient2)" strokeWidth="3" fill="none" />
          
          {/* Heart Icons */}
          <path d="M200,450 C175,425 150,425 125,450 C100,475 100,525 125,550 L200,625 L275,550 C300,525 300,475 275,450 C250,425 225,425 200,450 Z" fill="#3B82F6" opacity="0.2" />
          <path d="M600,450 C575,425 550,425 525,450 C500,475 500,525 525,550 L600,625 L675,550 C700,525 700,475 675,450 C650,425 625,425 600,450 Z" fill="#4F46E5" opacity="0.2" />
          <path d="M1000,450 C975,425 950,425 925,450 C900,475 900,525 925,550 L1000,625 L1075,550 C1100,525 1100,475 1075,450 C1050,425 1025,425 1000,450 Z" fill="#3B82F6" opacity="0.2" />
          
          {/* DNA Double Helix */}
          <path d="M100,650 C150,680 250,620 300,650 C350,680 450,620 500,650 C550,680 650,620 700,650" stroke="#3B82F6" strokeWidth="2" fill="none" opacity="0.4" />
          <path d="M100,700 C150,670 250,730 300,700 C350,670 450,730 500,700 C550,670 650,730 700,700" stroke="#4F46E5" strokeWidth="2" fill="none" opacity="0.4" />
          
          {/* Connecting dots between the DNA strands */}
          <line x1="100" y1="650" x2="100" y2="700" stroke="#3B82F6" strokeWidth="1.5" opacity="0.3" />
          <line x1="200" y1="635" x2="200" y2="715" stroke="#4F46E5" strokeWidth="1.5" opacity="0.3" />
          <line x1="300" y1="650" x2="300" y2="700" stroke="#3B82F6" strokeWidth="1.5" opacity="0.3" />
          <line x1="400" y1="635" x2="400" y2="715" stroke="#4F46E5" strokeWidth="1.5" opacity="0.3" />
          <line x1="500" y1="650" x2="500" y2="700" stroke="#3B82F6" strokeWidth="1.5" opacity="0.3" />
          <line x1="600" y1="635" x2="600" y2="715" stroke="#4F46E5" strokeWidth="1.5" opacity="0.3" />
          <line x1="700" y1="650" x2="700" y2="700" stroke="#3B82F6" strokeWidth="1.5" opacity="0.3" />
          
          {/* Medical Symbols */}
          {/* Caduceus */}
          <circle cx="900" cy="650" r="30" fill="#4F46E5" opacity="0.2" />
          <path d="M900,610 L900,690" stroke="#4F46E5" strokeWidth="3" fill="none" opacity="0.5" />
          <path d="M875,630 C875,630 875,670 900,670 C925,670 925,630 925,630" stroke="#4F46E5" strokeWidth="2" fill="none" opacity="0.5" />
          <path d="M875,640 C875,640 875,680 900,680 C925,680 925,640 925,640" stroke="#4F46E5" strokeWidth="2" fill="none" opacity="0.5" />
          
          {/* Plus symbol */}
          <path d="M1050,650 L1150,650" stroke="#3B82F6" strokeWidth="4" fill="none" opacity="0.5" />
          <path d="M1100,600 L1100,700" stroke="#3B82F6" strokeWidth="4" fill="none" opacity="0.5" />
          
          {/* Small scattered health dots */}
          <circle cx="150" cy="100" r="5" fill="#3B82F6" opacity="0.3" />
          <circle cx="250" cy="120" r="3" fill="#4F46E5" opacity="0.3" />
          <circle cx="350" cy="90" r="4" fill="#3B82F6" opacity="0.3" />
          <circle cx="450" cy="110" r="6" fill="#4F46E5" opacity="0.3" />
          <circle cx="550" cy="100" r="3" fill="#3B82F6" opacity="0.3" />
          <circle cx="650" cy="120" r="5" fill="#4F46E5" opacity="0.3" />
          <circle cx="750" cy="90" r="4" fill="#3B82F6" opacity="0.3" />
          <circle cx="850" cy="110" r="3" fill="#4F46E5" opacity="0.3" />
          <circle cx="950" cy="100" r="6" fill="#3B82F6" opacity="0.3" />
          <circle cx="1050" cy="120" r="4" fill="#4F46E5" opacity="0.3" />
        </svg>
      </div>
      
      <div className="container px-4 md:px-6 relative z-10">
        <div className="max-w-3xl mx-auto text-center">
          <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl lg:text-6xl mb-6 scroll-reveal visible">
            Personalized Health Risk Assessments & Insurance Plans
          </h1>
          <p className="text-muted-foreground md:text-xl mb-8 scroll-reveal visible">
            Analyze your health data across multiple disease models for personalized insurance premiums and health recommendations tailored to your unique profile.
          </p>
          <div className="flex flex-col sm:flex-row justify-center gap-3 mb-12 scroll-reveal visible">
            <Button 
              onClick={redirectToPrediction} 
              className="gap-1 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 relative overflow-hidden group"
              size="lg"
            >
              <span className="relative z-10 flex items-center gap-1">
                Get Started <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
              </span>
              <span className="absolute inset-0 bg-gradient-to-r from-indigo-600 to-blue-600 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></span>
            </Button>
          </div>
          
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 max-w-2xl mx-auto">
            <div className="flex items-center gap-2 p-3 rounded-lg bg-white bg-opacity-80 backdrop-blur-sm shadow-sm scroll-reveal">
              <Shield className="h-5 w-5 text-primary" />
              <span className="text-sm font-medium">Privacy Protected</span>
            </div>
            <div className="flex items-center gap-2 p-3 rounded-lg bg-white bg-opacity-80 backdrop-blur-sm shadow-sm scroll-reveal">
              <Activity className="h-5 w-5 text-primary" />
              <span className="text-sm font-medium">Real-time Analysis</span>
            </div>
            <div className="flex items-center gap-2 p-3 rounded-lg bg-white bg-opacity-80 backdrop-blur-sm shadow-sm scroll-reveal">
              <BarChart className="h-5 w-5 text-primary" />
              <span className="text-sm font-medium">AI-Powered</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
