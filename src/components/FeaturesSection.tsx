
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Activity, Database, Heart, LineChart, Laptop, Shield } from "lucide-react";

export function FeaturesSection() {
  return (
    <section className="py-16 bg-slate-50 dark:bg-slate-900" id="features">
      <div className="container px-4 md:px-6">
        <div className="flex flex-col items-center justify-center space-y-4 text-center">
          <div className="space-y-2">
            <div className="inline-block rounded-lg bg-primary/10 px-3 py-1 text-sm text-primary">
              Features
            </div>
            <h2 className="text-3xl font-bold tracking-tighter sm:text-5xl">
              Cutting-Edge Technology for Health Risk Assessment
            </h2>
            <p className="max-w-[900px] text-muted-foreground md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed">
              Our advanced platform combines AI and healthcare expertise to deliver personalized health risk assessments.
            </p>
          </div>
        </div>
        <div className="mx-auto grid max-w-5xl grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3 mt-12">
          {features.map((feature) => (
            <Card key={feature.title} className="transition-all hover:shadow-lg">
              <CardHeader className="space-y-1">
                <feature.icon className="h-8 w-8 text-primary" />
                <CardTitle className="text-xl">{feature.title}</CardTitle>
                <CardDescription>{feature.description}</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">{feature.content}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}

const features = [
  {
    title: "Multi-Disease Prediction",
    description: "Comprehensive health risk assessment",
    content: "Integrates AI models for cancer, diabetes, heart, kidney, and liver disease risk assessment, providing a holistic view of your health profile.",
    icon: Heart
  },
  {
    title: "Real-Time Risk Analysis",
    description: "Instant health insights",
    content: "Processes health data instantly to provide personalized insights and recommendations based on your unique health profile.",
    icon: Activity
  },
  {
    title: "Personalized Insurance Profiling",
    description: "Tailored insurance options",
    content: "Generates discount offers based on individual health profiles and lifestyle improvements, helping you save on insurance premiums.",
    icon: LineChart
  },
  {
    title: "HyperPrecision ML",
    description: "Highly accurate predictions",
    content: "Ensures high accuracy with top machine learning models designed for extreme accuracy and reliability in health risk predictions.",
    icon: Database
  },
  {
    title: "User-Friendly Dashboard",
    description: "Intuitive interface",
    content: "Provides intuitive insights, recommendations, and insurance options tailored to users, making complex health data easy to understand.",
    icon: Laptop
  },
  {
    title: "Privacy-First Approach",
    description: "Secure data handling",
    content: "Utilizes federated learning to process information locally without sharing personal data, ensuring your health information remains private.",
    icon: Shield
  }
];
