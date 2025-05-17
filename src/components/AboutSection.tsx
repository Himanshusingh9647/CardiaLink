import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { CardContent, Card } from "@/components/ui/card";
import { Microscope, HeartPulse, ShieldCheck, Database } from "lucide-react";

export function AboutSection() {
  // Redirect to prediction page with loading animation
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

  return (
    <section id="about" className="w-full py-12 md:py-24 lg:py-32 bg-gradient-to-b from-black to-gray-900 relative overflow-hidden about-section">
      {/* Red glow effects */}
      <div className="absolute top-20 right-0 w-96 h-96 bg-red-600 rounded-full filter blur-[150px] opacity-10"></div>
      <div className="absolute -bottom-40 left-1/4 w-96 h-96 bg-red-600 rounded-full filter blur-[150px] opacity-10"></div>
      
      <div className="container px-4 md:px-6 relative z-10">
        <div className="flex flex-col items-center justify-center space-y-4 text-center mb-12">
          <Badge className="bg-red-600 hover:bg-red-500 text-white" variant="secondary">
            About Us
          </Badge>
          <h2 className="text-3xl font-bold tracking-tighter sm:text-5xl md:text-6xl red-text-gradient">
            Our Mission
          </h2>
          <p className="max-w-[800px] text-gray-300 md:text-xl">
            At CardiaLink, we're on a mission to revolutionize how health risks are assessed and how insurance premiums are calculated.
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          <Card className="bg-black/60 border border-gray-800 shadow-lg hover:shadow-red-500/5 transition duration-300">
            <CardContent className="p-6 flex flex-col items-center text-center space-y-4">
              <div className="p-2 rounded-full bg-red-900/20 w-16 h-16 flex items-center justify-center">
                <HeartPulse className="h-8 w-8 text-red-500" />
              </div>
              <h3 className="text-xl font-bold text-white">Heart Disease</h3>
              <p className="text-gray-300">
                Our advanced algorithms analyze cardiovascular data to predict heart disease risk with high accuracy.
              </p>
            </CardContent>
          </Card>
          
          <Card className="bg-black/60 border border-gray-800 shadow-lg hover:shadow-red-500/5 transition duration-300">
            <CardContent className="p-6 flex flex-col items-center text-center space-y-4">
              <div className="p-2 rounded-full bg-red-900/20 w-16 h-16 flex items-center justify-center">
                <Microscope className="h-8 w-8 text-red-500" />
              </div>
              <h3 className="text-xl font-bold text-white">Kidney Disease</h3>
              <p className="text-gray-300">
                We assess renal function and identify potential kidney disease risk factors to enable early intervention.
              </p>
            </CardContent>
          </Card>
          
          <Card className="bg-black/60 border border-gray-800 shadow-lg hover:shadow-red-500/5 transition duration-300">
            <CardContent className="p-6 flex flex-col items-center text-center space-y-4">
              <div className="p-2 rounded-full bg-red-900/20 w-16 h-16 flex items-center justify-center">
                <Database className="h-8 w-8 text-red-500" />
              </div>
              <h3 className="text-xl font-bold text-white">Diabetes Risk</h3>
              <p className="text-gray-300">
                Our platform evaluates metabolic health to predict diabetes risk and provide personalized prevention strategies.
              </p>
            </CardContent>
          </Card>
          
          <Card className="bg-black/60 border border-gray-800 shadow-lg hover:shadow-red-500/5 transition duration-300">
            <CardContent className="p-6 flex flex-col items-center text-center space-y-4">
              <div className="p-2 rounded-full bg-red-900/20 w-16 h-16 flex items-center justify-center">
                <ShieldCheck className="h-8 w-8 text-red-500" />
              </div>
              <h3 className="text-xl font-bold text-white">Insurance Fairness</h3>
              <p className="text-gray-300">
                We enable fair insurance premium calculations based on actual health data rather than broad demographics.
              </p>
            </CardContent>
          </Card>
        </div>
        
        <div className="grid gap-6 lg:grid-cols-2 lg:gap-12 items-center">
          <div className="space-y-6">
            <div className="space-y-3">
              <h3 className="text-2xl font-bold text-white">Our Technology</h3>
              <p className="text-gray-300">
                We utilize state-of-the-art machine learning models trained on extensive medical datasets to provide accurate health risk assessments. Our technology is constantly updated with the latest medical research to ensure the highest accuracy.
              </p>
            </div>
            <div className="space-y-3">
              <h3 className="text-2xl font-bold text-white">Privacy First</h3>
              <p className="text-gray-300">
                We prioritize your data privacy and security. All health data is processed with the highest level of encryption and security protocols, and we never share your personal information without explicit consent.
              </p>
            </div>
            <div className="mt-6">
              <Button onClick={redirectToPrediction} className="bg-gradient-to-r from-red-600 to-red-800 hover:from-red-700 hover:to-red-900 text-white">
                Start Your Assessment
              </Button>
            </div>
          </div>
          
          <div className="relative">
            <div className="absolute inset-0 border-2 border-red-500 rounded-lg opacity-30 animate-pulse"></div>
            <Card className="p-6 bg-black/90 border border-gray-800 shadow-lg rounded-lg overflow-hidden">
              <CardContent className="space-y-4">
                <h3 className="text-xl font-bold text-white">Why Choose Us?</h3>
                <ul className="space-y-3">
                  <li className="flex items-start gap-2">
                    <div className="rounded-full bg-red-500/10 p-1 mt-1">
                      <svg className="h-4 w-4 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                      </svg>
                    </div>
                    <p className="text-gray-300">
                      <span className="font-medium text-white">State-of-the-Art AI Models</span> - Our algorithms are trained on vast medical datasets and validated by healthcare professionals.
                    </p>
                  </li>
                  <li className="flex items-start gap-2">
                    <div className="rounded-full bg-red-500/10 p-1 mt-1">
                      <svg className="h-4 w-4 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                      </svg>
                    </div>
                    <p className="text-gray-300">
                      <span className="font-medium text-white">Comprehensive Risk Assessment</span> - We evaluate multiple diseases simultaneously to provide a holistic view of your health.
                    </p>
                  </li>
                  <li className="flex items-start gap-2">
                    <div className="rounded-full bg-red-500/10 p-1 mt-1">
                      <svg className="h-4 w-4 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                      </svg>
                    </div>
                    <p className="text-gray-300">
                      <span className="font-medium text-white">Personalized Insurance Premiums</span> - Get fair insurance rates based on your actual health status.
                    </p>
                  </li>
                  <li className="flex items-start gap-2">
                    <div className="rounded-full bg-red-500/10 p-1 mt-1">
                      <svg className="h-4 w-4 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                      </svg>
                    </div>
                    <p className="text-gray-300">
                      <span className="font-medium text-white">Data Privacy Guaranteed</span> - Your health information is protected with enterprise-grade security.
                    </p>
                  </li>
                </ul>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </section>
  );
}
