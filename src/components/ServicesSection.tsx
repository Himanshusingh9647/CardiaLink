
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Heart, Activity, Scan as ScanIcon, Droplet as DropletIcon } from "lucide-react";
import { cn } from "@/lib/utils";
import { Link } from "react-router-dom";

export function ServicesSection() {
  return (
    <section className="py-12 md:py-16 bg-muted/50" id="services">
      <div className="container px-4 md:px-6">
        <div className="flex flex-col items-center justify-center space-y-4 text-center mb-8 md:mb-12">
          <div className="inline-block rounded-lg bg-primary/10 px-3 py-1 text-sm text-primary">
            Services
          </div>
          <h2 className="text-2xl md:text-3xl lg:text-5xl font-bold tracking-tighter">
            Our Health Assessment Services
          </h2>
          <p className="max-w-[900px] text-muted-foreground text-sm md:text-base lg:text-xl/relaxed">
            Comprehensive health risk assessments across multiple disease categories
          </p>
        </div>
        
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6 lg:gap-8">
          {services.map((service, index) => (
            <Link 
              key={service.title} 
              to={service.href} 
              className="block transition-all duration-300 hover:-translate-y-2 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 rounded-lg"
            >
              <Card className={cn(
                "h-full shadow-sm hover:shadow-lg border-2 border-muted hover:border-primary/20 transition-all duration-300",
                index === 0 && "sm:col-span-2 lg:col-span-1 lg:row-span-1 bg-gradient-to-br from-primary/5 to-background"
              )}>
                <CardHeader className="p-4 md:p-6 space-y-2 md:space-y-4">
                  <div className="flex items-center gap-3">
                    <div className="p-2 rounded-full bg-primary/10">
                      <service.icon className="h-5 w-5 md:h-6 md:w-6 text-primary" />
                    </div>
                    <CardTitle className="text-base md:text-xl font-bold">{service.title}</CardTitle>
                  </div>
                  <CardDescription className="text-xs md:text-base">{service.description}</CardDescription>
                </CardHeader>
                <CardContent className="p-4 md:p-6 pt-0">
                  <ul className="space-y-2 md:space-y-3">
                    {service.features.map((feature) => (
                      <li key={feature} className="flex items-center gap-2 text-xs md:text-sm">
                        <div className="h-1.5 w-1.5 rounded-full bg-primary" />
                        <span>{feature}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
                <CardFooter className="p-4 md:p-6 pt-0 flex justify-end">
                  <div className="text-xs md:text-sm font-medium text-primary flex items-center gap-1">
                    View details
                    <svg 
                      xmlns="http://www.w3.org/2000/svg" 
                      width="16" 
                      height="16" 
                      viewBox="0 0 24 24" 
                      fill="none" 
                      stroke="currentColor" 
                      strokeWidth="2" 
                      strokeLinecap="round" 
                      strokeLinejoin="round" 
                      className="ml-1"
                    >
                      <path d="M5 12h14"></path>
                      <path d="m12 5 7 7-7 7"></path>
                    </svg>
                  </div>
                </CardFooter>
              </Card>
            </Link>
          ))}
        </div>
      </div>
    </section>
  );
}

// Custom diabetes icon (since it's not in lucide-react)
const DiabetesIcon = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <path d="M9 17v-2" />
    <path d="M12 17v-6" />
    <path d="M15 17v-4" />
    <path d="M12 13.5V12" />
    <path d="M3 3h18" />
    <path d="M3 21h18" />
    <path d="M3 12h3" />
    <path d="M12 3v3" />
    <path d="M12 18v3" />
  </svg>
);

// Custom lungs icon
const LungsIcon = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <path d="M6.081 20C6.946 20 7.588 18.848 7.588 17.429c0-1.118-.041-2.895.454-3.868.496-.973 1.487-1.824 2.294-2.29.576-.337 1.664-.256 2.331-.835.67-.878.493-1.733.493-2.867 0-1.14-.686-2.039-1.18-2.336M6.08 20H3.959M6.08 20l.001-.003M17.92 20c-.865 0-1.507-1.152-1.507-2.571 0-1.118.041-2.895-.454-3.868-.496-.973-1.487-1.824-2.294-2.29-.576-.337-1.664-.256-2.331-.835-.67-.878-.493-1.733-.493-2.867 0-1.14.686-2.039 1.18-2.336M17.92 20h2.121M17.92 20l-.001-.003M11.253 7.252V3" />
  </svg>
);

// Custom liver icon
const LiverIcon = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <path d="M14 11h1a5 5 0 0 1 5 5v2a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1v-1a1 1 0 0 0-1-1h-1a1 1 0 0 0-1 1v1a1 1 0 0 1-1 1H9a1 1 0 0 1-1-1v-2a5 5 0 0 1 5-5h1Z" />
    <path d="M18 9a3 3 0 0 0-3-3H9a3 3 0 0 0-3 3v1" />
    <path d="M9 14v-4a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v4" />
    <path d="M13 13h1" />
  </svg>
);

const services = [
  {
    title: "Heart Disease Risk Assessment",
    description: "Comprehensive analysis of cardiovascular health",
    icon: Heart,
    href: "/services/heart",
    features: [
      "In-depth heart health evaluation",
      "Risk factor identification",
      "Personalized prevention strategies",
      "Insurance premium adjustment recommendations",
      "Lifestyle modification suggestions"
    ]
  },
  {
    title: "Diabetes Risk Analysis",
    description: "Early detection and prevention of diabetes",
    icon: DiabetesIcon,
    href: "/services/diabetes",
    features: [
      "Blood glucose prediction models",
      "Lifestyle risk factor analysis",
      "Personalized diet recommendations",
      "Activity level assessment",
      "Insurance savings calculations"
    ]
  },
  {
    title: "Cancer Risk Evaluation",
    description: "Multi-cancer type risk assessment",
    icon: ScanIcon,
    href: "/services/cancer",
    features: [
      "Genetic predisposition analysis",
      "Environmental factor evaluation",
      "Early detection recommendations",
      "Screening schedule suggestions",
      "Specialized insurance options"
    ]
  },
  {
    title: "Kidney Health Check",
    description: "Comprehensive kidney function analysis",
    icon: DropletIcon,
    href: "/services/kidney",
    features: [
      "Kidney function prediction",
      "Chronic kidney disease risk assessment",
      "Hydration recommendations",
      "Dietary guidelines",
      "Preventive care options"
    ]
  },
  {
    title: "Liver Health Assessment",
    description: "Complete liver function evaluation",
    icon: LiverIcon,
    href: "/services/liver",
    features: [
      "Liver function test analysis",
      "Fatty liver risk prediction",
      "Alcohol consumption guidance",
      "Medication interaction warnings",
      "Personalized health recommendations"
    ]
  }
];
