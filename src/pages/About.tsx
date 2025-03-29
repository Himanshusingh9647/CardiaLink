// src/pages/About.tsx
import React from "react";
import { Header } from "@/components/Header";
import { Footer } from "@/components/Footer";
import { Shield, Activity, BarChart } from "lucide-react";

export default function AboutPage() {
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-1">
        {/* Hero Section */}
        <section className="relative py-20 overflow-hidden">
          {/* Background gradient */}
          <div className="absolute inset-0 bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-950/20 dark:to-blue-900/30 -z-10" />
          
          <div className="container px-4 md:px-6">
            <div className="mx-auto max-w-3xl text-center">
              <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl lg:text-6xl">
                About CardiaLink
              </h1>
              <p className="mt-6 text-muted-foreground md:text-xl">
                CardiaLink is an AI-powered web platform designed to personalize health risk assessments and insurance plans.
              </p>
            </div>
          </div>
        </section>

        {/* Main Content Section */}
        <section className="py-12">
          <div className="container px-4 md:px-6">
            <div className="grid gap-10 md:grid-cols-2 lg:gap-16">
              <div>
                <p className="text-muted-foreground mb-6">
                  By analyzing real-time data across various disease models—including all crucial cancer, diabetes, heart disease, kidney disease, and liver disease—CardiaLink evaluates individual health risks. This enables insurance companies to adjust premiums and offer personalized discounts based on each person's unique health profile.
                </p>
                <p className="text-muted-foreground">
                  Utilizing federated learning, CardiaLink ensures data privacy by processing information locally without sharing personal data. Our approach not only streamlines the underwriting process but also enhances accuracy and efficiency in insurance decision-making with cutting edge tech.
                </p>
              </div>
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-br from-blue-500 to-indigo-500 rounded-full blur-3xl opacity-20" />
                <div className="relative z-10 bg-white p-8 rounded-lg shadow-md">
                  <h2 className="text-2xl font-bold mb-6">Our Key Features</h2>
                  <div className="space-y-6">
                    <div className="flex items-start gap-4">
                      <div className="p-2 bg-primary/10 rounded-md">
                        <Activity className="h-6 w-6 text-primary" />
                      </div>
                      <div>
                        <h3 className="text-lg font-medium">Multi-Disease Prediction</h3>
                        <p className="text-muted-foreground">Integrates AI models for cancer, diabetes, heart, kidney, and liver disease risk assessment.</p>
                      </div>
                    </div>
                    
                    <div className="flex items-start gap-4">
                      <div className="p-2 bg-primary/10 rounded-md">
                        <BarChart className="h-6 w-6 text-primary" />
                      </div>
                      <div>
                        <h3 className="text-lg font-medium">Real-Time Risk Analysis</h3>
                        <p className="text-muted-foreground">Processes health data instantly to provide personalized insights.</p>
                      </div>
                    </div>
                    
                    <div className="flex items-start gap-4">
                      <div className="p-2 bg-primary/10 rounded-md">
                        <Shield className="h-6 w-6 text-primary" />
                      </div>
                      <div>
                        <h3 className="text-lg font-medium">Personalized Insurance Profiling</h3>
                        <p className="text-muted-foreground">The real-life valuable data generates discount offers based on individual health profiles and lifestyle improvements.</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
        
        {/* Additional Background Section */}
        <section className="py-16 bg-slate-50">
          <div className="container px-4 md:px-6">
            <div className="mx-auto max-w-2xl text-center mb-12">
              <h2 className="text-3xl font-bold mb-4">Our Approach</h2>
              <p className="text-muted-foreground">
                We're committed to transforming healthcare risk assessment and insurance through innovative AI technology, creating a more personalized, efficient, and equitable system for everyone.
              </p>
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </div>
  );
}