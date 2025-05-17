import { useEffect } from 'react';
import { useAnimation } from 'framer-motion';
import { useInView } from 'framer-motion';

export const useScrollAnimation = (threshold = 0.2) => {
  const controls = useAnimation();
  const [ref, inView] = useInView({ threshold });

  useEffect(() => {
    if (inView) {
      controls.start('visible');
    }
  }, [controls, inView]);

  return { ref, controls, inView };
}; 