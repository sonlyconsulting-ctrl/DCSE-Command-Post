
import React, { useState, useEffect, useRef } from 'react';
import { Mic, MicOff, ChevronDown, ChevronUp, Copy, RefreshCw, Save } from 'lucide-react';
import { useAppContext } from '../context/AppContext';
import { PROMPTS, FRAMEWORK_CONTENT } from '../constants';
import { AIAssist } from './AIAssist';

export const JournalView: React.FC = () => {
  const { state, dispatch } = useAppContext();
  const [selectedPromptId, setSelectedPromptId] = useState(state.journal.promptId);
  const [isListening, setIsListening] = useState(false);
  const [showFramework, setShowFramework] = useState(false);
  const [showMinors, setShowMinors] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const currentPrompt = PROMPTS.find(p => p.id === selectedPromptId) || PROMPTS[0];
  const minorPrompts = PROMPTS.filter(p => p.id !== 'mvp-primary');

  // Voice Input Setup
  const recognitionRef = useRef<any>(null);

  useEffect(() => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = true;
      recognitionRef.current.interimResults = true;

      recognitionRef.current.onresult = (event: any) => {
        let finalTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; ++i) {
          if (event.results[i].isFinal) {
            finalTranscript += event.results[i][0].transcript;
          }
        }
        if (finalTranscript) {
           const newContent = (state.journal.content + ' ' + finalTranscript).trim();
           dispatch({ type: 'UPDATE_JOURNAL', payload: { content: newContent } });
        }
      };

      recognitionRef.current.onerror = (event: any) => {
        console.error('Speech recognition error', event.error);
        setIsListening(false);
      };
      
      recognitionRef.current.onend = () => {
          if (isListening) setIsListening(false);
      }
    }
  }, [state.journal.content, dispatch, isListening]);

  const toggleListening = () => {
    if (!recognitionRef.current) {
      alert("Voice input not supported in this browser. Try Chrome or Edge.");
      return;
    }
    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      recognitionRef.current.start();
      setIsListening(true);
    }
  };

  const handlePromptChange = (id: string) => {
    setSelectedPromptId(id);
    dispatch({ type: 'UPDATE_JOURNAL', payload: { promptId: id } });
    setShowMinors(false);
  };

  return (
    <div className="space-y-6 animate-fade-in pb-20">
      
      {/* Prompt Section */}
      <div className="bg-sc-ivory/5 border border-sc-gold/20 rounded-xl p-6 relative shadow-sm">
        <div className="flex justify-between items-start mb-4">
          <h2 className="text-sc-gold font-bold text-lg">{currentPrompt.title}</h2>
          <button 
             onClick={() => navigator.clipboard.writeText(currentPrompt.content)}
             className="text-sc-muted hover:text-sc-gold p-1 transition-colors" 
             title="Copy Prompt"
             aria-label="Copy prompt to clipboard"
          >
             <Copy size={16} />
          </button>
        </div>
        <div className="whitespace-pre-wrap text-sc-ivory/90 leading-relaxed font-medium">
          {currentPrompt.content}
        </div>

        {/* Minor Prompts Toggle */}
        <div className="mt-6 border-t border-sc-gold/10 pt-4">
          <button 
            onClick={() => setShowMinors(!showMinors)}
            className="text-xs text-sc-gold/70 hover:text-sc-gold uppercase tracking-wider font-semibold flex items-center gap-1 transition-colors"
          >
            {showMinors ? 'Hide Options' : 'Want a different prompt?'}
            {showMinors ? <ChevronUp size={12} /> : <ChevronDown size={12} />}
          </button>
          
          {showMinors && (
            <div className="mt-4 space-y-2 grid gap-2 sm:grid-cols-3 animate-fade-in">
              {minorPrompts.map(p => (
                <button
                  key={p.id}
                  onClick={() => handlePromptChange(p.id)}
                  className={`text-left p-3 rounded border text-sm transition-all focus-ring
                    ${selectedPromptId === p.id 
                      ? 'bg-sc-gold text-sc-navy border-sc-gold shadow-md' 
                      : 'bg-transparent text-sc-ivory border-sc-muted/50 hover:border-sc-gold'
                    }`}
                >
                  {p.title}
                </button>
              ))}
              {selectedPromptId !== 'mvp-primary' && (
                  <button
                  onClick={() => handlePromptChange('mvp-primary')}
                  className="text-left p-3 rounded border text-sm bg-transparent text-sc-ivory border-sc-muted/50 hover:border-sc-gold focus-ring"
                >
                  Return to Primary
                </button>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Framework Card */}
      <div className="border border-sc-gold/30 rounded-lg overflow-hidden transition-all duration-300 shadow-sm">
        <button
          onClick={() => setShowFramework(!showFramework)}
          className="w-full bg-sc-navy p-4 flex items-center justify-between text-sc-ivory hover:bg-sc-ivory/5 focus-ring transition-colors"
          aria-expanded={showFramework}
        >
          <span className="font-semibold flex items-center gap-2">
            <span className="w-2 h-2 bg-sc-gold rounded-full shadow-[0_0_8px_#C8A444]"></span>
            Strategic Framework
          </span>
          {showFramework ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
        </button>
        {showFramework && (
          <div className="p-4 bg-sc-ivory/5 space-y-3 text-sm border-t border-sc-gold/10 animate-fade-in">
            <div>
              <strong className="text-sc-gold block mb-1">Mindset (Nickell)</strong>
              <p className="text-sc-ivory/80">{FRAMEWORK_CONTENT.mindset}</p>
            </div>
            <div>
              <strong className="text-sc-gold block mb-1">Evidence Check (Shermer)</strong>
              <p className="text-sc-ivory/80">{FRAMEWORK_CONTENT.checklist}</p>
            </div>
            <div>
              <strong className="text-sc-gold block mb-1">Action Hook</strong>
              <p className="text-sc-ivory/80">{FRAMEWORK_CONTENT.action}</p>
            </div>
          </div>
        )}
      </div>

      {/* Editor */}
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <label htmlFor="journal-entry" className="sr-only">Journal Entry</label>
          <div className="flex gap-4 text-xs text-sc-muted">
            <span>{state.journal.wordCount} words</span>
            <span>{state.journal.charCount} chars</span>
          </div>
          {state.journal.lastSaved && (
              <span className="text-xs text-sc-gold/60 flex items-center gap-1">
                  <Save size={10} /> Saved
              </span>
          )}
        </div>
        
        <div className="relative">
          <textarea
            id="journal-entry"
            ref={textareaRef}
            value={state.journal.content}
            onChange={(e) => dispatch({ type: 'UPDATE_JOURNAL', payload: { content: e.target.value } })}
            placeholder="Type your reflection here, or tap the mic to speak..."
            className="w-full bg-sc-ivory/5 border border-sc-muted/50 focus:border-sc-gold rounded-xl p-4 min-h-[300px] text-sc-ivory placeholder-sc-muted/50 resize-y focus-ring text-lg leading-relaxed font-serif transition-colors"
            spellCheck="false"
          />
          
          <button
            onClick={toggleListening}
            className={`absolute bottom-4 right-4 p-3 rounded-full shadow-lg transition-all focus-ring
              ${isListening 
                ? 'bg-red-500 text-white animate-pulse shadow-red-500/50' 
                : 'bg-sc-gold text-sc-navy hover:bg-white hover:scale-110'}`}
            title={isListening ? "Stop Recording" : "Start Voice Input"}
          >
            {isListening ? <MicOff size={24} /> : <Mic size={24} />}
          </button>
        </div>
      </div>

      {/* AI Assist Component */}
      <AIAssist content={state.journal.content} />

      {/* Actions */}
      <div className="flex justify-between items-center pt-8 border-t border-sc-gold/10 mt-8">
         <button 
           onClick={() => {
               if(window.confirm('Clear your journal entry?')) {
                   dispatch({type: 'UPDATE_JOURNAL', payload: { content: '' }});
               }
           }}
           className="text-sc-muted hover:text-red-400 text-sm flex items-center gap-1 px-2 py-1 rounded focus-ring transition-colors"
         >
             <RefreshCw size={14} /> Clear
         </button>

         <button
            onClick={() => dispatch({ type: 'SET_VIEW', payload: 'export' })}
            disabled={state.journal.wordCount < 5}
            className="bg-sc-gold disabled:opacity-50 disabled:cursor-not-allowed text-sc-navy font-bold py-3 px-8 rounded-full hover:shadow-[0_4px_14px_0_rgba(200,164,68,0.39)] hover:-translate-y-0.5 transition-all focus-ring"
         >
            Finish & Export
         </button>
      </div>
    </div>
  );
};
