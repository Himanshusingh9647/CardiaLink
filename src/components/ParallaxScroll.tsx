import { useEffect, useState, ReactNode } from "react";

interface ParallaxScrollProps {
  children: ReactNode;
  speed?: number; // Speed of the parallax effect (1 = normal, 2 = twice as fast)
  direction?: "up" | "down" | "left" | "right";
  className?: string;
}

export function ParallaxScroll({
  children,
  speed = 0.5,
  direction = "up",
  className = "",
}: ParallaxScrollProps) {
  const [offset, setOffset] = useState(0);
  
  // Listen for scroll events
  useEffect(() => {
    const handleScroll = () => {
      const scrollY = window.scrollY;
      setOffset(scrollY);
    };
    
    window.addEventListener("scroll", handleScroll);
    
    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);
  
  // Calculate transform based on direction and speed
  const getTransform = () => {
    const value = offset * speed;
    
    switch (direction) {
      case "up":
        return `translateY(-${value}px)`;
      case "down":
        return `translateY(${value}px)`;
      case "left":
        return `translateX(-${value}px)`;
      case "right":
        return `translateX(${value}px)`;
      default:
        return `translateY(-${value}px)`;
    }
  };
  
  return (
    <div
      className={`parallax-scroll ${className}`}
      style={{ transform: getTransform() }}
    >
      {children}
    </div>
  );
} 