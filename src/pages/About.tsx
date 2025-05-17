// src/pages/About.tsx
import React from "react";
import { Header } from "@/components/Header";
import { Footer } from "@/components/Footer";
import { Heart, Shield, Brain, LineChart, Users, Target, Award } from "lucide-react";

export default function About() {
  return (
    <div className="min-h-screen flex flex-col bg-black w-full overflow-hidden">
      <Header />
      <main className="flex-1 relative w-full">
        {/* Background effects */}
        <div className="absolute inset-0 bg-grid-white/[0.05] bg-[size:50px_50px]" />
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-red-500/5 to-transparent" />
        
        <div className="w-full max-w-7xl mx-auto px-4 md:px-6 relative">
          <div className="py-24">
            <div className="text-center mb-16">
              <h1 className="text-4xl font-bold tracking-tighter sm:text-5xl md:text-6xl bg-clip-text text-transparent bg-gradient-to-r from-red-500 to-red-700">
                About CardiaLink
              </h1>
              <p className="mt-4 text-xl text-gray-400 max-w-2xl mx-auto">
                Empowering individuals with AI-driven health insights and personalized insurance recommendations.
              </p>
            </div>

            <div className="grid gap-12 md:grid-cols-2 lg:grid-cols-3 mb-16">
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-r from-red-500/20 to-red-700/20 rounded-2xl" />
                <div className="relative bg-black/50 backdrop-blur-sm rounded-2xl p-6 border border-red-500/20">
                  <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-red-500/10 mb-4">
                    <Users className="h-6 w-6 text-red-500" />
                  </div>
                  <h3 className="text-xl font-semibold text-white mb-2">Our Team</h3>
                  <p className="text-gray-400">
                    A diverse team of healthcare professionals, data scientists, and insurance experts working together to revolutionize health risk assessment.
                  </p>
                </div>
              </div>

              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-r from-red-500/20 to-red-700/20 rounded-2xl" />
                <div className="relative bg-black/50 backdrop-blur-sm rounded-2xl p-6 border border-red-500/20">
                  <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-red-500/10 mb-4">
                    <Target className="h-6 w-6 text-red-500" />
                  </div>
                  <h3 className="text-xl font-semibold text-white mb-2">Our Vision</h3>
                  <p className="text-gray-400">
                    To make personalized health risk assessment accessible to everyone, helping individuals make informed decisions about their health and insurance.
                  </p>
                </div>
              </div>

              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-r from-red-500/20 to-red-700/20 rounded-2xl" />
                <div className="relative bg-black/50 backdrop-blur-sm rounded-2xl p-6 border border-red-500/20">
                  <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-red-500/10 mb-4">
                    <Award className="h-6 w-6 text-red-500" />
                  </div>
                  <h3 className="text-xl font-semibold text-white mb-2">Our Values</h3>
                  <p className="text-gray-400">
                    Innovation, accuracy, privacy, and user-centricity guide everything we do at CardiaLink.
                  </p>
                </div>
              </div>
            </div>

            <div className="grid gap-8 md:grid-cols-2">
              <div className="space-y-6">
                <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl bg-clip-text text-transparent bg-gradient-to-r from-red-500 to-red-700">
                  Our Technology
                </h2>
                <p className="text-gray-400">
                  We leverage cutting-edge AI and machine learning algorithms to analyze health data and provide accurate risk assessments. Our models are trained on extensive datasets and regularly updated to ensure the highest accuracy.
                </p>
                <div className="grid gap-4">
                  <div className="flex items-center gap-3">
                    <div className="h-2 w-2 rounded-full bg-red-500" />
                    <span className="text-gray-300">Advanced AI Algorithms</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="h-2 w-2 rounded-full bg-red-500" />
                    <span className="text-gray-300">Real-time Data Processing</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="h-2 w-2 rounded-full bg-red-500" />
                    <span className="text-gray-300">Secure Data Storage</span>
                  </div>
                </div>
              </div>

              <div className="space-y-6">
                <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl bg-clip-text text-transparent bg-gradient-to-r from-red-500 to-red-700">
                  Our Commitment
                </h2>
                <p className="text-gray-400">
                  We are committed to providing accurate, reliable, and secure health risk assessments while maintaining the highest standards of data privacy and security.
                </p>
                <div className="grid gap-4">
                  <div className="flex items-center gap-3">
                    <div className="h-2 w-2 rounded-full bg-red-500" />
                    <span className="text-gray-300">HIPAA Compliance</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="h-2 w-2 rounded-full bg-red-500" />
                    <span className="text-gray-300">Regular Security Audits</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="h-2 w-2 rounded-full bg-red-500" />
                    <span className="text-gray-300">Continuous Improvement</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}