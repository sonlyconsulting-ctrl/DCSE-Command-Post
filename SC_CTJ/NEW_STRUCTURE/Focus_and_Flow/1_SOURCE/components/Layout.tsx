import React, { useState } from 'react';
import { Settings, X, Type, Zap, Eye, Accessibility } from 'lucide-react';
import { useAppContext } from '../context/AppContext';

export const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [menuOpen, setMenuOpen] = useState(false);
  const { state, dispatch } = useAppContext();

  return (
    <div className="flex flex-col min-h-screen font-sans transition-colors duration-200">
      {/* Header */}
      <header className="border-b border-sc-gold/30 bg-sc-navy/95 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-sc-gold rounded-full flex items-center justify-center text-sc-navy font-bold text-xl select-none">
              C
            </div>
            <h1 className="text-sc-gold font-semibold tracking-wide text-lg sm:text-xl">
              CTJ: Focus & Flow™
            </h1>
          </div>
          
          <button
            onClick={() => setMenuOpen(!menuOpen)}
            className="p-2 text-sc-ivory hover:text-sc-gold transition-colors focus-ring rounded-lg"
            aria-label="Accessibility Settings"
            aria-expanded={menuOpen}
          >
            {menuOpen ? <X size={24} /> : <Settings size={24} />}
          </button>
        </div>

        {/* Accessibility Menu */}
        {menuOpen && (
          <div className="absolute top-16 right-0 w-full sm:w-80 bg-sc-navy border-b sm:border-l sm:border-b border-sc-gold/30 shadow-2xl p-6 space-y-4 animate-fade-in z-40">
            <h2 className="text-sc-gold font-semibold mb-4 flex items-center gap-2">
              <Accessibility size={20} />
              Display Settings
            </h2>
            
            <Toggle
              label="High Contrast"
              icon={<Eye size={18} />}
              active={state.settings.highContrast}
              onClick={() => dispatch({ type: 'TOGGLE_SETTING', payload: 'highContrast' })}
            />
            
            <Toggle
              label="Dyslexia Font"
              icon={<Type size={18} />}
              active={state.settings.dyslexiaFont}
              onClick={() => dispatch({ type: 'TOGGLE_SETTING', payload: 'dyslexiaFont' })}
            />
            
            <Toggle
              label="Reduced Motion"
              icon={<Zap size={18} />}
              active={state.settings.reducedMotion}
              onClick={() => dispatch({ type: 'TOGGLE_SETTING', payload: 'reducedMotion' })}
            />
          </div>
        )}
      </header>

      {/* Main Content */}
      <main className="flex-grow flex flex-col relative" role="main">
        {children}
      </main>

      {/* Footer */}
      <footer className="border-t border-sc-gold/20 py-8 mt-auto bg-sc-navy text-sc-muted text-sm text-center">
        <div className="max-w-3xl mx-auto px-4 space-y-4">
          <p>
            CTJ: Focus & Flow™ MVP v1.0 powered by Sonly Consulting.
          </p>
          <p className="text-xs max-w-lg mx-auto leading-relaxed opacity-70">
            Privacy Notice: This application is local-first. All data is stored in your browser's LocalStorage. 
            We do not track you, use cookies, or send data to any server. Your thoughts are yours alone.
          </p>
          <div className="pt-2">
             <button onClick={() => dispatch({type: 'RESET_SESSION'})} className="text-sc-gold/60 hover:text-sc-gold hover:underline text-xs">
               Reset All Data
             </button>
          </div>
        </div>
      </footer>
    </div>
  );
};

const Toggle: React.FC<{ label: string; icon: React.ReactNode; active: boolean; onClick: () => void }> = ({ 
  label, icon, active, onClick 
}) => (
  <button
    onClick={onClick}
    className={`w-full flex items-center justify-between p-3 rounded-lg border transition-all focus-ring
      ${active 
        ? 'bg-sc-gold text-sc-navy border-sc-gold font-semibold' 
        : 'bg-transparent text-sc-ivory border-sc-muted hover:border-sc-gold'
      }`}
    aria-pressed={active}
  >
    <div className="flex items-center gap-3">
      {icon}
      <span>{label}</span>
    </div>
    <div className={`w-3 h-3 rounded-full ${active ? 'bg-sc-navy' : 'bg-sc-muted'}`} />
  </button>
);