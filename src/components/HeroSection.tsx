
import { Button } from "@/components/ui/button";
import { ArrowRight, Shield, Activity, BarChart } from "lucide-react";

export function HeroSection() {
  return (
    <section className="relative py-20 overflow-hidden">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-950/20 dark:to-blue-900/30 -z-10" />
      
      <div className="container px-4 md:px-6">
        <div className="grid gap-6 lg:grid-cols-[1fr_400px] lg:gap-12 xl:grid-cols-[1fr_600px]">
          <div className="flex flex-col justify-center space-y-4">
            <div className="inline-block rounded-lg bg-primary/10 px-3 py-1 text-sm text-primary">
              Revolutionizing Health Risk Assessment
            </div>
            <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl lg:text-6xl">
              Personalized Health Risk Assessments & Insurance Plans
            </h1>
            <p className="max-w-[600px] text-muted-foreground md:text-xl">
              CardiaLink uses AI to analyze real-time health data across multiple disease models, 
              enabling personalized insurance premiums and discounts based on your unique health profile.
            </p>
            <div className="flex flex-col gap-2 min-[400px]:flex-row">
              <Button className="gap-1">
                Get Started <ArrowRight className="h-4 w-4" />
              </Button>
              <Button variant="outline">Learn More</Button>
            </div>
            <div className="flex items-center gap-4 pt-4">
              <div className="flex items-center gap-1">
                <Shield className="h-4 w-4 text-primary" />
                <span className="text-sm font-medium">Privacy Protected</span>
              </div>
              <div className="flex items-center gap-1">
                <Activity className="h-4 w-4 text-primary" />
                <span className="text-sm font-medium">Real-time Analysis</span>
              </div>
              <div className="flex items-center gap-1">
                <BarChart className="h-4 w-4 text-primary" />
                <span className="text-sm font-medium">AI-Powered</span>
              </div>
            </div>
          </div>
          <div className="flex items-center justify-center">
            <div className="relative w-full max-w-[500px] aspect-square">
              <div className="absolute inset-0 bg-gradient-to-br from-blue-500 to-indigo-500 rounded-full blur-3xl opacity-20" />
              <img
                src="https://images.unsplash.com/photo-1576091160550-2173dba999ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80"
                alt="Digital health visualization"
                className="relative z-10 w-full rounded-lg object-cover"
              />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
