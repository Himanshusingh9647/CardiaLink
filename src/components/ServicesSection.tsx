
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Heart, Activity, Scan as ScanIcon, Droplet as DropletIcon } from "lucide-react";
import { cn } from "@/lib/utils";
import { Link } from "react-router-dom";

export function ServicesSection() {
  return (
    <section className="py-16" id="services">
      <div className="container px-4 md:px-6">
        <div className="flex flex-col items-center justify-center space-y-4 text-center">
          <div className="space-y-2">
            <div className="inline-block rounded-lg bg-primary/10 px-3 py-1 text-sm text-primary">
              Services
            </div>
            <h2 className="text-3xl font-bold tracking-tighter sm:text-5xl">
              Our Health Assessment Services
            </h2>
            <p className="max-w-[900px] text-muted-foreground md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed">
              Comprehensive health risk assessments across multiple disease categories
            </p>
          </div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-12">
          {services.map((service, index) => (
            <Link 
              key={service.title} 
              to={service.href} 
              className="block transition-transform hover:-translate-y-1 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 rounded-lg"
            >
              <Card className={cn("overflow-hidden h-full hover:shadow-lg cursor-pointer", 
                index === 0 && "lg:col-span-2 lg:row-span-2")}>
                <CardHeader className="p-6">
                  <div className="flex items-center gap-2">
                    <service.icon className="h-6 w-6 text-primary" />
                    <CardTitle>{service.title}</CardTitle>
                  </div>
                  <CardDescription>{service.description}</CardDescription>
                </CardHeader>
                <CardContent className="p-6 pt-0">
                  <ul className="space-y-2 text-sm">
                    {service.features.map((feature) => (
                      <li key={feature} className="flex items-center">
                        <div className="mr-2 h-1.5 w-1.5 rounded-full bg-primary" />
                        {feature}
                      </li>
                    ))}
                  </ul>
                </CardContent>
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
