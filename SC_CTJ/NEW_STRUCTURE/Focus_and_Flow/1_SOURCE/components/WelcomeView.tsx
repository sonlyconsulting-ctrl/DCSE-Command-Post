import React from 'react';
import { ArrowRight, ShieldCheck } from 'lucide-react';
import { useAppContext } from '../context/AppContext';
import { WELCOME_COPY } from '../constants';

export const WelcomeView: React.FC = () => {
  const { dispatch } = useAppContext();

  return (
    <div className="space-y-8 py-4 sm:py-12">
      <div className="text-center space-y-4">
        <h2 className="text-sc-gold text-sm font-semibold tracking-widest uppercase">
          {WELCOME_COPY.subtitle}
        </h2>
        <h1 className="text-3xl sm:text-5xl font-bold text-sc-ivory leading-tight">
          {WELCOME_COPY.title}
        </h1>
      </div>

      <div className="bg-sc-ivory/5 border border-sc-gold/20 rounded-2xl p-6 sm:p-8 space-y-4 shadow-xl backdrop-blur-sm">
        {WELCOME_COPY.body.map((paragraph, idx) => (
          <p key={idx} className="text-sc-ivory/90 leading-relaxed text-lg">
            {paragraph}
          </p>
        ))}
        
        <div className="flex items-center gap-2 text-sc-gold/80 text-sm pt-4">
          <ShieldCheck size={16} />
          <span>Local-first. No accounts. No cloud storage.</span>
        </div>
      </div>

      <div className="flex justify-center pt-4">
        <button
          onClick={() => dispatch({ type: 'SET_VIEW', payload: 'warmup' })}
          className="group relative bg-sc-gold text-sc-navy font-bold py-4 px-8 rounded-full text-lg shadow-lg shadow-sc-gold/20 hover:shadow-sc-gold/40 hover:-translate-y-0.5 transition-all duration-200 focus-ring flex items-center gap-2"
        >
          Begin Session
          <ArrowRight className="group-hover:translate-x-1 transition-transform" />
        </button>
      </div>
    </div>
  );
};