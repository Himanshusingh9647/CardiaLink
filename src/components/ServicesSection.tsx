import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { CardContent, Card } from "@/components/ui/card";
import { Activity, Heart, Shield, Microscope, Droplet, HeartPulse, CalendarClock } from "lucide-react";
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
    logo.innerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
        <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
      </svg>
    `;
    
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
    
    // Create percentage text
    const percentageText = document.createElement('div');
    percentageText.className = 'progress-percentage';
    percentageText.innerText = '0%';
    
    // Add all elements to the overlay
    overlay.appendChild(logo);
    overlay.appendChild(text);
    overlay.appendChild(progressContainer);
    overlay.appendChild(percentageText);
    document.body.appendChild(overlay);
    
    // Add visible class after a small delay to enable transition
    setTimeout(() => {
      overlay.classList.add('visible');
    }, 10);
    
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
        width += 1;
        progressBar.style.width = width + '%';
        percentageText.innerText = width + '%';
        
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
    <section id="services" className="w-full py-12 md:py-24 lg:py-32 bg-black relative overflow-hidden services-section">
      {/* Red glow effects */}
      <div className="absolute -bottom-40 right-0 w-96 h-96 bg-red-600 rounded-full filter blur-[150px] opacity-10"></div>
      <div className="absolute -top-20 left-0 w-96 h-96 bg-red-600 rounded-full filter blur-[150px] opacity-10"></div>
      
      <div className="container px-4 md:px-6 relative z-10">
        <div className="grid gap-6 lg:grid-cols-[1fr_500px] lg:gap-12 xl:grid-cols-[1fr_550px]">
          <div className="flex flex-col justify-center space-y-4">
            <div className="space-y-2">
              <Badge className="bg-red-600 hover:bg-red-500 text-white" variant="secondary">
                Our Services
              </Badge>
              <h2 className="text-3xl font-bold tracking-tighter md:text-4xl/tight red-text-gradient">
                Comprehensive Health Risk Assessment
              </h2>
              <p className="max-w-[600px] text-gray-300 md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed">
                Our AI-driven platform analyzes your medical data to provide accurate health risk assessments and personalized insurance recommendations.
              </p>
            </div>
            <div className="flex flex-col gap-2 min-[400px]:flex-row">
              <Button onClick={redirectToPrediction} className="bg-gradient-to-r from-red-600 to-red-800 hover:from-red-700 hover:to-red-900 text-white">
                Start Assessment
              </Button>
              <Button variant="outline" className="border-red-600 text-red-500 hover:text-red-400 hover:bg-black/50">
                View Demo
              </Button>
            </div>
          </div>
          <div className="flex items-center justify-center">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Card className="bg-black/60 border border-gray-800 shadow-lg hover:shadow-red-500/5 transition duration-300">
                <CardContent className="p-6">
                  <div className="flex items-center gap-4">
                    <div className="flex h-10 w-10 items-center justify-center rounded-full bg-red-900/20">
                      <Heart className="h-5 w-5 text-red-500" />
                    </div>
                    <div>
                      <h3 className="text-xl font-bold text-white">Heart Disease</h3>
                      <p className="text-sm text-gray-400">Cardiac risk analysis</p>
                    </div>
                  </div>
                  <div className="mt-4 text-gray-300">
                    Evaluates your cardiac health using multiple parameters including blood pressure, cholesterol, and ECG data.
                  </div>
                </CardContent>
              </Card>
              <Card className="bg-black/60 border border-gray-800 shadow-lg hover:shadow-red-500/5 transition duration-300">
                <CardContent className="p-6">
                  <div className="flex items-center gap-4">
                    <div className="flex h-10 w-10 items-center justify-center rounded-full bg-red-900/20">
                      <Droplet className="h-5 w-5 text-red-500" />
                    </div>
                    <div>
                      <h3 className="text-xl font-bold text-white">Kidney Disease</h3>
                      <p className="text-sm text-gray-400">Renal health assessment</p>
                    </div>
                  </div>
                  <div className="mt-4 text-gray-300">
                    Assesses kidney function through biomarker analysis and medical history evaluation.
                  </div>
                </CardContent>
              </Card>
              <Card className="bg-black/60 border border-gray-800 shadow-lg hover:shadow-red-500/5 transition duration-300">
                <CardContent className="p-6">
                  <div className="flex items-center gap-4">
                    <div className="flex h-10 w-10 items-center justify-center rounded-full bg-red-900/20">
                      <Activity className="h-5 w-5 text-red-500" />
                    </div>
                    <div>
                      <h3 className="text-xl font-bold text-white">Diabetes Risk</h3>
                      <p className="text-sm text-gray-400">Glucose metabolism analysis</p>
                    </div>
                  </div>
                  <div className="mt-4 text-gray-300">
                    Evaluates diabetes risk factors including blood glucose, BMI, and family history.
                  </div>
                </CardContent>
              </Card>
              <Card className="bg-black/60 border border-gray-800 shadow-lg hover:shadow-red-500/5 transition duration-300">
                <CardContent className="p-6">
                  <div className="flex items-center gap-4">
                    <div className="flex h-10 w-10 items-center justify-center rounded-full bg-red-900/20">
                      <Shield className="h-5 w-5 text-red-500" />
                    </div>
                    <div>
                      <h3 className="text-xl font-bold text-white">Insurance Premium</h3>
                      <p className="text-sm text-gray-400">Insurance premium adjustments based on your health profile</p>
                    </div>
                  </div>
                  <div className="mt-4 text-gray-300">
                    Personalized insurance quotes based on your comprehensive health risk assessment.
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>

        <div className="mt-16 grid gap-8 md:grid-cols-2 lg:grid-cols-3">
          <Card className="bg-black/60 border border-gray-800 shadow-lg hover:shadow-red-500/5 transition duration-300">
            <CardContent className="p-6 space-y-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-full bg-red-900/20">
                <HeartPulse className="h-6 w-6 text-red-500" />
              </div>
              <h3 className="text-xl font-bold text-white">Real-time Health Monitoring</h3>
              <p className="text-gray-300">
                Connect wearable devices for continuous health monitoring and improved assessment accuracy.
              </p>
            </CardContent>
          </Card>
          <Card className="bg-black/60 border border-gray-800 shadow-lg hover:shadow-red-500/5 transition duration-300">
            <CardContent className="p-6 space-y-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-full bg-red-900/20">
                <Microscope className="h-6 w-6 text-red-500" />
              </div>
              <h3 className="text-xl font-bold text-white">AI-Powered Analysis</h3>
              <p className="text-gray-300">
                Advanced machine learning algorithms process your health data for highly accurate predictions.
              </p>
            </CardContent>
          </Card>
          <Card className="bg-black/60 border border-gray-800 shadow-lg hover:shadow-red-500/5 transition duration-300">
            <CardContent className="p-6 space-y-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-full bg-red-900/20">
                <CalendarClock className="h-6 w-6 text-red-500" />
              </div>
              <h3 className="text-xl font-bold text-white">Preventive Care Planning</h3>
              <p className="text-gray-300">
                Receive customized preventive care recommendations to improve health outcomes.
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  );
}
