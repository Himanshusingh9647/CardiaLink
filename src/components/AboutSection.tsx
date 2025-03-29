
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Separator } from "@/components/ui/separator";
import { BrainCircuit, Shield, Users, Code, LineChart } from "lucide-react";

export function AboutSection() {
  return (
    <section className="py-16 bg-slate-50 dark:bg-slate-900" id="about">
      <div className="container px-4 md:px-6">
        <div className="flex flex-col items-center justify-center space-y-4 text-center">
          <div className="space-y-2">
            <div className="inline-block rounded-lg bg-primary/10 px-3 py-1 text-sm text-primary">
              About Us
            </div>
            <h2 className="text-3xl font-bold tracking-tighter sm:text-5xl">
              Our Mission & Approach
            </h2>
            <p className="max-w-[900px] text-muted-foreground md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed">
              CardiaLink is transforming health risk assessment and insurance by combining AI technology with medical expertise.
            </p>
          </div>
        </div>
        
        <Tabs defaultValue="mission" className="mt-12 max-w-4xl mx-auto">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="mission">Our Mission</TabsTrigger>
            <TabsTrigger value="technology">Our Technology</TabsTrigger>
            <TabsTrigger value="team">Our Team</TabsTrigger>
          </TabsList>
          <TabsContent value="mission" className="p-4">
            <Card>
              <CardContent className="p-6">
                <div className="grid gap-6 lg:grid-cols-2">
                  <div>
                    <h3 className="text-2xl font-bold mb-4">Transforming Healthcare & Insurance</h3>
                    <p className="text-muted-foreground mb-4">
                      At CardiaLink, we're on a mission to revolutionize how health risks are assessed and how insurance premiums are calculated. 
                      By leveraging cutting-edge AI technology, we provide personalized health risk assessments that enable insurance companies to offer fairer, 
                      more personalized premiums based on individual health profiles.
                    </p>
                    <p className="text-muted-foreground mb-4">
                      Our goal is to create a win-win situation where individuals are motivated to improve their health while 
                      insurance companies can more accurately price their policies.
                    </p>
                    <Button variant="outline" className="mt-2">Learn More</Button>
                  </div>
                  <div className="flex items-center justify-center">
                    <div className="grid grid-cols-2 gap-4">
                      <div className="flex flex-col items-center text-center p-4">
                        <BrainCircuit className="h-10 w-10 text-primary mb-2" />
                        <h4 className="font-medium">AI-Powered</h4>
                        <p className="text-sm text-muted-foreground">Advanced algorithms for accurate predictions</p>
                      </div>
                      <div className="flex flex-col items-center text-center p-4">
                        <Shield className="h-10 w-10 text-primary mb-2" />
                        <h4 className="font-medium">Privacy-First</h4>
                        <p className="text-sm text-muted-foreground">Your data never leaves your device</p>
                      </div>
                      <div className="flex flex-col items-center text-center p-4">
                        <Users className="h-10 w-10 text-primary mb-2" />
                        <h4 className="font-medium">User-Centered</h4>
                        <p className="text-sm text-muted-foreground">Designed for real people</p>
                      </div>
                      <div className="flex flex-col items-center text-center p-4">
                        <LineChart className="h-10 w-10 text-primary mb-2" />
                        <h4 className="font-medium">Data-Driven</h4>
                        <p className="text-sm text-muted-foreground">Evidence-based recommendations</p>
                      </div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
          <TabsContent value="technology" className="p-4">
            <Card>
              <CardContent className="p-6">
                <div className="space-y-6">
                  <h3 className="text-2xl font-bold">Cutting-Edge Technology</h3>
                  <p className="text-muted-foreground">
                    CardiaLink leverages the latest advancements in artificial intelligence, machine learning, and federated learning to provide 
                    accurate health risk assessments while maintaining the highest standards of data privacy.
                  </p>
                  
                  <div className="space-y-4">
                    <div className="flex flex-col space-y-2">
                      <h4 className="font-medium flex items-center gap-2">
                        <Code className="h-5 w-5 text-primary" /> Federated Learning
                      </h4>
                      <p className="text-sm text-muted-foreground">
                        Our federated learning approach processes data locally on users' devices, ensuring sensitive health information never leaves their control.
                        The AI models improve over time without ever accessing personal data.
                      </p>
                      <Separator className="my-2" />
                    </div>
                    
                    <div className="flex flex-col space-y-2">
                      <h4 className="font-medium flex items-center gap-2">
                        <BrainCircuit className="h-5 w-5 text-primary" /> Multi-Disease AI Models
                      </h4>
                      <p className="text-sm text-muted-foreground">
                        We've developed specialized AI models for each disease category, trained on extensive medical datasets and validated by healthcare professionals.
                        These models work together to provide a comprehensive health risk assessment.
                      </p>
                      <Separator className="my-2" />
                    </div>
                    
                    <div className="flex flex-col space-y-2">
                      <h4 className="font-medium flex items-center gap-2">
                        <LineChart className="h-5 w-5 text-primary" /> Real-Time Analysis
                      </h4>
                      <p className="text-sm text-muted-foreground">
                        Our platform processes health data in real-time, providing instant insights and recommendations.
                        The system continuously adapts to new information, ensuring the most accurate and up-to-date risk assessments.
                      </p>
                      <Separator className="my-2" />
                    </div>
                    
                    <div className="flex flex-col space-y-2">
                      <h4 className="font-medium flex items-center gap-2">
                        <Shield className="h-5 w-5 text-primary" /> Privacy & Security
                      </h4>
                      <p className="text-sm text-muted-foreground">
                        We've implemented industry-leading security measures to protect user data.
                        Our platform is compliant with HIPAA, GDPR, and other relevant data protection regulations.
                      </p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
          <TabsContent value="team" className="p-4">
            <Card>
              <CardContent className="p-6">
                <h3 className="text-2xl font-bold mb-6">Our Expert Team</h3>
                <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                  <div className="flex flex-col items-center text-center">
                    <div className="w-24 h-24 rounded-full bg-primary/10 mb-4 flex items-center justify-center">
                      <Users className="h-12 w-12 text-primary" />
                    </div>
                    <h4 className="text-lg font-medium">Healthcare Professionals</h4>
                    <p className="text-sm text-muted-foreground mt-2">
                      Our team includes doctors, nurses, and medical researchers who ensure our models align with clinical best practices.
                    </p>
                  </div>
                  <div className="flex flex-col items-center text-center">
                    <div className="w-24 h-24 rounded-full bg-primary/10 mb-4 flex items-center justify-center">
                      <BrainCircuit className="h-12 w-12 text-primary" />
                    </div>
                    <h4 className="text-lg font-medium">AI & ML Engineers</h4>
                    <p className="text-sm text-muted-foreground mt-2">
                      Specialists in artificial intelligence and machine learning who develop and refine our predictive models.
                    </p>
                  </div>
                  <div className="flex flex-col items-center text-center">
                    <div className="w-24 h-24 rounded-full bg-primary/10 mb-4 flex items-center justify-center">
                      <LineChart className="h-12 w-12 text-primary" />
                    </div>
                    <h4 className="text-lg font-medium">Data Scientists</h4>
                    <p className="text-sm text-muted-foreground mt-2">
                      Experts who analyze health data patterns and ensure our models deliver accurate and reliable predictions.
                    </p>
                  </div>
                </div>
                <div className="text-center mt-8">
                  <Button variant="outline">Join Our Team</Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </section>
  );
}
