import { Heart, Shield, Brain, LineChart } from "lucide-react";

export function MissionSection() {
  return (
    <section className="py-24 bg-black relative overflow-hidden">
      {/* Background effects */}
      <div className="absolute inset-0 bg-grid-white/[0.05] bg-[size:50px_50px]" />
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-red-500/5 to-transparent" />
      
      <div className="container px-4 md:px-6 relative">
        <div className="grid gap-12 lg:grid-cols-2">
          <div className="space-y-6">
            <div className="space-y-2">
              <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl bg-clip-text text-transparent bg-gradient-to-r from-red-500 to-red-700">
                Our Mission
              </h2>
              <p className="text-gray-400">
                Empowering individuals with AI-driven health insights and personalized insurance recommendations.
              </p>
            </div>
            <div className="grid gap-6">
              <div className="flex gap-4">
                <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-red-500/10">
                  <Heart className="h-6 w-6 text-red-500" />
                </div>
                <div className="space-y-2">
                  <h3 className="text-xl font-semibold text-white">Health First</h3>
                  <p className="text-gray-400">
                    Prioritizing your well-being with accurate health risk assessments and personalized recommendations.
                  </p>
                </div>
              </div>
              <div className="flex gap-4">
                <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-red-500/10">
                  <Shield className="h-6 w-6 text-red-500" />
                </div>
                <div className="space-y-2">
                  <h3 className="text-xl font-semibold text-white">Secure & Private</h3>
                  <p className="text-gray-400">
                    Your health data is protected with enterprise-grade security and HIPAA compliance.
                  </p>
                </div>
              </div>
              <div className="flex gap-4">
                <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-red-500/10">
                  <Brain className="h-6 w-6 text-red-500" />
                </div>
                <div className="space-y-2">
                  <h3 className="text-xl font-semibold text-white">AI-Powered Insights</h3>
                  <p className="text-gray-400">
                    Leveraging advanced AI to provide accurate risk assessments and personalized recommendations.
                  </p>
                </div>
              </div>
              <div className="flex gap-4">
                <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-red-500/10">
                  <LineChart className="h-6 w-6 text-red-500" />
                </div>
                <div className="space-y-2">
                  <h3 className="text-xl font-semibold text-white">Insurance Optimization</h3>
                  <p className="text-gray-400">
                    Helping you find the right insurance coverage based on your health profile.
                  </p>
                </div>
              </div>
            </div>
          </div>
          <div className="relative">
            <div className="absolute inset-0 bg-gradient-to-r from-red-500/20 to-red-700/20 rounded-2xl" />
            <div className="relative bg-black/50 backdrop-blur-sm rounded-2xl p-6 border border-red-500/20">
              <div className="space-y-4">
                <div className="flex items-center gap-2">
                  <div className="h-2 w-2 rounded-full bg-red-500" />
                  <span className="text-sm font-medium text-red-500">Real-time Analysis</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="h-2 w-2 rounded-full bg-red-500" />
                  <span className="text-sm font-medium text-red-500">Personalized Insights</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="h-2 w-2 rounded-full bg-red-500" />
                  <span className="text-sm font-medium text-red-500">Insurance Optimization</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
} 