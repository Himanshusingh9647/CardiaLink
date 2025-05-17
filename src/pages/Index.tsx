import { Header } from "@/components/Header";
import { HeroSection } from "@/components/HeroSection";
import { FeaturesSection } from "@/components/FeaturesSection";
import { ServicesSection } from "@/components/ServicesSection";
import { AboutSection } from "@/components/AboutSection";
import { Footer } from "@/components/Footer";
import { useEffect } from "react";
import "./IndexPage.css"; // Import custom styles for Index page

const Index = () => {
  // Apply black-red theme class to body element
  useEffect(() => {
    // Add the black-red theme class to the document body when component mounts
    document.body.classList.add('black-red');
    
    // Remove the class when component unmounts
    return () => {
      document.body.classList.remove('black-red');
    };
  }, []);

  // Initialize scroll observer manually to avoid potential issues
  useEffect(() => {
    const handleScrollAnimations = () => {
      const elements = document.querySelectorAll('.reveal-on-scroll');
      
      elements.forEach((el) => {
        const rect = el.getBoundingClientRect();
        const isVisible = rect.top <= window.innerHeight * 0.8;
        
        if (isVisible) {
          el.classList.add('revealed');
        }
      });
    };
    
    // Initial check
    handleScrollAnimations();
    
    // Add scroll listener
    window.addEventListener('scroll', handleScrollAnimations);
    
    return () => {
      window.removeEventListener('scroll', handleScrollAnimations);
    };
  }, []);

  return (
    <div className="main-page-container">
      <div className="main-page-content bg-black">
        <Header />
        <main className="flex-1">
          <HeroSection />
          <FeaturesSection />
          
          {/* Add animated gradient title before Services section */}
          <div className="py-12 text-center">
            <h2 className="text-3xl font-bold animated-gradient-text reveal-on-scroll">
              Discover Our Health Services
            </h2>
            <p className="text-gray-400 mt-4 max-w-2xl mx-auto reveal-on-scroll">
              Comprehensive health assessments powered by advanced AI technology
            </p>
          </div>
          
          <ServicesSection />
          
          {/* Add a line-reveal text section */}
          <div className="py-12 text-center">
            <div className="line-reveal max-w-2xl mx-auto">
              <span className="text-2xl font-bold text-white">Your health data matters.</span>
              <span className="text-xl text-gray-300">We provide powerful insights.</span>
              <span className="text-lg text-gray-400">Make informed decisions.</span>
              <span className="text-base text-red-500">CardiaLink cares for your heart.</span>
            </div>
          </div>
          
          <AboutSection />
        </main>
        <Footer />
      </div>
    </div>
  );
};

export default Index;
