
import React, { useState, useEffect } from 'react';
import { ArrowRight, CheckCircle, Brain, Activity, Wind } from 'lucide-react';
import { useAppContext } from '../context/AppContext';
import { BIAS_QUIZ_QUESTIONS } from '../constants';

export const WarmupView: React.FC = () => {
  const { dispatch, state } = useAppContext();
  const [step, setStep] = useState<1 | 2 | 3>(1);

  return (
    <div className="space-y-8 animate-fade-in">
      <div className="text-center space-y-2">
        <h2 className="text-sc-gold uppercase tracking-widest text-sm font-semibold">
          Focus Reset
        </h2>
        <h3 className="text-2xl text-sc-ivory font-bold">
          {step === 1 ? 'State Calibration' : step === 2 ? 'Cognitive Priming' : 'Physiological Sync'}
        </h3>
        {/* Progress Bar */}
        <div className="flex justify-center gap-2 pt-4">
          {[1, 2, 3].map(i => (
            <div key={i} className={`h-1.5 rounded-full transition-all duration-500 ${step >= i ? 'w-12 bg-sc-gold shadow-[0_0_10px_rgba(200,164,68,0.5)]' : 'w-4 bg-sc-muted/30'}`} />
          ))}
        </div>
      </div>

      <div className="bg-sc-navy/50 backdrop-blur-md rounded-2xl w-full border border-sc-gold/20 overflow-hidden relative shadow-2xl min-h-[400px] flex flex-col">
        {step === 1 && <StateCalibration onNext={() => setStep(2)} />}
        {step === 2 && <BiasBlitz onNext={() => setStep(3)} />}
        {step === 3 && <BreathingExercise onComplete={() => dispatch({ type: 'SET_VIEW', payload: 'journal' })} reducedMotion={state.settings.reducedMotion} />}
      </div>
    </div>
  );
};

// --- Sub-Components ---

const StateCalibration: React.FC<{ onNext: () => void }> = ({ onNext }) => {
  const [clarity, setClarity] = useState(50);
  const [energy, setEnergy] = useState(50);

  return (
    <div className="flex flex-col items-center justify-center p-8 h-full space-y-8 animate-fade-in">
      <div className="text-center space-y-2 max-w-md">
        <Activity size={32} className="mx-auto text-sc-gold mb-2" />
        <h4 className="text-xl text-sc-ivory font-semibold">Tune In</h4>
        <p className="text-sc-ivory/60 text-sm">Where is your mind right now? Adjust the sliders to match your state.</p>
      </div>

      <div className="w-full max-w-xs space-y-6">
        <div className="space-y-2">
          <div className="flex justify-between text-xs text-sc-gold uppercase tracking-wider font-semibold">
            <span>Foggy</span>
            <span>Clear</span>
          </div>
          <input 
            type="range" 
            min="0" max="100" 
            value={clarity}
            onChange={(e) => setClarity(Number(e.target.value))}
            className="w-full h-2 bg-sc-muted/30 rounded-lg appearance-none cursor-pointer accent-sc-gold hover:accent-sc-ivory transition-all"
          />
        </div>

        <div className="space-y-2">
          <div className="flex justify-between text-xs text-sc-gold uppercase tracking-wider font-semibold">
            <span>Reactive</span>
            <span>Proactive</span>
          </div>
          <input 
            type="range" 
            min="0" max="100" 
            value={energy}
            onChange={(e) => setEnergy(Number(e.target.value))}
            className="w-full h-2 bg-sc-muted/30 rounded-lg appearance-none cursor-pointer accent-sc-gold hover:accent-sc-ivory transition-all"
          />
        </div>
      </div>

      <button 
        onClick={onNext}
        className="mt-4 px-8 py-3 bg-sc-gold text-sc-navy font-bold rounded-full hover:scale-105 transition-all shadow-lg shadow-sc-gold/20 flex items-center gap-2"
      >
        Set Baseline <ArrowRight size={18} />
      </button>
    </div>
  );
};

const BiasBlitz: React.FC<{ onNext: () => void }> = ({ onNext }) => {
  const [qIndex, setQIndex] = useState(0);
  const [selected, setSelected] = useState<number | null>(null);
  const [showFeedback, setShowFeedback] = useState(false);

  const currentQ = BIAS_QUIZ_QUESTIONS[qIndex];

  const handleSelect = (idx: number) => {
    if (showFeedback) return;
    setSelected(idx);
    setShowFeedback(true);
    
    // Auto advance after brief pause
    setTimeout(() => {
      if (qIndex < BIAS_QUIZ_QUESTIONS.length - 1) {
        setQIndex(prev => prev + 1);
        setSelected(null);
        setShowFeedback(false);
      } else {
        onNext();
      }
    }, 1500);
  };

  return (
    <div className="flex flex-col items-center justify-center p-6 sm:p-8 h-full space-y-6 animate-fade-in w-full">
      <div className="text-center space-y-1">
        <Brain size={32} className="mx-auto text-sc-gold mb-2" />
        <h4 className="text-lg text-sc-ivory font-semibold">Bias Blitz {qIndex + 1}/{BIAS_QUIZ_QUESTIONS.length}</h4>
        <p className="text-sc-ivory/60 text-sm">Spot the thinking trap.</p>
      </div>

      <div className="w-full max-w-md bg-sc-ivory/5 border border-sc-gold/10 rounded-xl p-6 text-center">
        <p className="text-lg text-sc-ivory font-medium mb-6">{currentQ.question}</p>
        
        <div className="space-y-3">
          {currentQ.options.map((opt, idx) => {
            let btnClass = "bg-sc-navy border-sc-muted/50 hover:border-sc-gold";
            if (showFeedback) {
              if (idx === currentQ.correctIndex) btnClass = "bg-green-900/50 border-green-500 text-green-100";
              else if (idx === selected) btnClass = "bg-red-900/50 border-red-500 text-red-100";
              else btnClass = "opacity-50 border-transparent";
            } else if (selected === idx) {
               btnClass = "bg-sc-gold text-sc-navy border-sc-gold";
            }

            return (
              <button
                key={idx}
                onClick={() => handleSelect(idx)}
                disabled={showFeedback}
                className={`w-full p-3 rounded-lg border text-sm font-medium transition-all duration-200 ${btnClass}`}
              >
                {opt}
              </button>
            );
          })}
        </div>
        
        {showFeedback && (
          <div className="mt-4 text-xs text-sc-gold animate-fade-in">
            {currentQ.explanation}
          </div>
        )}
      </div>
    </div>
  );
};

const BreathingExercise: React.FC<{ onComplete: () => void; reducedMotion: boolean }> = ({ onComplete, reducedMotion }) => {
  return (
    <div className="flex flex-col items-center justify-center p-8 h-full relative w-full overflow-hidden">
      
      {!reducedMotion ? (
        <div className="relative flex items-center justify-center">
           {/* Outer Glow Halo */}
           <div className="absolute w-64 h-64 bg-sc-gold/10 rounded-full blur-3xl animate-pulse"></div>
           {/* Breathing Circle */}
           <div className="w-32 h-32 border-4 border-sc-gold/50 rounded-full flex items-center justify-center animate-breathing shadow-[0_0_30px_rgba(200,164,68,0.3)]">
             <div className="w-2 h-2 bg-sc-gold rounded-full"></div>
           </div>
        </div>
      ) : (
        <div className="text-sc-ivory text-center p-6 border border-sc-gold/30 rounded-xl bg-sc-ivory/5">
          <Wind size={32} className="mx-auto text-sc-gold mb-4" />
          <p className="text-lg font-bold">Box Breathing</p>
          <p className="mt-2 text-sc-ivory/70">Inhale 4s • Hold 4s • Exhale 4s • Hold 4s</p>
        </div>
      )}

      <div className="absolute bottom-8 flex flex-col items-center gap-4">
        <p className="text-sc-ivory/50 text-xs tracking-widest uppercase">Physiological Sync</p>
        <button
            onClick={onComplete}
            className="bg-sc-gold text-sc-navy font-bold py-3 px-10 rounded-full hover:scale-105 transition-transform focus-ring flex items-center gap-2 shadow-lg shadow-sc-gold/20"
        >
            <CheckCircle size={20} />
            Enter Flow State
        </button>
      </div>
    </div>
  );
};
