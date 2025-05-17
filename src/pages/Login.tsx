import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { useToast } from "@/components/ui/use-toast";
import { AuthLayout } from "@/components/AuthLayout";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      // This is a placeholder for actual authentication
      // In a real app, this would connect to your auth provider
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      toast({
        title: "Successfully logged in",
        description: "Welcome back to CardiaLink",
      });
      
      navigate("/");
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Error logging in",
        description: "Please check your credentials and try again",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AuthLayout
      title="Welcome back"
      description="Enter your credentials to access your account"
      footer={
        <div className="mt-4 text-center text-sm text-gray-400">
          Don't have an account?{" "}
          <Link to="/signup" className="underline text-red-500 hover:text-red-400 transition-colors">
            Sign up
          </Link>
        </div>
      }
    >
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="email" className="text-gray-300">Email</Label>
            <Input
              id="email"
              type="email"
              placeholder="name@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              autoComplete="email"
              className="bg-gray-800/70 border-gray-700 text-white placeholder:text-gray-500 focus:border-red-500 focus:ring-red-500/20"
            />
          </div>
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <Label htmlFor="password" className="text-gray-300">Password</Label>
              <Link to="/forgot-password" className="text-xs text-red-500 hover:text-red-400 transition-colors">
                Forgot password?
              </Link>
            </div>
            <Input
              id="password"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              autoComplete="current-password"
              className="bg-gray-800/70 border-gray-700 text-white placeholder:text-gray-500 focus:border-red-500 focus:ring-red-500/20"
            />
          </div>
          <div className="flex items-center space-x-2">
            <Checkbox id="remember" className="border-gray-700 data-[state=checked]:bg-red-600 data-[state=checked]:border-red-600" />
            <Label htmlFor="remember" className="text-sm font-medium leading-none text-gray-300">
              Remember me
            </Label>
          </div>
        </div>
        <Button 
          type="submit" 
          className="w-full bg-gradient-to-r from-red-600 to-red-800 hover:from-red-700 hover:to-red-900 text-white transition-all duration-300" 
          disabled={isLoading}
        >
          {isLoading ? "Logging in..." : "Log in"}
        </Button>
      </form>
    </AuthLayout>
  );
};

export default Login;
