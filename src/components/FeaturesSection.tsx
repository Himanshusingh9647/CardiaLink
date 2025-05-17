import { Activity, Database, Heart, LineChart, Laptop, Shield } from "lucide-react";
import { motion } from "framer-motion";

export function FeaturesSection() {
  return (
    <section className="py-16 bg-black features-section" id="features">
      <div className="container px-4 md:px-6 relative">
        {/* Red glow effects */}
        <div className="absolute top-1/4 -left-20 w-72 h-72 bg-red-600 rounded-full filter blur-[120px] opacity-20"></div>
        <div className="absolute bottom-1/4 -right-20 w-72 h-72 bg-red-600 rounded-full filter blur-[120px] opacity-20"></div>
        
        <div className="flex flex-col items-center justify-center space-y-4 text-center relative z-10">
          <motion.div 
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7 }}
            className="space-y-2"
          >
            <div className="inline-block rounded-lg bg-red-900/30 px-3 py-1 text-sm text-red-500 border border-red-800/50">
              Features
            </div>
            <h2 className="text-3xl font-bold tracking-tighter sm:text-5xl bg-clip-text text-transparent bg-gradient-to-r from-red-500 to-red-700">
              Cutting-Edge Technology for Health Risk Assessment
            </h2>
            <p className="max-w-[900px] text-gray-400 md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed">
              Our advanced platform combines AI and healthcare expertise to deliver personalized health risk assessments.
            </p>
          </motion.div>
        </div>
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="mx-auto grid max-w-5xl grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3 mt-12"
        >
          {features.map((feature, index) => (
            <motion.div 
              key={feature.title} 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.1 * (index + 1) }}
              whileHover={{ y: -5 }}
              className="bg-gray-900/50 border border-gray-800 rounded-xl p-6 transition-all duration-300"
            >
              <div className="mb-4">
                <feature.icon className="h-10 w-10 text-red-500" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">{feature.title}</h3>
              <p className="text-sm text-red-400 mb-3">{feature.description}</p>
              <p className="text-sm text-gray-400">{feature.content}</p>
            </motion.div>
          ))}
        </motion.div>
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
