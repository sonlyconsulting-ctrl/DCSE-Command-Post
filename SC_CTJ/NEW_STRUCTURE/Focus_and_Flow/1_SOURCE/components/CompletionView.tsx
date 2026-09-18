import React, { useEffect } from 'react';
import { RotateCcw } from 'lucide-react';
import { useAppContext } from '../context/AppContext';
import confetti from 'canvas-confetti';

export const CompletionView: React.FC = () => {
  const { dispatch } = useAppContext();

  useEffect(() => {
    // Gentle gold confetti
    const duration = 3000;
    const end = Date.now() + duration;

    const frame = () => {
      confetti({
        particleCount: 2,
        angle: 60,
        spread: 55,
        origin: { x: 0 },
        colors: ['#C8A444', '#F6F2E9']
      });
      confetti({
        particleCount: 2,
        angle: 120,
        spread: 55,
        origin: { x: 1 },
        colors: ['#C8A444', '#F6F2E9']
      });

      if (Date.now() < end) {
        requestAnimationFrame(frame);
      }
    };
    frame();
  }, []);

  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-12 text-center animate-fade-in">
      
      <div className="relative">
        <div className="absolute inset-0 bg-sc-gold blur-3xl opacity-20 animate-pulse"></div>
        <div className="relative w-32 h-32 rounded-full border-4 border-sc-gold flex items-center justify-center bg-sc-navy">
          <span className="text-4xl">🌟</span>
        </div>
      </div>

      <div className="space-y-4 max-w-md">
        <h2 className="text-4xl font-bold text-sc-ivory">Flow State Achieved</h2>
        <p className="text-sc-ivory/70 text-lg">
          You've invested in your cognitive architecture today. 
          Carry this clarity into your next decision.
        </p>
      </div>

      <button
        onClick={() => dispatch({ type: 'RESET_SESSION' })}
        className="group bg-transparent border border-sc-gold text-sc-gold hover:bg-sc-gold hover:text-sc-navy font-bold py-3 px-8 rounded-full transition-all focus-ring flex items-center gap-2"
      >
        <RotateCcw size={20} className="group-hover:-rotate-180 transition-transform duration-500" />
        Start New Session
      </button>
    </div>
  );
};