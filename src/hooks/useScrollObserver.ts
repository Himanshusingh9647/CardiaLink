import { useEffect } from 'react';

interface ScrollObserverOptions {
  threshold?: number;
  rootMargin?: string;
  onEnter?: (entry: IntersectionObserverEntry) => void;
  onExit?: (entry: IntersectionObserverEntry) => void;
}

export const useScrollObserver = (
  selector: string, 
  options: ScrollObserverOptions = {}
) => {
  const { 
    threshold = 0.1, 
    rootMargin = '0px', 
    onEnter = () => {}, 
    onExit = () => {} 
  } = options;

  useEffect(() => {
    const elements = document.querySelectorAll(selector);
    
    if (elements.length === 0) return;
    
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            // Element is now visible
            entry.target.classList.add('revealed');
            onEnter(entry);
          } else {
            // Element is no longer visible
            // Uncomment the next line if you want to reset the animation when it's out of view
            // entry.target.classList.remove('revealed');
            onExit(entry);
          }
        });
      },
      { threshold, rootMargin }
    );
    
    elements.forEach(el => observer.observe(el));
    
    return () => {
      elements.forEach(el => observer.unobserve(el));
    };
  }, [selector, threshold, rootMargin, onEnter, onExit]);
}; 